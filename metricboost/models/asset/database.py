from typing import Tuple

import aiomysql
from tortoise import fields

from metricboost.logger import get_logger
from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import StatusType

logger = get_logger(__name__)


class Database(BaseModel, TimestampMixin):
    """数据库信息"""

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50, description="数据库名称")
    type = fields.CharField(max_length=50, description="数据库类型")
    host = fields.CharField(max_length=50, description="数据库主机")
    port = fields.IntField(description="数据库端口")
    username = fields.CharField(max_length=50, description="数据库用户")
    password = fields.CharField(max_length=255, description="数据库密码")
    database = fields.CharField(max_length=255, description="选用的数据库")
    status = fields.CharEnumField(
        StatusType, default=StatusType.enable, description="数据库状态，1启用，0禁用"
    )
    description = fields.CharField(max_length=255, description="数据库描述", null=True)
    update_by = fields.ForeignKeyField(
        "app_system.User", related_name="updated_databases", description="更新人"
    )
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_databases", description="创建人"
    )

    class Meta:
        table = "databases"
        table_description = "数据库信息"

    async def get_connection(self):
        """获取 MySQL 数据库连接"""
        # 检查数据库是否存在
        try:
            conn = await aiomysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                db=self.database,
            )
            logger.debug("成功连接到数据库")
            return conn
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise e

    async def execute(self, sql: str) -> list[dict]:
        """执行 SQL 语句"""
        conn = await self.get_connection()
        logger.debug(f"执行SQL查询: {sql}")
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql)
                await conn.commit()
                result = await cursor.fetchall()
                logger.debug("SQL 执行成功")
                return result
        except Exception as e:
            logger.error(f"SQL 执行失败: {e}")
            raise e
        finally:
            conn.close()
            logger.debug("数据库连接已关闭")
