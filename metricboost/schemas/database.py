from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

# from metricboost.models.system import User


class DatabaseBase(BaseModel):
    name: str = Field(..., description="数据库名称")
    type: str = Field(..., description="数据库类型")
    host: str = Field(..., description="数据库主机")
    port: int = Field(..., description="数据库端口")
    username: Optional[str] = Field(None, description="数据库用户")
    password: Optional[str] = Field(None, description="数据库密码")
    database: Optional[str] = Field(None, description="选用的数据库")
    status: str = Field("1", description="数据库状态，1启用，0禁用")
    description: Optional[str] = Field(None, description="数据库描述")
    update_by_id: Optional[int] = Field(None, description="更新者", alias="updateById")
    create_by_id: Optional[int] = Field(None, description="创建者", alias="createById")
    model_config = ConfigDict(populate_by_name=True)


class DatabaseCreate(DatabaseBase): ...


class DatabaseUpdate(DatabaseBase):
    name: Optional[str] = Field(None, description="数据库名称")
    type: Optional[str] = Field(None, description="数据库类型")
    host: Optional[str] = Field(None, description="数据库主机")
    port: Optional[int] = Field(None, description="数据库端口")
    status: Optional[str] = Field(None, description="数据库状态，1启用，0禁用")


class DatabaseResponse(DatabaseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdatePassword(BaseModel):
    old_password: str = Field(..., alias="oldPassword")
    new_password: str = Field(..., alias="newPassword")

    model_config = ConfigDict(populate_by_name=True)
