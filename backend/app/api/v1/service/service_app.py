from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.schemas.base import SuccessExtra, Success, Error
from app.controllers import service_app_controller
from app.models.system import LogType, LogDetailType, User
from app.api.v1.utils import insert_log
from app.schemas.service_app import ServiceAppCreate, ServiceAppUpdate

router = APIRouter()

@router.get("/app", summary="获取应用列表")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    appName: str = Query(None, description="应用名称"),
    appStatus: str = Query(None, description="应用状态"),
    createBy: str = Query(None, description="创建人"),
    userName: str = Query(None, description="用户名"),
    ):
    user = await User.get_or_none(user_name=userName)
    if not user:
        return Error(msg="用户不存在")
    q = Q()
    if appName:
        q &= Q(app_name__contains=appName)
    if appStatus:
        q &= Q(app_status__contains=appStatus)  
    if createBy:
        q &= Q(create_by__user_name=createBy)
    total, app_objs = await service_app_controller.get_app_list(
        page=current, page_size=size, search=q,
    )
    data = {"records": [await app_obj.to_dict() for app_obj in app_objs]}
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.ServiceAppGet,
        by_user_id=user.id,
    )
    return SuccessExtra(code=LogDetailType.ServiceAppGet.value, data=data, total=total, current=current, size=size)

@router.post("/app", summary="创建应用")
async def _(
    app_in: ServiceAppCreate,
):
    app_obj = await service_app_controller.create(app_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.ServiceAppCreate,
        by_user_id=app_obj.create_by.id,
    )
    return Success(code=LogDetailType.ServiceAppCreate.value, msg="创建成功", data={"create_id": app_obj.id})

@router.put("/app/{id}", summary="更新应用")
async def _(
    id: int,
    app_in: ServiceAppUpdate,
):
    app_obj = await service_app_controller.update(id, app_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.ServiceAppUpdate,
        by_user_id=app_obj.create_by.id,
    )
    return Success(code=LogDetailType.ServiceAppUpdate.value, msg="更新成功", data={"update_id": app_obj.id})

@router.delete("/app/{id}", summary="删除应用")
async def _(id: int, userName: str = Query(None, description="用户名")):
    user = await User.get_or_none(user_name=userName)
    if not user:
        return Error(msg="用户不存在")
    await service_app_controller.remove(id)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.ServiceAppDelete,
        by_user_id=user.id)
    return Success(code=LogDetailType.ServiceAppDelete.value, msg="删除成功", data={"delete_id": id})