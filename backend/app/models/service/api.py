# 支持异步的ORM库
from tortoise import fields
from app.models.utils import (
    BaseModel,
    TimestampMixin,
)

class ServiceApi(BaseModel, TimestampMixin):
    id = fields.IntField(pk=True)
    api_name = fields.CharField(max_length=50, unique=True, description="API名称")
    api_path = fields.CharField(max_length=255, description="API地址")
    api_desc = fields.CharField(max_length=255, description="API描述")
    api_method = fields.CharField(max_length=10, description="API请求方法")
    api_status = fields.IntField(default=2, description="API状态(1启用，2非启用)")
   
    # 定义外键关系
    app = fields.ForeignKeyField(
        "app_system.ServiceApp",
        related_name="apis",
        description="应用"
    )
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_apis", description="创建人"
    )

    class Meta:
        table = "service_apis"
        table_description = "指标发布API"

class ServiceApiParam(BaseModel, TimestampMixin):
    id = fields.IntField(pk=True)
    param_name = fields.CharField(max_length=50, unique=True, description="参数名称")
    param_type = fields.CharField(max_length=50, description="参数类型")
    param_desc = fields.CharField(max_length=255, description="参数描述")
    param_required = fields.IntField(default=2,  description="参数是否必填(1必填，2非必填)")
    param_default = fields.CharField(max_length=255, description="参数默认值")
    param_example = fields.CharField(max_length=255, description="参数示例")
    # 定义外键关系
    api = fields.ForeignKeyField(
        "app_system.ServiceApi",
        related_name="params",
        description="API"
    )
    class Meta:
        table = "service_apis_params"
        table_description = "指标发布API参数"
