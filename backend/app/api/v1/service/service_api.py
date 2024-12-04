from tortoise.expressions import Q
from fastapi import APIRouter, Query
from app.schemas.base import SuccessExtra, Success, Error
from app.schemas.service_api import ServiceApiCreate
from app.controllers.service_api import ServiceApiController

router = APIRouter()

@router.get("/api", summary="获取指标发布分享列表")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    apiStatus: str = Query(None, description="api状态"),
    apiName: str = Query(None, description="api名称"),
    apiMethod: str = Query(None, description="api类型"),
    createBy: str = Query(None, description="创建人"),
    ):
    q = Q()
    if apiStatus:
        q &= Q(api_status__contains=apiStatus)
    if apiName:
        q &= Q(api_name__contains=apiName)
    if apiMethod:
        q &= Q(api_method__contains=apiMethod)
    if createBy:
        q &= Q(create_by__user_name=createBy)
    
    total, service_api_objs = await ServiceApiController().get_api_list(page=current, page_size=size, search=q)

    # 去除不需要的字段，增加额外字段
    records = []
    for item in service_api_objs:
        api_dict = await item.to_dict(exclude_fields=["create_by_id"])
        api_dict.update({
            "createBy": item.create_by.user_name,
            "appName": item.app.app_name
        })
        records.append(api_dict)
    data = {"records":records}

    return SuccessExtra(msg="获取成功", data=data, total=total)

@router.get("/api/{id}", summary="获取指标发布分享详情")
async def _(id: int):
    api_detail = await ServiceApiController().get_api_detail(api_id=id)
    # 去除不需要的字段，增加额外字段
    api_dict = await api_detail.to_dict(exclude_fields=["create_by_id"])
    api_dict.update({
            "createBy": api_detail.create_by.user_name,
            "appName": api_detail.app.app_name,
            "params": [await param.to_dict(exclude_fields=["id","api_id"]) for param in api_detail.params]
            })
    data = {"records":api_dict}

    return Success(msg="获取成功", data=data)

@router.post("/api", summary="创建指标发布分享")
async def _(metric_api_in: ServiceApiCreate):
    new_metric_api = await ServiceApiController().create(obj_in=metric_api_in)

    return Success(msg="创建成功", data={"create_id": new_metric_api.id})

@router.patch("/api/{id}", summary="更新指标发布分享")
async def _(id: int, metric_api_in: ServiceApiCreate):
    await ServiceApiController().update(id=id, obj_in=metric_api_in)
    return Success(msg="更新成功", data={"update_id": id})

@router.delete("/api/{id}", summary="删除指标发布分享")
async def _(id: int):
    await ServiceApiController().remove(id=id)
    return Success(msg="删除成功", data={"delete_id": id})