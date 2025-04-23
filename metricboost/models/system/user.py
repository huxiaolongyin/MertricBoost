from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import GenderType, StatusType


class User(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True, description="用户ID")
    user_name = fields.CharField(max_length=20, unique=True, description="用户名称")
    password = fields.CharField(max_length=128, description="密码")
    nick_name = fields.CharField(max_length=30, null=True, description="昵称")
    user_gender = fields.CharEnumField(
        enum_type=GenderType, default=GenderType.unknown, description="性别"
    )
    user_email = fields.CharField(max_length=255, null=True, description="邮箱")
    user_phone = fields.CharField(max_length=20, null=True, description="电话")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")
    roles = fields.ManyToManyField("app_system.Role", related_name="user_roles")
    status = fields.CharEnumField(
        enum_type=StatusType, default=StatusType.enable, description="状态"
    )

    class Meta:
        table = "users"
