import json
import asyncio
from cachetools import TTLCache
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
    def __init__(self):
        super().__init__(model=Metric)

    @staticmethod
    def get_top_30_by_date(data):
        # 使用 defaultdict 简化分组操作
        date_groups = defaultdict(list)
        for row in data:
            date_groups[row["date"]].append(row)

        # 对每个日期组内的数据按value排序并取前30
        result = []
        for date in sorted(date_groups.keys()):
            sorted_group = sorted(
                date_groups[date], key=lambda x: x["value"], reverse=True
            )[:30]
            result.extend(sorted_group)

        return result

    async def fetch_metric_data(
        self,
        metric,
        date_formats,
        statistical_period,
        date_range,
        search_dimensions,
        condition_sql_string,
        period_formats,
    ):
        # 创建一个缓存，设置过期时间, 200个条目，10分钟
        cache = TTLCache(maxsize=300, ttl=600)

        # 检查是否有关联的数据模型
        if metric.data_model:

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
                date_search_sql_string = (
                    f"BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
                )
            else:
                if metric.statistical_period == "day":
                    date_search_sql_string = f">= DATE_SUB(CURDATE(), INTERVAL {metric.chart_display_date} {metric.statistical_period})"
                else:
                    date_search_sql_string = f">= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL {metric.chart_display_date} {metric.statistical_period}), '%Y-%m-01')"

            # 获取用于维度统计的查询字段
            search_dimensions_sql_string = (
                search_dimensions + "," if search_dimensions else ""
            )

            # 构建 SQL 查询语句
            sql_query = f"""
            SELECT 
                DATE_FORMAT({date_column}, '{date_format_sql_string}') as date,
                {search_dimensions_sql_string}
                {static_type}({metric_column}){extended_computation} as value
            FROM {table_name}
            WHERE {date_column} {date_search_sql_string} {condition_sql_string}
            GROUP BY {search_dimensions_sql_string} DATE_FORMAT({date_column}, '{date_format_sql_string}')
            ORDER BY date, value DESC
            """

            conn = Tortoise.get_connection(connection_name="default")

            try:
                _, data = await conn.execute_query(sql_query)

                # 如果有维度筛选，则处理 top 30，防止维度数据过多
                if search_dimensions_sql_string:
                    data = self.get_top_30_by_date(data)

                metric.format = format_type

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
                    if dim_value in cache:
                        dimension["options"] = cache[dim_value]
                    else:
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
                        cache[dim_value] = options

                metric.dimensions = dimensions
                metric.tags = [period_formats[metric.statistical_period], "2024"]
                metric.data = data

            except:
                print("sql query error")
            else:
                return "查询错误"

    async def list(
        self,
        page: int,
        page_size: int,
        search: Q = Q(),
        search_dimensions: str | None = None,
        condition_sql_string: str | None = None,
        date_range: list[str] | None = None,
        statistical_period: str | None = None,
        order: list[str] | None = None,
    ) -> tuple[Total, list[ModelType]]:
        if order is None:
            order = []

        # 获取指标和关联的主题模型,一次性获取所需数据
        query = self.model.filter(search).select_related("data_model__database")

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
            self.fetch_metric_data(
                metric,
                date_formats,
                statistical_period,
                date_range,
                search_dimensions,
                condition_sql_string,
                period_formats,
            )
            for metric in metrics
        ]

        await asyncio.gather(*tasks)

        return Total(total), metrics

    async def create(self, obj_in: MetricCreate) -> Metric:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj_in.data_model = await DataModel.get(id=obj_in.data_model)
        return await super().create(obj_in)

    async def update(self, id, obj_in: MetricUpdate) -> Metric:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj_in.data_model = await DataModel.get(id=obj_in.data_model)
        return await super().update(id, obj_in)

    async def remove(self, id: int) -> Metric:
        return await super().remove(id)


metric_controller = MetricController()
