from typing import Annotated, Any
from pydantic import BaseModel, Field, ConfigDict
from app.models.system import StatusType


class DatabaseBase(BaseModel):
    database_name: str = Field(alias="databaseName")
    database_type: str = Field(alias="databaseType")
    database_host: str = Field(alias="databaseHost")
    database_port: int = Field(alias="databasePort")
    database_user: str = Field(alias="databaseUser")
    password: str = Field(alias="password")
    database_database: str = Field(alias="databaseDatabase")
    status: Annotated[StatusType | None, Field()] = StatusType.enable
    database_description: Annotated[str | None, Field()] = None
    create_by: Annotated[Any, Field(alias="createBy")] = None

    # 允许原始名称和别名来访问和设置字段值
    model_config = ConfigDict(populate_by_name=True)


class DatabaseCreate(DatabaseBase): ...


class DatabaseUpdate(DatabaseBase):
    password: Annotated[str | None, Field()] = None


class UpdatePassword(BaseModel):
    old_password: str = Field(alias="oldPassword")
    new_password: str = Field(alias="newPassword")

    model_config = ConfigDict(populate_by_name=True)
