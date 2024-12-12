from tortoise import fields
from app.models.utils import BaseModel, TimestampMixin


class DataDomain(BaseModel, TimestampMixin):
    """数据域信息"""

    id = fields.IntField(primary_key=True)
    domain_name = fields.CharField(max_length=50, description="数据域名称")
    domain_desc = fields.CharField(max_length=255, description="数据域描述")
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="create_data_domain", description="创建人"
    )

    class Meta:
        table = "data_domains"
        table_description = "数据域信息"


class TopicDomain(BaseModel, TimestampMixin):
    """主题域信息"""

    id = fields.IntField(primary_key=True)
    domain_name = fields.CharField(max_length=50, description="数据域名称")
    domain_desc = fields.CharField(max_length=255, description="数据域描述")
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_topic_domain", description="创建人"
    )

    class Meta:
        table = "topic_domains"
        table_description = "主题域信息"
