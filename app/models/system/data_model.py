from tortoise import fields
from app.models.utils import BaseModel, TimestampMixin


class DataModel(BaseModel, TimestampMixin):
    """数据模型信息"""

    id = fields.IntField(pk=True)
    data_model_name = fields.CharField(max_length=50, description="模型名称")
    data_model_desc = fields.CharField(max_length=255, description="主题描述")
    status = fields.CharField(max_length=50, description="模型状态")
    # statistic_column = fields.CharField(max_length=50, description="统计字段")
    # statistic_type = fields.CharField(max_length=50, description="统计方式")
    # aggregated_column = fields.CharField(max_length=50, description="聚合字段")
    table_name = fields.CharField(max_length=50, description="表名")
    field_conf = fields.TextField(description="字段配置")
    database = fields.ForeignKeyField("app_system.Database", related_name="database")
    data_domain = fields.ForeignKeyField(
        "app_system.DataDomain", related_name="data_domain"
    )

    topic_domain = fields.ForeignKeyField(
        "app_system.TopicDomain", related_name="topic_domain"
    )
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_topic", description="创建人"
    )

    class Meta:
        table = "data_models"
        table_description = "数据模型信息"
