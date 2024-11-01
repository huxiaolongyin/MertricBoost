from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.schemas.base import SuccessExtra, Success
from app.controllers import (
    topic_domain_controller,
    data_domain_controller,
)
from app.models.system import LogType, LogDetailType, User
from app.api.v1.utils import insert_log
from app.schemas.topic import (
    TopicDomainCreate,
    TopicDomainUpdate,
    DataDomainCreate,
    DataDomainUpdate,
)

router = APIRouter()


@router.get("/data-domain", summary="获取数据域信息")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    createBy: str = Query(None, description="创建人"),
):

    q = Q()  # Q() 是一个查询构造器，用于构建复杂的数据库查询条件
    if createBy:
        user = await User.get_or_none(user_name=createBy)
        if user:
            q &= Q(create_by_id=user.id)
        else:
            q &= Q(create_by_id=None)  # 使用 &= 运算符来添加条件，相当于 AND 操作
    total, data_domain_objs = await data_domain_controller.list(
        page=current,
        page_size=size,
        search=q,
        order=["id"],
    )
    records = [await data_domain_obj.to_dict() for data_domain_obj in data_domain_objs]
    data = {"records": records}
    await insert_log(LogType.SystemLog, LogDetailType.DataDomainGet, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.post("/data-domain", summary="创建数据域信息")
async def _(
    data_domain_in: DataDomainCreate,
):
    new_database = await data_domain_controller.create(obj_in=data_domain_in)

    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataDomainCreate,
        by_user_id=0,
    )
    return Success(msg="创建成功", data={"create_id": new_database.id})


@router.patch("/data-domain/{id}", summary="更新数据域信息")
async def _(
    id: int,
    data_domain_in: DataDomainUpdate,
):
    await data_domain_controller.update(id=id, obj_in=data_domain_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataDomainUpdate,
        by_user_id=0,
    )
    return Success(msg="更新成功", data={"update_id": id})


@router.delete("/data-domain/{id}", summary="删除数据域信息")
async def _(
    id: int,
):
    await data_domain_controller.remove(id=id)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataDomainDelete,
        by_user_id=0,
    )
    return Success(msg="删除成功", data={"delete_id": id})


@router.get("/topic-domain", summary="获取主题域信息")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    createBy: str = Query(None, description="创建人"),
):
    # Q() 是一个查询构造器，用于构建复杂的数据库查询条件
    q = Q()
    # 使用 &= 运算符来添加条件，相当于 AND 操作
    if createBy:
        user = await User.get_or_none(user_name=createBy)
        if user:
            q &= Q(create_by_id=user.id)
        else:
            q &= Q(create_by_id=None)  # 使用 &= 运算符来添加条件，相当于 AND 操作
    total, topic_domain_objs = await topic_domain_controller.list(
        page=current,
        page_size=size,
        search=q,
        order=["id"],
    )
    records = [
        await topic_domain_obj.to_dict() for topic_domain_obj in topic_domain_objs
    ]
    data = {"records": records}
    await insert_log(LogType.SystemLog, LogDetailType.TopicDomainGet, by_user_id=0)
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.post("/topic-domain", summary="创建主题域信息")
async def _(
    topic_domain_in: TopicDomainCreate,
):
    new_database = await topic_domain_controller.create(obj_in=topic_domain_in)

    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.TopicDomainCreate,
        by_user_id=0,
    )
    return Success(msg="创建成功", data={"create_id": new_database.id})


@router.patch("/topic-domain/{id}", summary="更新主题域信息")
async def _(
    id: int,
    topic_domain_in: TopicDomainUpdate,
):
    await topic_domain_controller.update(id=id, obj_in=topic_domain_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.TopicDomainUpdate,
        by_user_id=0,
    )
    return Success(msg="更新成功", data={"update_id": id})


@router.delete("/topic-domain/{id}", summary="删除主题域信息")
async def _(
    id: int,
):
    await topic_domain_controller.remove(id=id)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.TopicDomainDelete,
        by_user_id=0,
    )
    return Success(msg="删除成功", data={"delete_id": id})
