from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import DomainType


class Domain(BaseModel, TimestampMixin):
    """数据域信息"""

    id = fields.IntField(primary_key=True)
    domain_name = fields.CharField(max_length=50, description="域名称")
    domain_desc = fields.CharField(max_length=255, description="域描述")
    domain_type = fields.CharEnumField(DomainType, description="域类型")
    update_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="updated_domains",
        description="更新人",
    )
    create_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="created_domains",
        description="创建人",
    )

    class Meta:
        table = "domains"
        table_description = "域信息"
