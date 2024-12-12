from tortoise import fields
from app.models.utils import (
    BaseModel,
    TimestampMixin,
)


class ServiceApp(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True)
    app_name = fields.CharField(max_length=50, unique=True, description="应用名称")
    app_desc = fields.CharField(max_length=255, description="应用描述")
    status = fields.IntField(default=2, description="应用状态")
    app_key = fields.CharField(max_length=255, unique=True, description="应用key")
    app_secret = fields.CharField(max_length=255, description="应用密钥")
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_apps", description="创建人"
    )

    class Meta:
        table = "service_apps"
        table_description = "应用"
