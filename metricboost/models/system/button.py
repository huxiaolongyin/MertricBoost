from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import StatusType


class Button(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True, description="菜单ID")
    button_code = fields.CharField(max_length=200, description="按钮编码")
    button_desc = fields.CharField(max_length=200, description="按钮描述", null=True)
    status = fields.CharEnumField(
        enum_type=StatusType, default=StatusType.enable, description="状态"
    )

    class Meta:
        table = "buttons"
