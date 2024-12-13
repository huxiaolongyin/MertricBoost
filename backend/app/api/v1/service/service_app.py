from fastapi import APIRouter, Query, Body
from tortoise.expressions import Q
from app.schemas.base import SuccessExtra, Success, Fail
from app.controllers import service_app_controller
from app.models.system import LogType, LogDetailType, User
from app.api.v1.utils import insert_log
from app.schemas.service_app import ServiceAppCreate, ServiceAppUpdate

router = APIRouter()


@router.get("/apps", summary="获取应用列表")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    appName: str = Query(None, description="应用名称"),
    status: str = Query(None, description="应用状态"),
    createBy: str = Query(None, description="创建人"),
    userName: str = Query(None, description="用户名"),
):
    user = await User.get_or_none(user_name=userName)
    if not user:
        return Fail(msg="用户不存在")
    q = Q()
    if appName:
        q &= Q(app_name__contains=appName)
    if status:
        q &= Q(status__contains=status)
    if createBy:
        q &= Q(create_by__user_name=createBy)
    total, app_objs = await service_app_controller.get_app_list(
        page=current,
        page_size=size,
        search=q,
    )
    records = []
    for app_obj in app_objs:
        app_dict = await app_obj.to_dict()
        app_dict["createBy"] = app_obj.create_by.user_name
        records.append(app_dict)

    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.ServiceAppGet,
        by_user_id=user.id,
    )
    return SuccessExtra(
        code=LogDetailType.ServiceAppGet.value,
        data={"records": records},
        total=total,
        current=current,
        size=size,
    )


@router.get("/apps/{id}", summary="获取应用详情")
async def _(
    id: int,
):
    app_obj = await service_app_controller.get(id)
    if not app_obj:
        return Fail(msg="应用不存在")
    apis = await app_obj.apis.all()
    app_dict = await app_obj.to_dict()
    apis = [(api.id, api.api_name) for api in apis]
    app_dict["apis"] = apis

    return Success(
        code=LogDetailType.ServiceAppGet.value,
        data={"records": app_dict},
    )


@router.post("/apps", summary="创建应用")
async def _(
    app_in: ServiceAppCreate,
):
    # 校验应用名称是否重复
    app_obj = await service_app_controller.get_app_by_name(app_in.app_name)
    if app_obj:
        return Fail(msg="应用名称已存在")
    app_obj = await service_app_controller.create(app_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.ServiceAppCreate,
        by_user_id=app_obj.create_by.id,
    )
    return Success(
        code=LogDetailType.ServiceAppCreate.value,
        msg="创建成功",
        data={"create_id": app_obj.id},
    )


@router.patch("/apps/{id}", summary="更新应用")
async def _(
    id: int,
    app_in: ServiceAppUpdate = Body(description="应用信息"),
):
    app_obj = await service_app_controller.update(id, app_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.ServiceAppUpdate,
        by_user_id=app_obj.create_by.id,
    )
    return Success(
        code=LogDetailType.ServiceAppUpdate.value,
        msg="更新成功",
        data={"update_id": app_obj.id},
    )


@router.delete("/apps/{id}", summary="删除应用")
async def _(
    id: int,
    # userName: str = Query(None, description="用户名"),
):
    # user = await User.get_or_none(user_name=userName)
    # if not user:
    #     return Fail(msg="用户不存在")
    await service_app_controller.remove(id)
    # await insert_log(
    #     log_type=LogType.SystemLog,
    #     log_detail_type=LogDetailType.ServiceAppDelete,
    #     by_user_id=user.id,
    # )
    return Success(
        code=LogDetailType.ServiceAppDelete.value,
        msg="删除成功",
        data={"delete_id": id},
    )
