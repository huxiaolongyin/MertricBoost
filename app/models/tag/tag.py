# 支持异步的ORM库
from tortoise import fields
from app.models.utils import (
    BaseModel,
    TimestampMixin,
)


class Tag(BaseModel, TimestampMixin):
    """标签类型表"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True, description="标签名称")
    type = fields.CharField(max_length=50, description="标签类型")
    description = fields.CharField(max_length=255, description="标签描述")
    creator = fields.ForeignKeyField(
        "app_system.User", related_name="created_tags", description="创建人"
    )  # 关联到用户表

    class Meta:
        table = "metric_tag_type"
        table_description = "指标标签类型"


class MetricTag(BaseModel, TimestampMixin):
    """指标标签关系表"""

    id = fields.IntField(pk=True)
    metric = fields.ForeignKeyField(
        "app_system.Metric", description="指标"
    )  # 关联到指标表
    tag = fields.ForeignKeyField("app_system.Tag", description="标签")  # 关联到标签表
    creator = fields.ForeignKeyField("app_system.User", description="创建人")

    class Meta:
        table = "metric_tags"
        table_description = "指标标签关系"
        unique_together = ("metric", "tag")
