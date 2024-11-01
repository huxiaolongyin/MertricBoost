from typing import Annotated
from pydantic import BaseModel, Field


class DataDomainBase(BaseModel):
    """数据域信息"""

    data_domain_name: str = Field(alias="dataDomainName")
    data_domain_description: str = Field(alias="dataDomainDescription")
    create_by: Annotated[str, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    class Config:
        populate_by_name = True


class DataDomainCreate(DataDomainBase): ...


class DataDomainUpdate(DataDomainBase): ...


class TopicDomainBase(BaseModel):
    """主题域信息"""

    topic_domain_name: str = Field(alias="topicDomainName")
    topic_domain_description: str = Field(alias="topicDomainDescription")
    create_by: Annotated[str, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    class Config:
        populate_by_name = True


class TopicDomainCreate(TopicDomainBase): ...


class TopicDomainUpdate(TopicDomainBase): ...
