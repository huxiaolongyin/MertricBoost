import json
import asyncio
from cachetools import TTLCache, cached
from collections import defaultdict
from app.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricUpdate
from app.models.system import User, DataModel
from app.core.crud import CRUDBase
from typing import NewType, TypeVar
from pydantic import BaseModel
from tortoise.expressions import Q
from tortoise.models import Model
from tortoise import Tortoise

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class MetricController(CRUDBase[Metric, MetricCreate, MetricUpdate]):
    _cache = TTLCache(maxsize=100, ttl=600)

    def __init__(self):
        super().__init__(model=Metric)

    @staticmethod
    def get_top_30_by_date(data, sort):
        # 使用 defaultdict 简化分组操作
        date_groups = defaultdict(list)
        for row in data:
            date_groups[row["date"]].append(row)

        # 对每个日期组内的数据按value排序并取前30
        result = []
        for date in sorted(date_groups.keys()):
            sorted_group = sorted(
                date_groups[date], key=lambda x: x["value"], reverse=sort != "desc"
            )[:30]
            result.extend(sorted_group)

        return result

    @classmethod
    async def fetch_metric_data(
        cls,
        metric,
        date_formats,
        statistical_period,
        date_range,
        dimension_drilldown,
        condition_sql_string,
        period_formats,
        sort,
    ):

        # 生成 sql 语句
        table_name = metric.data_model.table_name
        field_conf = json.loads(metric.data_model.field_conf)

        # 获取日期字段和格式
        date_field = next(
            (field for field in field_conf if field["semanticType"] == "date"), None
        )
        if not date_field:
            return "没有日期字段"  # 如果没有日期字段

        date_column = date_field["columnName"]
        date_format = date_field["format"]
        date_format_sql_string = date_formats[date_format].get(
            metric.statistical_period, "%Y-%m-%d"
        )

        # 如果指定统计周期，则使用指定的统计周期
        if statistical_period:
            date_format_sql_string = {
                "day": "%Y-%m-%d",
                "week": "%Y-%u",
                "month": "%Y-%m",
                "year": "%Y",
            }.get(statistical_period, date_format_sql_string)

        # 获取指标字段和统计方式
        metric_field = next(
            (field for field in field_conf if field["semanticType"] == "metric"),
            None,
        )
        if not metric_field:
            return "没有指标字段"  # 如果没有指标字段，则跳过

        metric_column = metric_field["columnName"]
        static_type = metric_field["staticType"]
        format_type = metric_field["format"]
        extended_computation = (
            ""
            if metric_field["extendedComputation"] is None
            else metric_field["extendedComputation"]
        )

        # 设置日期搜索的SQL查询语句
        if date_range:
            date_search_sql_string = f"BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
        else:
            if metric.statistical_period == "day":
                date_search_sql_string = f">= DATE_SUB(CURDATE(), INTERVAL {metric.chart_display_date} {metric.statistical_period})"
            else:
                date_search_sql_string = f">= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL {metric.chart_display_date} {metric.statistical_period}), '%Y-%m-01')"

        # 获取用于维度统计的查询字段
        dimension_drilldown_sql_string = (
            f"{dimension_drilldown}," if dimension_drilldown else ""
        )

        # 构建 SQL 查询语句
        sql_query = f"""
        SELECT 
            DATE_FORMAT({date_column}, '{date_format_sql_string}') as date,
            {dimension_drilldown_sql_string}
            {static_type}({metric_column}){extended_computation} as value
        FROM {table_name}
        WHERE {date_column} {date_search_sql_string} {condition_sql_string}
        GROUP BY {dimension_drilldown_sql_string} DATE_FORMAT({date_column}, '{date_format_sql_string}')
        ORDER BY date, value DESC
        """

        # 如果缓存中存在查询结果，则直接返回
        if sql_query in cls._cache:
            metric.data, metric.dimensions, metric.tags, metric.format = cls._cache[
                sql_query
            ]
            return

        # 获取数据库配置并建立连接
        db_config = metric.data_model.database
        connection_url = (
            f"{db_config.database_type}://{db_config.database_user}:"
            f"{db_config.password}@{db_config.database_host}:"
            f"{db_config.database_port}/{db_config.database_database}"
        )

        await Tortoise.init(
            db_url=connection_url,
            modules={"models": []},
            timezone="Asia/Shanghai",
        )
        conn = Tortoise.get_connection(connection_name="default")
        try:
            if sql_query in cls._cache:
                data = cls._cache[sql_query]
            else:
                # 执行 SQL 查询
                _, data = await conn.execute_query(sql_query)
                cls._cache[sql_query] = data
            # 如果有维度筛选，则处理 top 30，防止维度数据过多
            if dimension_drilldown_sql_string:
                data = cls.get_top_30_by_date(data, sort)

            # 获取可扩展的维度字段以及选项
            dimensions = [
                {
                    "label": field["columnComment"],
                    "value": field["columnName"],
                }
                for field in field_conf
                if field["semanticType"] == "dimension"
            ]

            # 从现有数据获取 metric.dimensions 的唯一值，作为可选项
            for dimension in dimensions:
                dim_value = dimension["value"]
                dim_query = f"""
                    SELECT 
                        DISTINCT {dim_value} 
                    FROM {table_name} 
                    WHERE {date_column} {date_search_sql_string}
                """
                _, dimension_data = await conn.execute_query(dim_query)
                options = [
                    {"label": item[dim_value], "value": item[dim_value]}
                    for item in dimension_data
                ]
                dimension["options"] = options

            metric.data = data
            metric.dimensions = dimensions
            metric.tags = [period_formats[metric.statistical_period], "2024"]
            metric.format = format_type
            # 缓存
            cls._cache[sql_query] = (
                data,
                dimensions,
                [period_formats[metric.statistical_period]],
                format_type,
            )

        except:
            print("sql query error")
        else:
            return "查询错误"

    @classmethod
    async def list(
        cls,
        page: int,
        page_size: int,
        search: Q = Q(),
        dimension_drilldown: str | None = None,
        condition_sql_string: str | None = None,
        date_range: list[str] | None = None,
        statistical_period: str | None = None,
        sort: str | None = None,
    ) -> tuple[Total, list[ModelType]]:
        """
        从指标获取相应的数据库配置信息，连接数据库，获取指标数据
        args:
            page: 页码
            page_size: 每页数量
            search: 查询条件
            dimension_drilldown: 维度钻取
            condition_sql_string: 条件查询
            date_range: 日期范围
            statistical_period: 统计周期
            sort: 排序方式
        returns:
            tuple[Total, list[ModelType]]: 指标数据
        """

        # 获取指标和关联的主题模型,一次性获取所需数据
        query = cls().model.filter(search).select_related("data_model__database")

        # 定义日期格式映射
        date_formats = {
            "YYYY-MM-DD": {"day": "%Y-%m-%d", "month": "%Y-%m", "year": "%Y"},
            "YYYY/MM/DD": {"day": "%Y/%m/%d", "month": "%Y/%m", "year": "%Y"},
            "YYYY年MM月DD日": {
                "day": "%Y年%m月%d日",
                "month": "%Y年%m月",
                "year": "%Y年",
            },
        }

        # 定义统计周期映射
        period_formats = {
            "day": "每日",
            "week": "每周",
            "month": "月份",
            "year": "年度",
        }

        # 遍历结果，为每个指标加载数据
        total = await query.count()
        metrics = await query.offset((page - 1) * page_size).limit(page_size)

        tasks = [
            cls.fetch_metric_data(
                metric,
                date_formats,
                statistical_period,
                date_range,
                dimension_drilldown,
                condition_sql_string,
                period_formats,
                sort,
            )
            for metric in metrics
            if metric.data_model
        ]

        await asyncio.gather(*tasks)

        return Total(total), metrics

    @classmethod
    async def create(cls, obj_in: MetricCreate) -> Metric:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj_in.data_model = await DataModel.get(id=obj_in.data_model)
        return await super().create(obj_in)

    @classmethod
    async def update(cls, id, obj_in: MetricUpdate) -> Metric:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj_in.data_model = await DataModel.get(id=obj_in.data_model)
        return await super().update(id, obj_in)

    @classmethod
    async def remove(cls, id: int) -> Metric:
        return await super().remove(id)


metric_controller = MetricController()
