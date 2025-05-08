from typing import Optional

from pydantic import BaseModel, Field

from metricboost.models.enums import ReportStatus


class ReportBase(BaseModel):
    name: str = Field(..., description="报告名称")
    description: Optional[str] = Field(None, description="报告描述")
    statistic_date: Optional[str] = Field(
        None, description="统计日期", alias="statisticDate"
    )
    statistical_period: Optional[str] = Field(
        None, description="统计周期", alias="statisticalPeriod"
    )
    status: Optional[ReportStatus] = Field(
        ReportStatus.PROCESSING, description="报告状态"
    )
    # error_message: Optional[str] = Field(
    #     None, description="错误信息", alias="errorMessage"
    # )
    # origin_data: Optional[str] = Field(None, description="原始数据", alias="originData")
    # content: Optional[str] = Field(None, description="报告内容")
    model_name: Optional[str] = Field(None, description="大模型名称", alias="modelName")
    metric_id: int = Field(..., description="指标ID", alias="metricId")
    report_template_id: int = Field(..., description="模板ID", alias="reportTemplateId")
    update_by_id: Optional[int] = Field(None, description="更新人", alias="updateById")
    create_by_id: Optional[int] = Field(None, description="创建人", alias="createById")


class ReportCreate(ReportBase): ...


class ReportUpdate(ReportBase): ...
