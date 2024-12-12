from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.system import GenderType, StatusType


class UserBase(BaseModel):
    user_name: str = Field(alias="userName")
    password: str = Field()
    user_email: EmailStr = Field(alias="userEmail")
    user_gender: Annotated[GenderType | None, Field(alias="userGender")] = (
        GenderType.male
    )
    nick_name: Annotated[str | None, Field(alias="nickName")] = None
    user_phone: Annotated[str | None, Field(alias="userPhone")] = None
    roles: Annotated[list[str] | None, Field(alias="userRoles")] = []
    status: Annotated[StatusType | None, Field()] = StatusType.enable

    model_config = ConfigDict(allow_extra=True, populate_by_name=True)


class UserCreate(UserBase): ...


class UserUpdate(UserBase):
    password: Annotated[str | None, Field()] = None


class UpdatePassword(BaseModel):
    old_password: str = Field(alias="oldPassword")
    new_password: str = Field(alias="newPassword")

    model_config = ConfigDict(allow_extra=True, populate_by_name=True)
