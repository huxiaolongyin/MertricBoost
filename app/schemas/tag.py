from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., description="标签名称")
    type: str = Field(..., description="标签类型")
    description: str = Field(..., description="标签描述")


class TagCreate(TagBase): ...


class TagUpdate(TagBase): ...
