from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import ReportStatus, StatisticalPeriod


class Report(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, description="报告名称")
    description = fields.CharField(max_length=500, description="报告描述", null=True)
    statistic_date = fields.DateField(description="统计日期范围", null=True)
    statistical_period = fields.CharEnumField(
        StatisticalPeriod, description="统计周期", null=True
    )
    status = fields.CharEnumField(
        ReportStatus, default=ReportStatus.PROCESSING, description="报告状态"
    )
    # 错误信息
    error_message = fields.TextField(description="失败时的错误信息", null=True)
    # 原数据
    origin_data = fields.TextField(description="原始数据", null=True)
    content = fields.TextField(description="报告内容", null=True)
    # 使用的大模型名称
    model_name = fields.CharField(
        max_length=100, description="使用的大模型名称", null=True
    )

    metric = fields.ForeignKeyField(
        "app_system.Metric",
        related_name="reports",
        description="关联的指标",
    )
    # 报告模板
    report_template = fields.ForeignKeyField(
        "app_system.ReportTemplate",
        related_name="report_templates",
        description="关联的报告模板",
    )
    # 更新人
    update_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="updated_reports",
        description="更新人",
    )
    create_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="created_reports",
        description="创建人",
    )

    class Meta:
        table = "reports"
        table_description = "智能报告信息"
