from typing import Annotated
from pydantic import BaseModel, Field
from app.models.system import StatusType


class DataModelBase(BaseModel):
    data_model_name: str = Field(alias="dataModelName")
    data_model_desc: str = Field(alias="dataModelDesc")
    status: Annotated[StatusType | None, Field()] = StatusType.enable
    sql_content: str = Field(alias="sqlContent")
    data_domain: Annotated[str, Field(alias="dataDomain")] = None
    topic_domain: Annotated[str, Field(alias="topicDomain")] = None
    database: Annotated[str, Field(alias="database")] = None
    create_by: Annotated[str, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    class Config:
        populate_by_name = True


class DataModelCreate(DataModelBase): ...


class DataModelUpdate(DataModelBase): ...
