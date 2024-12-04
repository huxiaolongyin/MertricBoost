from fastapi import APIRouter, Query
from app.controllers import tag_controller, metric_tag_controller
from tortoise.expressions import Q
from app.schemas.base import SuccessExtra, Success, Fail
from app.schemas.tag import TagCreate, TagUpdate, MetricTagCreate, MetricTagUpdate
from app.models.system import LogType, LogDetailType
from app.api.v1.utils import insert_log
from typing import List

router = APIRouter()


@router.get("/tag", summary="获取标签信息")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    createBy: str = Query(None, description="创建人"),
):
    q = Q()
    if createBy:
        q &= Q(create_by__user_name=createBy)
    total, tag_objs = await tag_controller.list(
        page=current, page_size=size, search=q, order=["id"]
    )
    records = []
    for tag_obj in tag_objs:
        # 构建基础数据字典
        tag_dict = await tag_obj.to_dict()
        # 获取用户关联数据
        create_by = await tag_obj.create_by
        tag_dict.update({"createBy": create_by.user_name})
        records.append(tag_dict)

    data = {"records": records}
    await insert_log(LogType.SystemLog, LogDetailType.TagGet, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.post("/tag", summary="创建标签信息")
async def _(tag_in: TagCreate):
    new_tag = await tag_controller.create(obj_in=tag_in)
    await insert_log(LogType.SystemLog, LogDetailType.TagCreate, by_user_id=0)
    return Success(msg="创建成功", data={"create_id": new_tag.id})


@router.patch("/tag/{tag_id}", summary="更新标签信息")
async def _(tag_id: int, tag_in: TagUpdate):
    await tag_controller.update(tag_id=tag_id, obj_in=tag_in)
    await insert_log(LogType.SystemLog, LogDetailType.TagUpdate, by_user_id=0)
    return Success(msg="更新成功", data={"update_id": tag_id})


@router.delete("/tag/{tag_id}", summary="删除标签信息")
async def _(tag_id: int):
    # 如果存在标签指标关联，则不允许删除
    metric_tag_objs = await metric_tag_controller.list(metric_ids=[tag_id])
    if metric_tag_objs:
        return Fail(msg="存在标签指标关联，不允许删除")
    await tag_controller.remove(tag_id=tag_id)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.TagDelete,
        by_user_id=0,
    )
    return Success(msg="删除成功", data={"delete_id": tag_id})


@router.get("/metric-tag", summary="获取标签指标信息")
async def _(
    metric_ids: List[int] = Query(None),
):
    total, metric_tag_objs = await metric_tag_controller.list(metric_ids)

    data = {"records": metric_tag_objs}
    await insert_log(LogType.SystemLog, LogDetailType.MetricTagGet, by_user_id=0)
    return SuccessExtra(total=total, data=data)


@router.post("/metric-tag", summary="创建标签指标信息")
async def _(metric_tag_in: MetricTagCreate):
    new_metric_tag = await metric_tag_controller.create(obj_in=metric_tag_in)
    await insert_log(LogType.SystemLog, LogDetailType.MetricTagCreate, by_user_id=0)
    return Success(msg="创建成功", data={"create_id": new_metric_tag.id})


@router.delete("/metric-tag", summary="删除标签指标信息")
async def _(metricId: int, tag: str):
    await metric_tag_controller.remove(metric_id=metricId, tag=tag)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.MetricTagDelete,
        by_user_id=0,
    )
    return Success(
        msg="删除成功", data={"delete_id": f"指标id[{metricId}]，标签[{tag}]"}
    )
