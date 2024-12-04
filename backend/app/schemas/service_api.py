from typing import Annotated
from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.system import StatusType


class ServiceApiParamBase(BaseModel):
    param_name: str = Field(alias="paramName")
    param_type: str = Field(alias="paramType")
    param_desc: str = Field(alias="paramDesc")
    param_required: int = Field(alias="paramRequired")
    param_default: str = Field(alias="paramDefault")
    param_example: str = Field(alias="paramExample")

class ServiceApiParamCreate(ServiceApiParamBase): ...

class ServiceApiParamUpdate(ServiceApiParamBase): ...

class ServiceApiBase(BaseModel):
    api_name: str = Field(alias="apiName")
    api_path: str = Field(alias="apiPath")  
    api_desc: str = Field(alias="apiDesc")
    api_method: str = Field(alias="apiMethod")
    api_status: Annotated[StatusType | None, Field(alias="apiStatus")] = StatusType.enable
    create_by: Annotated[str, Field(alias="createBy")] = None
    app_id: int = Field(alias="appId")

class ServiceApiCreate(ServiceApiBase): 
    params: List[ServiceApiParamCreate] = []

class ServiceApiUpdate(ServiceApiBase): ...