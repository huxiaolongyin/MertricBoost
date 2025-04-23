from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from metricboost.models.enums import StatusType


class BaseApi(BaseModel):
    # path: Annotated[str | None, Field(title="请求路径", description="/api/v1/auth/login")]
    # method: Annotated[str | None, Field(title="请求方法", description="GET")]
    path: Optional[str] = Field(
        default=None, title="请求路径", description="/api/v1/auth/login"
    )
    method: Optional[str] = Field(title="请求方法", description="GET")
    summary: Optional[str] = Field(title="API简介", default=None)
    tags: Optional[str | List[str]] = Field(title="API标签", default=None)
    status: Optional[StatusType] = Field(title="状态", default=None)

    model_config = ConfigDict(allow_extra=True, populate_by_name=True)


class ApiSearch(BaseApi):
    page: Optional[int] = Field(title="页码", default=1)
    size: Optional[int] = Field(title="每页数量", default=1)


class ApiCreate(BaseApi):
    path: str = Field(
        default_factory=str, title="请求路径", description="/api/v1/auth/login"
    )
    method: str = Field(default_factory=str, title="请求方法", description="GET")


class ApiUpdate(BaseApi): ...
