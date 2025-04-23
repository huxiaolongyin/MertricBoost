from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    tag_name: str = Field(..., description="标签名称", alias="tagName")
    tag_type: Optional[str] = Field(None, description="标签类型", alias="tagType")
    tag_desc: Optional[str] = Field(None, description="标签描述", alias="tagDesc")
    update_by_id: Optional[int] = Field(
        None, description="更新人ID", alias="updateById"
    )
    create_by_id: Optional[int] = Field(
        None, description="创建人ID", alias="createById"
    )
    model_config = ConfigDict(populate_by_name=True)


class TagCreate(TagBase): ...


class TagUpdate(TagBase):
    tag_name: Optional[str] = Field(None, description="标签名称", alias="tagName")
    tag_type: Optional[str] = Field(None, description="标签类型", alias="tagType")
    tag_desc: Optional[str] = Field(None, description="标签描述", alias="tagDesc")


class TagResponse(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MetricTagLink(BaseModel):
    metric_id: int = Field(..., description="指标ID", alias="metricId")
    tag_id: int = Field(..., description="标签ID", alias="tagId")

    model_config = ConfigDict(populate_by_name=True)
