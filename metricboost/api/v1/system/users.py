from fastapi import APIRouter, Query
from tortoise.expressions import Q

from metricboost.controllers.user import user_controller
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import get_logger, insert_log
from metricboost.models.system import LogDetailType, LogType
from metricboost.schemas.users import UserCreate, UserUpdate

logger = get_logger(__name__)

router = APIRouter()


@router.get("/users", summary="查看用户列表")
async def _(
    page: int = Query(1, description="页码", ge=1),
    page_size: int = Query(10, description="每页数量", ge=1, alias="pageSize"),
    userName: str = Query(None, description="用户名"),
    userGender: str = Query(None, description="用户性别"),
    nickName: str = Query(None, description="用户昵称"),
    userPhone: str = Query(None, description="用户手机"),
    userEmail: str = Query(None, description="用户邮箱"),
    status: str = Query(None, description="用户状态"),
):
    q = Q()
    if userName:
        q &= Q(user_name__contains=userName)
    if userGender:
        q &= Q(user_gender__contains=userGender)
    if nickName:
        q &= Q(nick_name__contains=nickName)
    if userPhone:
        q &= Q(user_phone__contains=userPhone)
    if userEmail:
        q &= Q(user_email__contains=userEmail)
    if status:
        q &= Q(status__contains=status)

    total, user_objs = await user_controller.get_list(
        page=page,
        page_size=page_size,
        search=q,
        order=["id"],
    )
    records = []
    for user_obj in user_objs:
        record = await user_obj.to_dict(exclude_fields=["password"])
        await user_obj.fetch_related("roles")
        user_roles = [r.role_code for r in user_obj.roles]
        record.update({"userRoles": user_roles})
        records.append(record)
    data = {"records": records}

    # 记录操作日志
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.UserGetList,
        log_detail="查看用户列表",
        by_user_id=0,
    )
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/users/{user_id}", summary="查看用户")
async def get_user(user_id: int):
    logger.debug(f"查看用户: {user_id}")
    user_obj = await user_controller.get(id=user_id)
    if not user_obj:
        logger.warning(f"用户{user_id}不存在")
        return Error(msg=f"用户{user_id}不存在")
    return Success(data=await user_obj.to_dict(exclude_fields=["password"]))


@router.post("/users", summary="创建用户")
async def _(user_in: UserCreate):
    logger.debug(f"创建用户: {user_in}")
    user = await user_controller.get_by_username(user_in.user_name)
    if user:
        return Error(msg=f"用户名{user_in.user_name}已存在")
    new_user = await user_controller.create(obj_in=user_in)
    await user_controller.update_roles_by_code(new_user, user_in.roles)
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.UserCreateOne,
        log_detail="创建用户",
        by_user_id=0,
    )
    return Success(msg="创建成功", data={"created_id": new_user.id})


@router.patch("/users/{user_id}", summary="更新用户")
async def _(user_id: int, user_in: UserUpdate):
    logger.debug(f"更新用户: {user_id}")
    user = await user_controller.get(id=user_id)
    if not user:
        return Error(msg=f"用户{user_id}不存在")
    user = await user_controller.update(user_id=user_id, obj_in=user_in)
    await user_controller.update_roles_by_code(user, user_in.roles)
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.UserUpdateOne,
        log_detail="更新用户",
        by_user_id=0,
    )
    logger.debug(f"更新用户成功: {user_id}")

    return Success(msg="Updated Successfully", data={"updated_id": user_id})


@router.delete("/users/{user_id}", summary="删除用户")
async def _(user_id: int):
    logger.debug(f"删除用户: {user_id}")
    user = await user_controller.get(id=user_id)
    if not user:
        return Error(msg=f"用户{user_id}不存在")
    await user_controller.remove(id=user_id)
    logger.debug(f"删除用户成功: {user_id}")
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.UserDeleteOne,
        log_detail="删除用户",
        by_user_id=0,
    )
    return Success(msg="Deleted Successfully", data={"deleted_id": user_id})


@router.delete("/users", summary="批量删除用户")
async def _(ids: str = Query(..., description="用户ID列表, 用逗号隔开")):
    logger.debug(f"批量删除用户: {ids}")
    user_ids = ids.split(",")
    deleted_ids = []
    for user_id in user_ids:
        user_obj = await user_controller.get(id=int(user_id))
        await user_obj.delete()
        deleted_ids.append(int(user_id))
    logger.debug(f"批量删除用户成功: {deleted_ids}")
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.UserBatchDeleteOne,
        log_detail="批量删除用户",
        by_user_id=0,
    )
    return Success(msg="Deleted Successfully", data={"deleted_ids": deleted_ids})
