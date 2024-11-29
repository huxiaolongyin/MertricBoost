from pydantic import BaseModel, Field
from typing import Annotated


class TagBase(BaseModel):
    tag_name: str = Field(..., description="标签名称", alias="tagName")
    tag_type: str = Field(..., description="标签类型", alias="tagType")
    tag_desc: str = Field(..., description="标签描述", alias="tagDesc")
    create_by: Annotated[str, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    class Config:
        populate_by_name = True


class TagCreate(TagBase): ...


class TagUpdate(TagBase): ...


class MetricTagBase(BaseModel):
    metric_id: Annotated[int, Field(alias="metricId")] = None
    tag_id: Annotated[int, Field(alias="tagId")] = None
    create_by: Annotated[str, Field(alias="createBy")] = None

    class Config:
        populate_by_name = True


class MetricTagCreate(MetricTagBase): ...


class MetricTagUpdate(MetricTagBase): ...
