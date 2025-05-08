from typing import Optional

from pydantic import BaseModel, Field


class ReportTemplateBase(BaseModel):
    name: str = Field(..., description="模板名称")
    content: str = Field(..., description="模板内容")
    update_by_id: Optional[int] = Field(None, description="更新人", alias="updateById")
    create_by_id: Optional[int] = Field(None, description="创建人", alias="createById")


class ReportTemplateCreate(ReportTemplateBase): ...


class ReportTemplateUpdate(ReportTemplateBase): ...
