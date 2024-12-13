from typing import Annotated, Any
from pydantic import BaseModel, Field, ConfigDict


class DomainBase(BaseModel):
    """数据域/主题域信息"""

    domain_name: str = Field(alias="domainName")
    domain_desc: str = Field(alias="domainDesc")
    create_by: Annotated[Any, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    model_config = ConfigDict(populate_by_name=True)


class DomainCreate(DomainBase): ...


class DomainUpdate(DomainBase): ...
