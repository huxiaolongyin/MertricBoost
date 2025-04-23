from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class DomainBase(BaseModel):
    """数据域信息"""

    domain_name: str = Field(..., description="域名称", alias="domainName")
    domain_desc: Optional[str] = Field(None, description="域描述", alias="domainDesc")
    domain_type: str = Field(..., description="域类型", alias="domainType")
    create_by_id: Optional[Any] = Field(None, description="创建者", alias="createById")
    update_by_id: Optional[Any] = Field(None, description="更新者", alias="updateById")

    model_config = ConfigDict(populate_by_name=True)


class DomainCreate(DomainBase): ...


class DomainUpdate(DomainBase):
    domain_name: Optional[str] = Field(None, description="域名称", alias="domainName")
    domain_type: Optional[str] = Field(None, description="域类型", alias="domainType")


class DomainResponse(DomainBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
