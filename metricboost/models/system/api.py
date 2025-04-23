from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import MethodType, StatusType


class Api(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True, description="API ID")
    path = fields.CharField(max_length=100, description="API路径")
    method = fields.CharEnumField(MethodType, description="请求方法")
    summary = fields.CharField(max_length=500, description="请求简介")
    tags = fields.JSONField(max_length=500, description="API标签")
    status = fields.CharEnumField(
        enum_type=StatusType, default=StatusType.enable, description="状态"
    )

    class Meta:
        table = "apis"
