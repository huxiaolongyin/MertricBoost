from typing import Tuple

from metricboost.core.crud import CRUDBase
from metricboost.core.ctx import get_current_user_id
from metricboost.logger import get_logger
from metricboost.models.asset import Database, DataModel, Domain
from metricboost.models.enums import EditMode
from metricboost.schemas.model import DataModelCreate, DataModelUpdate

logger = get_logger(__name__)


class DataMobdelController(CRUDBase[DataModel, DataModelCreate, DataModelUpdate]):
    def __init__(self):
        super().__init__(model=DataModel)

    async def update_domain_ids(self, data_model: DataModel, domain_ids: list[int]):
        """
        更新数据模型关联的域ID
        """
        await data_model.domains.clear()
        for domain_id in domain_ids:
            domain = await Domain.get_or_none(id=domain_id)
            if domain:
                await data_model.domains.add(domain)

    async def create(self, obj_in: DataModelCreate, exclude=None):
        """
        创建数据模型
        """
        # 检查数据名称是否重复
        if await self.model.filter(name=obj_in.name).first():
            raise ValueError("数据模型名称已存在")

        # 检查表名是否重复
        # if await self.model.filter(table_name=obj_in.table_name).first():
        #     raise ValueError("表名已存在")

        # 检查数据库是否存在
        if not await Database.get_or_none(id=obj_in.database_id):
            raise ValueError("指定的数据库不存在")

        # 获取当前用户ID
        current_user_id = get_current_user_id()
        # 设置创建人和更新人
        obj_in.create_by_id = current_user_id
        obj_in.update_by_id = current_user_id

        # 创建数据模型
        return await super().create(obj_in=obj_in, exclude=exclude)

    async def update(self, id: int, obj_in: DataModelUpdate, exclude=None):
        """
        更新数据模型
        """
        # 检查数据名称是否重复
        if await self.model.filter(name=obj_in.name).exclude(id=id).first():
            raise ValueError("数据模型名称已存在")

        # 检查数据库是否存在
        if obj_in.database_id:
            if not await Database.get_or_none(id=obj_in.database_id):
                raise ValueError("指定的数据库不存在")

        # 获取当前用户ID
        current_user_id = get_current_user_id()
        # 设置更新人
        obj_in.update_by_id = current_user_id

        # 更新数据模型
        return await super().update(id=id, obj_in=obj_in, exclude=exclude)

    async def remove(self, id: int):
        """
        删除数据模型
        """
        # 检查数据模型是否存在
        obj = await self.get(id=id)
        if not obj:
            raise ValueError("数据模型不存在")

        # 删除数据模型
        return await super().remove(id=id)

    async def fetch_table_preview(
        self,
        database_id: int,
        table_name: str,
        page: int,
        page_size: int,
    ) -> Tuple[int, dict]:
        """
        预览表数据的内容
        Args:
            database_id: 数据库ID
            table_name: 表名
            page: 当前页码
            page_size: 每页大小
        """
        # 检查数据库是否存在
        database = await Database.get_or_none(id=database_id)
        if not database:
            raise ValueError("指定的数据库不存在")

        # 获取总数
        total = await database.execute(f"SELECT COUNT(*) as total FROM {table_name}")

        # 配置SQL语句
        sql_query = f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {(page - 1) * page_size}"

        # 获取表数据的内容
        data = await database.execute(sql_query)

        return total[0].get("total"), data

    async def fetch_table_metadata(self, database_id: int):
        """
        获取数据库中所有的表名称
        """
        # 检查数据库是否存在
        database = await Database.get_or_none(id=database_id)
        if not database:
            raise ValueError("指定的数据库不存在")

        # 配置SQL
        sql_query = f"""
        SELECT
            TABLE_NAME as tableName,
            TABLE_COMMENT as tableComment
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{database.database}'
        """
        # 获取数据库中所有的表
        tables = await database.execute(sql_query)

        # 获取已存在于DataModel中的表名
        existing_tables = await DataModel.filter().values_list("table_name", flat=True)

        # 为结果添加disabled标记
        result = []
        for table in tables:
            # 检查表名是否已存在于DataModel中
            if table["tableName"] in existing_tables:
                table["disabled"] = "1"
            result.append(table)

        return result

    async def fetch_column_metadata(
        self, database_id: int, table_name: str, edit_mode: EditMode
    ):
        """
        获取字段配置信息，从数据库元数据表和数据模型配置获取
        如果数据模型中没有配置或者配置与数据库元数据表中的字段不一致，则从数据库元数据表中获取。
        Args:
            database_id: 数据库ID
            table_name: 表名
        """
        # 检查数据库是否存在
        database = await Database.get_or_none(id=database_id)
        if not database:
            raise ValueError("指定的数据库不存在")

        # 配置SQL语句
        sql_query = f"""
        SELECT 
            COLUMN_NAME as columnName, 
            COLUMN_TYPE as columnType, 
            COLUMN_COMMENT as columnComment,
            "" as staticType,
            "" as aggMethod,
            "" as format,
            "" as extraCaculate
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = '{database.database}'
        AND TABLE_NAME = '{table_name}'
        """

        columns_config = await database.execute(sql_query)

        if edit_mode == EditMode.add:
            logger.debug("使用数据库配置的字段元数据")
            return columns_config
        else:
            # 检查数据模型是否存在
            datamodel = await DataModel.filter(
                database_id=database_id, table_name=table_name
            ).first()
            if not datamodel:
                logger.debug("数据模型不存在，使用数据库配置")
                return columns_config
            try:
                columns_conf = eval(datamodel.columns_conf)
            except Exception:
                logger.error("字段配置解析失败，使用数据库配置")
                raise ValueError("字段配置解析失败")

            # 检查字段配置是否为空
            if not columns_conf:
                logger.debug("字段配置为空，使用数据库配置")
                return columns_config

            # 创建字段配置映射
            field_map = {
                column_conf["columnName"]: column_conf for column_conf in columns_conf
            }

            merged_metadata = [
                {
                    "columnName": col["columnName"],
                    "columnType": col["columnType"],
                    "columnComment": col["columnComment"],
                    "staticType": field_map.get(col["columnName"], {}).get(
                        "staticType", ""
                    ),
                    "aggMethod": field_map.get(col["columnName"], {}).get(
                        "aggMethod", ""
                    ),
                    "format": field_map.get(col["columnName"], {}).get("format", ""),
                    "extraCaculate": field_map.get(col["columnName"], {}).get(
                        "extraCaculate", ""
                    ),
                }
                for col in columns_config
            ]

            logger.debug("合并数据库字段元数据和字段配置完成")
            return merged_metadata


data_model_controller = DataMobdelController()
