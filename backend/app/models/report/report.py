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
    report_desc = fields.CharField(max_length=255, description="报告描述", null=True)
    report_content = fields.TextField(description="报告内容")
    status = fields.IntField(description="状态(1或2)")
    start_date = fields.DateField(description="开始日期", null=True)
    end_date = fields.DateField(description="结束日期", null=True)
    version = fields.FloatField(description="报告版本号", default=1.00)
    view_count = fields.IntField(description="查看次数", default=0)
    collect_count = fields.IntField(description="收藏次数", default=0)
    report_format = fields.CharField(
        max_length=20, description="报告格式", default="PDF"
    )
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
