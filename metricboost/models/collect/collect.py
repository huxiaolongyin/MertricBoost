from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import CollectType, StatusType


class Collect(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, description="采集任务名称")
    type = fields.CharEnumField(
        CollectType, description="采集类型", default=CollectType.BATCH
    )
    schedule = fields.CharField(max_length=100, description="Cron调度表达式", null=True)
    origin_database = fields.ForeignKeyField(
        "app_system.Database",
        related_name="collect_origin_databases",
        description="来源数据库",
    )
    origin_table = fields.CharField(max_length=100, description="来源表名")
    target_database = fields.ForeignKeyField(
        "app_system.Database",
        related_name="collect_target_databases",
        description="目标数据库",
    )
    target_table = fields.CharField(max_length=100, description="目标表名")
    status = fields.CharEnumField(
        StatusType, description="状态", default=StatusType.disable
    )
    update_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="updated_collects",
        description="更新人",
    )
    create_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="created_collects",
        description="创建人",
    )

    class Meta:
        table = "collects"
        table_description = "数据采集任务表"
