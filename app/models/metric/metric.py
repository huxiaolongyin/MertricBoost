# 支持异步的ORM库
from tortoise import fields
from app.models.utils import (
    BaseModel,
    TimestampMixin,
)
from enum import Enum


class PublishStatus(str, Enum):
    UNPUBLISHED = "2"
    PUBLISHED = "1"


class ChartType(str, Enum):
    LINE = "line"
    BAR = "bar"


class Metric(BaseModel, TimestampMixin):
    id = fields.IntField(pk=True)
    data_model = fields.ForeignKeyField(
        "app_system.DataModel", related_name="metrics", description="数据模型"
    )
    business_scope = fields.CharField(max_length=255, description="业务口径")
    chinese_name = fields.CharField(max_length=100, description="中文名")
    english_name = fields.CharField(max_length=100, description="英文名")
    alias = fields.CharField(max_length=100, description="别名", null=True)
    sensitivity = fields.CharField(max_length=10, description="敏感度")
    statistical_period = fields.CharField(max_length=20, description="统计周期")
    chart_type = fields.CharField(max_length=50, description="图表类型")
    chart_display_date = fields.CharField(max_length=20, description="图表显示日期")
    create_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="created_metrics",
        description="创建人",
    )  # 关联到用户表
    publish_status = fields.CharEnumField(
        PublishStatus, default=PublishStatus.UNPUBLISHED, description="发布状态"
    )
    publish_url = fields.CharField(max_length=255, null=True, description="发布地址")
    publish_pwd = fields.CharField(max_length=255, null=True, description="访问密码")

    # 反向关联
    tags = fields.ManyToManyField(
        "app_system.Tag",
        through="metric_tags",
        related_name="metrics",
        description="标签",
    )

    class Meta:
        table = "metrics"
        table_description = "指标管理信息"


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


# class DataModel(BaseModel, TimestampMixin):
#     """数据模型"""

#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=100, description="数据模型名称")
#     description = fields.CharField(max_length=255, description="数据模型描述")
#     creator = fields.ForeignKeyField(
#         "app_system.User",
#         related_name="created_data_models",
#         description="创建人",
#     )
#     # 关联到用户表
#     method = fields.CharField(max_length=255, description="方法")

#     class Meta:
#         table = "data_models"
#         table_description = "数据模型"
