from typing import Annotated, Union
from pydantic import BaseModel, Field
from app.models.system import StatusType


class ServiceAppBase(BaseModel):
    app_name: str = Field(alias="appName")
    app_desc: str = Field(alias="appDesc")
    status: Annotated[StatusType | None, Field(alias="status")] = StatusType.enable
    create_by: Annotated[Union[str, int], Field(alias="createBy")] = None


class ServiceAppCreate(ServiceAppBase): ...


class ServiceAppUpdate(ServiceAppBase): ...
