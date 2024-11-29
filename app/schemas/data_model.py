from typing import Annotated
from pydantic import BaseModel, Field
from app.models.system import StatusType


class DataModelBase(BaseModel):
    database: Annotated[int, Field(alias="database")] = None
    table_name: Annotated[str, Field(alias="tableName")] = None
    data_model_name: str = Field(alias="dataModelName")
    data_model_desc: str = Field(alias="dataModelDesc")
    data_domain: Annotated[int, Field(alias="dataDomain")] = None
    topic_domain: Annotated[int, Field(alias="topicDomain")] = None
    status: Annotated[StatusType | None, Field()] = StatusType.enable
    field_conf: Annotated[str, Field(alias="fieldConf")] = None
    create_by: Annotated[str, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    class Config:
        populate_by_name = True


class DataModelCreate(DataModelBase): ...


class DataModelUpdate(DataModelBase): ...
