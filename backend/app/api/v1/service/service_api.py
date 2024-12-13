from tortoise.expressions import Q
from fastapi import APIRouter, Query, Body
from app.schemas.base import SuccessExtra, Success, Error
from app.schemas.service_api import ServiceApiCreate
from app.controllers.service_api import service_api_controller

router = APIRouter()


@router.get("/apis", summary="获取指标发布分享列表")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    status: str = Query(None, description="api状态"),
    apiName: str = Query(None, description="api名称"),
    apiMethod: str = Query(None, description="api类型"),
    createBy: str = Query(None, description="创建人"),
):
    q = Q()
    if status:
        q &= Q(status__contains=status)
    if apiName:
        q &= Q(api_name__contains=apiName)
    if apiMethod:
        q &= Q(api_method=apiMethod)
    if createBy:
        q &= Q(create_by__user_name=createBy)

    total, service_api_objs = await service_api_controller.get_list(
        page=current,
        page_size=size,
        search=q,
        prefetch=["create_by", "metric", "app"],
    )

    # 去除不需要的字段，增加额外字段
    records = []
    for item in service_api_objs:
        api_dict = await item.to_dict(exclude_fields=["create_by_id"])
        api_dict.update(
            {
                "createBy": item.create_by.user_name,
                "appName": item.app.app_name,
                "metricName": item.metric.chinese_name,
            }
        )
        records.append(api_dict)
    data = {"records": records}

    return SuccessExtra(msg="获取成功", data=data, total=total)


@router.get("/apis/{id}", summary="获取指标发布分享详情")
async def _(id: int):
    api_detail = await service_api_controller.get_api_detail(api_id=id)
    # 去除不需要的字段，增加额外字段
    api_dict = await api_detail.to_dict(exclude_fields=["create_by_id"])
    api_dict.update(
        {
            "createBy": api_detail.create_by.user_name,
            "appName": api_detail.app.app_name,
            "metricName": api_detail.metric.chinese_name,
            "params": [
                await param.to_dict(exclude_fields=["api_id"])
                for param in api_detail.params
            ],
        }
    )
    data = {"records": api_dict}

    return Success(msg="获取成功", data=data)


@router.post("/apis", summary="创建指标发布分享")
async def _(metric_api_in: ServiceApiCreate):
    # 判断API是否已经存在
    api_name = metric_api_in.api_name
    existing_api = await service_api_controller.get_api_by_name(api_name)
    if existing_api:
        return Error(msg="API名称已存在")

    # 判断路径是否已经存在
    api_path = metric_api_in.api_path
    existing_api = await service_api_controller.get_api_by_path(api_path)
    if existing_api:
        return Error(msg="API路径已存在")

    new_metric_api = await service_api_controller.create(obj_in=metric_api_in)

    return Success(msg="创建成功", data={"create_id": new_metric_api.id})


@router.patch("/apis/{id}", summary="更新指标发布分享")
async def _(
    id: int,
    metric_api_in: ServiceApiCreate = Body(description="接口信息"),
):
    await service_api_controller.update(id=id, obj_in=metric_api_in)
    return Success(msg="更新成功", data={"update_id": id})


@router.delete("/apis/{id}", summary="删除指标发布分享")
async def _(id: int):
    await service_api_controller.remove(id=id)
    return Success(msg="删除成功", data={"delete_id": id})
