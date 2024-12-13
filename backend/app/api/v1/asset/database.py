from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.schemas.base import SuccessExtra, Success, Error
from app.controllers import database_controller
from app.models.system import LogType, LogDetailType, User
from app.api.v1.utils import insert_log
from app.schemas.database import DatabaseCreate, DatabaseUpdate

router = APIRouter()


# 获取全部数据库信息
@router.get("/databases", summary="获取数据库信息")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    status: str = Query(None, description="数据库状态"),
    databaseName: str = Query(None, description="数据库名称"),
    databaseType: str = Query(None, description="数据库类型"),
    createBy: str = Query(None, description="创建人"),
):
    # Q() 是一个查询构造器，用于构建复杂的数据库查询条件
    q = Q()
    # 使用 &= 运算符来添加条件，相当于 AND 操作
    if databaseName:
        q &= Q(database_name__contains=databaseName)
    if databaseType:
        q &= Q(database_type=databaseType)
    if status:
        q &= Q(status=status)  # 等同于 SQL: WHERE status LIKE '%status%'
    if createBy:
        q &= Q(create_by__user_name=createBy)

    total, database_objs = await database_controller.get_list(
        page=current,
        page_size=size,
        search=q,
        order=["id"],
    )
    records = [
        await database_obj.to_dict(exclude_fields=["password"])
        for database_obj in database_objs
    ]

    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataBaseGet,
        by_user_id=0,
    )
    return SuccessExtra(
        data={"records": records}, total=total, current=current, size=size
    )


@router.post("/databases", summary="创建数据库连接")
async def _(
    database_in: DatabaseCreate,
):
    new_database = await database_controller.create(obj_in=database_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataBaseCreate,
        by_user_id=0,
    )
    return Success(msg="创建成功", data={"create_id": new_database.id})


@router.patch("/databases/{database_id}", summary="更新数据库连接")
async def _(
    database_id: int,
    database_in: DatabaseUpdate,
):
    # 如果没有传密码，则不更新密码
    if not database_in.password:
        database_in.password = None
    await database_controller.update(database_id=database_id, obj_in=database_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataBaseUpdate,
        by_user_id=0,
    )
    return Success(msg="更新成功", data={"update_id": database_id})


@router.delete("/databases/{database_id}", summary="删除数据库连接")
async def _(
    database_id: int,
):
    await database_controller.remove(id=database_id)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataBaseDelete,
        by_user_id=0,
    )
    return Success(msg="删除成功", data={"delete_id": database_id})


@router.post("/databases/test", summary="测试数据库连接")
async def _(
    database_in: DatabaseCreate,
    database_id: int | None = None,
):

    # 如果是编辑数据库，传入数据库id，且没有传入密码，则根据ID获取数据密码
    if database_id and not database_in.password:
        database_in.password = (await database_controller.get(id=database_id)).password
    test_status, test_info = await database_controller.test_connection(
        obj_in=database_in
    )

    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataBaseTest,
        by_user_id=0,
    )

    if test_status == "连接成功":
        return Success(msg=test_status, data={"test_id": database_id})
    else:
        return Error(
            msg=test_status, data={"test_id": database_id, "test_info": test_info}
        )
