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
    id = fields.IntField(primary_key=True)
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
    chart_display_date = fields.IntField(description="图表显示日期")
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
        fields_for_dict = {"data": "data"}  # 添加data到序列化字段

    @property
    def data(self):
        return getattr(self, "_data", None)

    @data.setter
    def data(self, value):
        setattr(self, "_data", value)

    # 获取指标的维度
    @property
    def dimensions(self):
        return getattr(self, "_dimensions", None)

    @dimensions.setter
    def dimensions(self, value):
        setattr(self, "_dimensions", value)

    # 获取标签的内容
    @property
    def tags(self):
        return getattr(self, "_tags", None)

    @tags.setter
    def tags(self, value):
        setattr(self, "_tags", value)

    # 获取指标的格式
    @property
    def format(self):
        return getattr(self, "_format", None)

    @format.setter
    def format(self, value):
        setattr(self, "_format", value)

    async def to_dict(self):
        result = await super().to_dict()
        result["formatType"] = self.format
        result["dimensions"] = self.dimensions
        result["tags"] = self.tags
        result["data"] = self.data  # 手动添加data到结果字典
        return result
