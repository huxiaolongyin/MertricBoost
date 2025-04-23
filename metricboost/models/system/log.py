# 支持异步的ORM库
from tortoise import fields

from metricboost.models.base import BaseModel
from metricboost.models.enums import LogDetailType, LogType


class Log(BaseModel):
    id = fields.IntField(primary_key=True, description="日志ID")
    log_type = fields.CharEnumField(LogType, description="日志类型")
    by_user = fields.ForeignKeyField(
        "app_system.User", null=True, on_delete=fields.CASCADE, description="操作人"
    )
    api_log = fields.ForeignKeyField(
        "app_system.APILog", null=True, on_delete=fields.SET_NULL, description="API日志"
    )
    log_detail_type = fields.CharEnumField(
        LogDetailType, null=True, description="日志详情类型"
    )
    log_detail = fields.TextField(null=True, description="日志详情")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "logs"


class APILog(BaseModel):
    id = fields.IntField(primary_key=True, description="API日志ID")
    ip_address = fields.CharField(max_length=60, description="IP地址")
    user_agent = fields.CharField(max_length=800, description="User-Agent")
    request_url = fields.CharField(max_length=255, description="请求URL")
    request_params = fields.JSONField(null=True, description="请求参数")
    request_data = fields.JSONField(null=True, description="请求数据")
    response_data = fields.JSONField(null=True, description="响应数据")
    response_code = fields.CharField(max_length=6, null=True, description="响应业务码")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    process_time = fields.FloatField(null=True, description="请求处理时间")

    class Meta:
        table = "api_logs"
