from typing import Annotated
from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.system import StatusType


class ServiceApiParamBase(BaseModel):
    param_name: str = Field(alias="paramName")
    param_loc: str = Field(alias="paramLoc")
    param_type: str = Field(alias="paramType")
    param_desc: str = Field(alias="paramDesc")
    is_required: int = Field(alias="isRequired")
    default: str = Field(alias="default")
    example: str = Field(alias="example")


class ServiceApiParamCreate(ServiceApiParamBase): ...


class ServiceApiParamUpdate(ServiceApiParamBase): ...


class ServiceApiBase(BaseModel):
    api_name: str = Field(alias="apiName")
    api_path: str = Field(alias="apiPath")
    api_desc: str = Field(alias="apiDesc")
    api_method: str = Field(alias="apiMethod")
    status: Annotated[StatusType | None, Field()] = StatusType.enable
    create_by: Annotated[str, Field(alias="createBy")] = None
    app_id: int = Field(alias="appId")
    metric_id: int = Field(alias="metricId")


class ServiceApiCreate(ServiceApiBase):
    params: List[ServiceApiParamCreate] = []


class ServiceApiUpdate(ServiceApiBase): ...
