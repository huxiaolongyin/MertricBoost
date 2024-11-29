from typing import Annotated
from pydantic import BaseModel, Field


class DomainBase(BaseModel):
    """数据域/主题域信息"""

    domain_name: str = Field(alias="domainName")
    domain_desc: str = Field(alias="domainDesc")
    create_by: Annotated[str, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    class Config:
        populate_by_name = True


class DomainCreate(DomainBase): ...


class DomainUpdate(DomainBase): ...
