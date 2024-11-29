from tortoise import fields
from app.models.utils import BaseModel, TimestampMixin


class Database(BaseModel, TimestampMixin):
    """数据库信息"""

    id = fields.IntField(pk=True)
    database_name = fields.CharField(max_length=50, description="数据库名称")
    database_type = fields.CharField(max_length=50, description="数据库类型")
    database_host = fields.CharField(max_length=50, description="数据库主机")
    database_port = fields.IntField(description="数据库端口")
    database_user = fields.CharField(max_length=50, description="数据库用户")
    password = fields.CharField(max_length=255, description="数据库密码")
    database_database = fields.CharField(max_length=255, description="选用的数据库")
    status = fields.CharField(max_length=50, description="数据库状态，1启用，2禁用")
    database_desc = fields.CharField(
        max_length=255, description="数据库描述", null=True
    )
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="create_by", description="创建人"
    )

    class Meta:
        table = "databases"
        table_description = "数据库信息"
