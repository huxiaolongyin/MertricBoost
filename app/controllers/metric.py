import json
from app.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricUpdate
from app.models.system import User, DataModel, Database
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

    async def list(
        self,
        page: int,
        page_size: int,
        search: Q = Q(),
        search_dimensions: str | None = None,
        condition_sql_string: str | None = None,
        date_range: list[str] | None = None,
        order: list[str] | None = None,
    ) -> tuple[Total, list[ModelType]]:
        if order is None:
            order = []

        # 获取指标和关联的主题模型
        query = (
            self.model.filter(search)
            .select_related("data_model")
            .select_related("data_model__database")
        )

        # 进行日期在 mysql 的格式化
        formats = {
            "YYYY-MM-DD": {
                "day": "%Y-%m-%d",
                "month": "%Y-%m",
                "year": "%Y",
            },
            "YYYY/MM/DD": {
                "day": "%Y/%m/%d",
                "month": "%Y/%m",
                "year": "%Y",
            },
            "YYYY年MM月DD日": {
                "day": "%Y年%m月%d日",
                "month": "%Y年%m月",
                "year": "%Y年",
            },
        }

        # 根据统计周期，生成指标
        period_formats = {
            "day": "每日",
            "month": "月份",
            "quarter": "季度",
            "year": "年度",
        }

        # 遍历结果，为每个指标加载数据
        metrics = await query.offset((page - 1) * page_size).limit(page_size)
        for metric in metrics:
            # 获取数据库配置
            if metric.data_model:
                db_config = metric.data_model.database
                connection_url = f"{db_config.database_type}://{db_config.database_user}:{db_config.password}@{db_config.database_host}:{db_config.database_port}/{db_config.database_database}"

                await Tortoise.init(
                    db_url=connection_url,
                    modules={"models": []},
                    timezone="Asia/Shanghai",
                )
                table_name = metric.data_model.table_name
                field_conf = json.loads(metric.data_model.field_conf)

                # 获取指标用于维度统计的查询语句
                search_dimensions_sql_string = (
                    search_dimensions + "," if search_dimensions else ""
                )

                # 获取日期字段
                date_column, date_format = [
                    (
                        field["columnName"],
                        field["format"],
                    )
                    for field in field_conf
                    if field["semanticType"] == "date"
                ][0]

                # 用于格式化日期的查询语句
                date_format_sql_string = formats[date_format][metric.statistical_period]

                # 获取指标的字段、统计方式、格式
                metric_columns, static_type, format_type = [
                    (field["columnName"], field["staticType"], field["format"])
                    for field in field_conf
                    if field["semanticType"] == "metric"
                ][0]

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

                sql_query = f"""
                SELECT 
                    DATE_FORMAT({date_column}, '{date_format_sql_string}') as date,
                    {search_dimensions_sql_string}
                    {static_type}({metric_columns}) as value
                FROM {table_name}
                WHERE {date_column} {date_search_sql_string} {condition_sql_string}
                GROUP BY {search_dimensions_sql_string} DATE_FORMAT({date_column}, '{date_format_sql_string}')
                ORDER BY DATE_FORMAT({date_column}, '{date_format_sql_string}')
                """

                conn = Tortoise.get_connection(connection_name="default")
                try:
                    _, data = await conn.execute_query(sql_query)
                    metric.format = format_type

                    # 获取可以扩展的维度字段
                    metric.dimensions = [
                        {
                            "label": field["columnComment"],
                            "value": field["columnName"],
                            # "options": dimension_options[field["columnName"]],
                        }
                        for field in field_conf
                        if field["semanticType"] == "dimension"
                    ]

                    # 从现有数据获取 metric.dimensions 的唯一值，作为可选项
                    for dimension in metric.dimensions:
                        dim_value = dimension["value"]
                        dim_query = f"SELECT DISTINCT {dim_value} FROM {table_name} WHERE {date_column} {date_search_sql_string}"
                        _, dimension_data = await conn.execute_query(dim_query)
                        dimension["options"] = [
                            {"label": item[dim_value], "value": item[dim_value]}
                            for item in dimension_data
                        ]

                    metric.tags = [period_formats[metric.statistical_period], "2024"]
                    metric.data = data
                except:
                    print("sql query error")
            else:

                continue
        total = await query.count()
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
