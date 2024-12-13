from pydantic import BaseModel, Field
from typing import Optional, Annotated, Any


class ReportBase(BaseModel):
    report_name: str = Field(alias="reportName", description="报告名称")
    report_type: str = Field(alias="reportType", description="报告类型")
    report_desc: Optional[str] = Field(None, alias="reportDesc", description="报告描述")
    report_content: str = Field(alias="reportContent", description="报告内容")
    status: int = Field(alias="status", ge=1, le=2)
    start_date: Optional[str] = Field(None, alias="startDate", description="开始日期")
    end_date: Optional[str] = Field(None, alias="endDate", description="结束日期")
    version: float = Field(default=1.00, alias="version", description="报告版本号")
    view_count: int = Field(default=0, alias="viewCount", description="查看次数")
    collect_count: int = Field(default=0, alias="collectCount", description="收藏次数")
    report_format: str = Field(
        default="PDF", alias="reportFormat", description="报告格式"
    )
    metric: int = Field(alias="metric")
    create_by: Annotated[Any, Field(alias="createBy")] = None


class ReportCreate(ReportBase): ...


class ReportUpdate(BaseModel):
    report_name: Optional[str] = Field(None, description="报告名称")
    report_type: Optional[str] = Field(None, description="报告类型")
    report_desc: Optional[str] = Field(None, description="报告描述")
    report_content: Optional[str] = Field(None, description="报告内容")
    status: Optional[int] = Field(None, description="状态(1或2)", ge=1, le=2)
    start_date: Optional[str] = Field(None, description="开始日期")
    end_date: Optional[str] = Field(None, description="结束日期")
    version: Optional[float] = Field(None, description="报告版本号")
    report_format: Optional[str] = Field(None, description="报告格式")
