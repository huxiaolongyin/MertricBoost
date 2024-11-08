from app.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricUpdate
from app.models.system import User, DataModel, Database
from app.core.crud import CRUDBase
from typing import Any, Generic, NewType, TypeVar
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
        order: list[str] | None = None,
    ) -> tuple[Total, list[ModelType]]:
        if order is None:
            order = []

        # 1. 获取指标和关联的主题模型
        query = (
            self.model.filter(search)
            .select_related("data_model")
            .select_related("data_model__database")
        )
        # 遍历结果，为每个指标加载数据
        metrics = await query.offset((page - 1) * page_size).limit(page_size)

        for metric in metrics:

            # 获取数据库配置
            if metric.data_model:
                db_config = metric.data_model.database
                connection_url = f"{db_config.database_type}://{db_config.database_user}:{db_config.password}@{db_config.database_host}:{db_config.database_port}/{db_config.database_database}"

                await Tortoise.init(db_url=connection_url, modules={"models": []})
                table_name = metric.data_model.table_name
                field_conf = eval(metric.data_model.field_conf)

                # 获取指标的日期限制
                date_limit = metric.chart_display_date + " " + metric.statistical_period
                print(date_limit)

                # 获取维度的字段
                dimension_columns = ",".join(
                    [
                        field["columnName"]
                        for field in field_conf
                        if field["semanticType"] == "dimension"
                    ]
                )

                # 获取指标的字段
                metric_columns, static_type = [
                    (field["columnName"], field["staticType"])
                    for field in field_conf
                    if field["semanticType"] == "metric"
                ][0]

                # 获取日期字段
                date_column, date_format = [
                    (field["columnName"], field["dateFormat"])
                    for field in field_conf
                    if field["semanticType"] == "date"
                ][0]
                if date_format == "YYYY-MM-DD":
                    mysql_date_format = "%Y-%m-%d"
                elif date_format == "YYYY/MM/DD":
                    mysql_date_format = "%Y/%m/%d"
                elif date_format == "YYYY年MM月DD日":
                    mysql_date_format = "%Y年%m月%d日"
                # print(date_column, date_format)
                sql_query = f"""
                SELECT 
                    DATE_FORMAT({date_column}, '{mysql_date_format}') as date,
                    {dimension_columns},
                    {static_type}({metric_columns}) as value
                FROM {table_name}
                WHERE {date_column} >= DATE_SUB(CURDATE(), INTERVAL {date_limit})
                GROUP BY {dimension_columns}, DATE_FORMAT({date_column}, '{mysql_date_format}')
                ORDER BY DATE_FORMAT({date_column}, '{mysql_date_format}') DESC
                """
                print(sql_query)

                conn = Tortoise.get_connection(connection_name="default")
                try:
                    _, results = await conn.execute_query(sql_query)
                    metric.data = results
                    print(results)
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
