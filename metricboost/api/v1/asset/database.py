from typing import Optional

from fastapi import APIRouter, Body, Depends, Path, Query
from tortoise.expressions import Q

from metricboost.controllers.database import database_controller
from metricboost.core.ctx import get_current_user_id
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import insert_log
from metricboost.models.system import LogDetailType, LogType
from metricboost.schemas.database import DatabaseCreate, DatabaseUpdate

router = APIRouter()


@router.get(
    "/databases",
    summary="获取数据库连接列表",
)
async def get_databases(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量", alias="pageSize"),
    status: Optional[str] = Query(None, description="数据库状态"),
    name: Optional[str] = Query(None, description="数据库名称"),
    type: Optional[str] = Query(None, description="数据库类型"),
    with_metrics_count: bool = Query(False, description="是否返回关联的模型数量"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取数据库连接列表

    - 支持按状态、名称、类型筛选
    - 可以选择是否返回关联的数据模型数量
    - 默认按ID排序
    """
    try:
        # 构建查询条件
        q = Q()
        if name:
            q &= Q(name__contains=name)
        if type:
            if "-" in type:
                q &= Q(type__not=type.split("-")[1])
            else:
                q &= Q(type=type)
        if status:
            q &= Q(status=status)

        if with_metrics_count:
            # 获取数据库及其模型数量
            total, records = await database_controller.get_databases_with_models_count(
                page=page, page_size=page_size
            )
        else:
            # 获取标准数据库列表
            total, database_objs = await database_controller.get_list(
                page=page,
                page_size=page_size,
                search=q,
                order=["id"],
                prefetch=["create_by"],
            )

            # 转换为响应格式，排除密码字段
            records = []
            for db in database_objs:
                db_dict = await db.to_dict(exclude_fields={"password"})
                create_by = await db.create_by
                db_dict["createBy"] = create_by.user_name if create_by else "系统"
                records.append(db_dict)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseGet,
            log_detail=f"获取数据库连接列表: 页码={page}, 每页={page_size}",
            by_user_id=user_id,
        )

        return SuccessExtra(
            data={"records": records}, total=total, page=page, page_size=page_size
        )

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseGet,
            log_detail=f"获取数据库连接列表失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"查询失败: {str(e)}")


@router.post("/databases", summary="创建数据库连接")
async def create_database(
    database_in: DatabaseCreate,
    user_id: int = Depends(get_current_user_id),
):
    """
    创建新的数据库连接

    - 自动进行连接测试，失败则不创建
    - 成功创建后返回新创建的数据库ID
    """
    try:
        database_in.create_by_id = user_id
        database_in.update_by_id = user_id
        new_database = await database_controller.create(obj_in=database_in)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseCreate,
            log_detail=f"创建数据库连接: 名称={database_in.name}, 类型={database_in.type}",
            by_user_id=user_id,
        )

        return Success(msg="创建成功", data={"create_id": new_database.id})

    except Exception as e:

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseCreate,
            log_detail=f"创建数据库连接失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"创建失败: {str(e)}")


@router.patch("/databases/{database_id}", summary="更新数据库连接")
async def update_database(
    database_id: int = Path(..., description="数据库连接ID"),
    database_in: DatabaseUpdate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    更新指定ID的数据库连接

    - 如果更新了连接信息，会自动进行连接测试
    - 密码字段为空时，会保留原密码
    """
    try:
        database_in.update_by_id = user_id
        await database_controller.update(id=database_id, obj_in=database_in)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseUpdate,
            log_detail=f"更新数据库连接: ID={database_id}, 名称={database_in.name}",
            by_user_id=user_id,
        )

        return Success(msg="更新成功", data={"update_id": database_id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseUpdate,
            log_detail=f"更新数据库连接失败: ID={database_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"更新失败: {str(e)}")


@router.delete("/databases/{database_id}", summary="删除数据库连接")
async def delete_database(
    database_id: int = Path(..., description="数据库连接ID"),
    user_id: int = Depends(get_current_user_id),
):
    """
    删除指定ID的数据库连接

    - 成功删除后返回被删除的数据库ID
    """
    try:
        # 获取数据库信息用于日志记录
        db_info = await database_controller.get(id=database_id)

        await database_controller.remove(id=database_id)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseDelete,
            log_detail=f"删除数据库连接: ID={database_id}, 名称={db_info.name}",
            by_user_id=user_id,
        )

        return Success(msg="删除成功", data={"delete_id": database_id})

    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseDelete,
            log_detail=f"删除数据库连接失败: ID={database_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"删除失败: {str(e)}")


@router.delete("/databases", summary="批量删除数据库连接")
async def batch_delete_databases(
    ids: str = Query(..., description="数据库ID列表，用逗号隔开"),
    user_id: int = Depends(get_current_user_id),
):
    """
    批量删除数据库连接

    - 接受以逗号分隔的ID列表
    - 返回成功删除的ID列表
    """
    try:
        database_ids = ids.split(",")
        deleted_ids = []
        failed_ids = []

        for database_id in database_ids:
            try:
                db_id = int(database_id)
                # 获取数据库信息用于日志记录
                db_info = await database_controller.get(id=db_id)
                if db_info:
                    result = await database_controller.remove(id=db_id)
                    if result:
                        deleted_ids.append(db_id)
                    else:
                        failed_ids.append(db_id)
                else:
                    failed_ids.append(db_id)
            except Exception:
                failed_ids.append(int(database_id))

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseDelete,
            log_detail=f"批量删除数据库连接: 成功={deleted_ids}, 失败={failed_ids}",
            by_user_id=user_id,
        )

        if failed_ids:
            return Success(
                msg="部分删除成功",
                data={"deleted_ids": deleted_ids, "failed_ids": failed_ids},
            )
        return Success(msg="批量删除成功", data={"deleted_ids": deleted_ids})

    except Exception as e:
        # 记录错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseDelete,
            log_detail=f"批量删除数据库连接失败: IDs={ids}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"批量删除失败: {str(e)}")


@router.post("/databases/test", summary="测试数据库连接")
async def test_database_connection(
    database_in: DatabaseCreate,
    database_id: Optional[int] = Query(
        None, description="现有数据库ID", alias="databaseId"
    ),
    user_id: int = Depends(get_current_user_id),
):
    """
    测试数据库连接

    - 如果提供数据库ID且未提供密码，会使用已有数据库的密码
    - 返回连接测试结果和性能指标
    """
    try:
        # 如果是编辑数据库，传入数据库id，且没有传入密码，则根据ID获取数据密码
        if database_id and not database_in.password:
            existing_db = await database_controller.get(id=database_id)
            if existing_db:
                database_in.password = existing_db.password
            else:
                return Error(msg=f"找不到ID为{database_id}的数据库连接")

        # 记录开始时间，用于计算响应时间
        import time

        start_time = time.time()

        success, error = await database_controller.test_connection(obj_in=database_in)

        # 计算响应时间
        response_time = (time.time() - start_time) * 1000  # 转换为毫秒

        # 添加连接性能信息
        connection_metrics = {
            "response_time_ms": round(response_time, 2),
        }

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseTest,
            log_detail=f"测试数据库连接: 名称={database_in.name}, 类型={database_in.type}, 结果={'成功' if success else '失败'}",
            by_user_id=user_id,
        )

        if success:
            return Success(
                msg="连接成功",
                data={"test_id": database_id, "metrics": connection_metrics},
            )
        else:
            return Error(
                msg=f"连接失败，错误信息: {error}",
                data={
                    "test_id": database_id,
                    "error": error,
                    "metrics": connection_metrics,
                },
            )

    except Exception as e:
        # 记录错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseTest,
            log_detail=f"测试数据库连接异常: 名称={database_in.name}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg="测试连接发生异常", data={"error": str(e)})


@router.get("/databases/health", summary="检查所有数据库连接健康状态")
async def check_database_health(
    user_id: int = Depends(get_current_user_id),
):
    """
    检查所有数据库连接的健康状态

    - 测试所有启用状态的数据库连接
    - 返回每个数据库的连接结果和性能指标
    """
    try:
        # 获取所有数据库连接
        total, database_objs = await database_controller.get_list(
            page=1,
            page_size=1000,  # 假设数据库连接数量不会太多
            search=Q(status="1"),  # 只检查激活状态的连接
        )

        # 存储健康状态结果
        health_results = []

        # 检查每个数据库连接
        for db in database_objs:
            db_info = await db.to_dict(exclude=["password"])
            db_create = DatabaseCreate(**db_info)

            # 测试连接
            import time

            start_time = time.time()
            success, error = await database_controller.test_connection(obj_in=db_create)
            response_time = (time.time() - start_time) * 1000  # 转换为毫秒

            health_results.append(
                {
                    "id": db.id,
                    "name": db.name,
                    "type": db.type,
                    "status": "连接成功" if success else f"连接失败: {error}",
                    "response_time_ms": round(response_time, 2),
                    "last_checked": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseTest,
            log_detail=f"检查所有数据库连接健康状态: 共{len(health_results)}个连接",
            by_user_id=user_id,
        )

        return Success(
            msg="健康检查完成",
            data={
                "health_status": health_results,
                "summary": {
                    "total": len(health_results),
                    "healthy": sum(
                        1 for r in health_results if "连接成功" in r["status"]
                    ),
                    "unhealthy": sum(
                        1 for r in health_results if "连接失败" in r["status"]
                    ),
                },
            },
        )

    except Exception as e:
        # 记录错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataBaseTest,
            log_detail=f"检查数据库连接健康状态失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"健康检查失败: {str(e)}")
