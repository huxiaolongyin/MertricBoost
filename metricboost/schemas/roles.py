from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from metricboost.models.enums import Sensitivity, StatusType


class RoleBase(BaseModel):
    role_name: str = Field(alias="roleName", description="角色名称")
    role_code: str = Field(alias="roleCode", description="角色编码")
    role_desc: Annotated[
        str | None, Field(alias="roleDesc", description="角色描述")
    ] = None
    role_home: Annotated[
        str | None, Field(alias="roleHome", description="角色首页")
    ] = None
    status: Annotated[StatusType | None, Field(alias="status")] = None
    sensitivity: Annotated[Sensitivity | None, Field(alias="sensitivity")] = None
    domainIds: Annotated[list[int | str] | None, Field(alias="domainIds")] = None

    model_config = ConfigDict(allow_extra=True, populate_by_name=True)


class RoleCreate(RoleBase): ...


class RoleUpdate(RoleBase): ...


class RoleUpdateAuthrization(BaseModel):
    role_home: Annotated[
        str | None, Field(alias="roleHome", description="角色首页")
    ] = None
    menu_ids: Annotated[
        list[int] | None, Field(alias="menuIds", description="菜单id列表")
    ] = None
    api_ids: Annotated[
        list[int] | None, Field(alias="apiIds", description="API id列表")
    ] = None
    button_ids: Annotated[
        list[int] | None, Field(alias="buttonIds", description="按钮id列表")
    ] = None
    domain_ids: Annotated[
        list[int] | None, Field(alias="domainIds", description="域id列表")
    ] = None
