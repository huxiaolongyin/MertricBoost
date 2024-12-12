# 支持异步的ORM库
from tortoise import fields
from app.models.utils import (
    BaseModel,
    TimestampMixin,
)


class Report(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True)
    report_name = fields.CharField(max_length=100, description="报告名称")
    report_type = fields.CharField(max_length=100, description="报告类型")
    report_content = fields.TextField(description="报告内容")
    metric_data = fields.JSONField(description="指标数据")
    metric = fields.ForeignKeyField(
        "app_system.Metric",
        related_name="reports",
        description="指标",
    )
    create_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="created_reports",
        description="创建人",
    )

    class Meta:
        table = "reports"
        table_description = "报告"
