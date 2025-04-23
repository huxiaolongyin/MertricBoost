from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin


class Tag(BaseModel, TimestampMixin):
    """标签类型表"""

    id = fields.IntField(primary_key=True)
    tag_name = fields.CharField(max_length=50, unique=True, description="标签名称")
    tag_type = fields.CharField(max_length=50, null=True, description="标签类型")
    tag_desc = fields.CharField(max_length=255, null=True, description="标签描述")
    update_by = fields.ForeignKeyField(
        "app_system.User", related_name="updated_tags", description="更新人"
    )
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_tags", description="创建人"
    )

    class Meta:
        table = "tags"
        table_description = "指标标签类型"
