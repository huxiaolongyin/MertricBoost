from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin


class ReportTemplate(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, description="模板名称")
    content = fields.TextField(description="模板内容", null=True)
    # 更新人
    update_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="updated_report_templates",
        description="更新人",
    )
    create_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="created_report_templates",
        description="创建人",
    )

    class Meta:
        table = "report_templates"
        table_description = "报告模板"
