from tortoise import fields
from app.models.utils import (
    BaseModel,
    TimestampMixin,
)

class ServiceApp(BaseModel, TimestampMixin):
    id = fields.IntField(pk=True)
    app_name = fields.CharField(max_length=50, unique=True, description="应用名称")
    app_desc = fields.CharField(max_length=255, description="应用描述")
    app_status = fields.IntField(default=2, description="应用状态")
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_apps", description="创建人"
    )

    class Meta:
        table = "service_apps"
        table_description = "应用"

