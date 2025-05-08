from typing import Optional

from fastapi import APIRouter, Body, Depends, Path, Query
from tortoise.expressions import Q

from metricboost.controllers.collect import collect_controller
from metricboost.core.ctx import get_current_user_id
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import insert_log
from metricboost.models.enums import CollectType, StatusType
from metricboost.models.system import LogDetailType, LogType
from metricboost.schemas.collect import CollectCreate, CollectUpdate

router = APIRouter()


@router.get(
    "/list",
    summary="获取数据采集任务列表",
)
async def get_collects(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量", alias="pageSize"),
    origin_database_ids: Optional[list] = Query(
        None, description="来源数据库ID", alias="originDatabaseIds"
    ),
    target_database_ids: Optional[list] = Query(
        None, description="目标数据库ID", alias="targetDatabaseIds"
    ),
    type: Optional[CollectType] = Query(None, description="采集类型"),
    name: Optional[str] = Query(None, description="采集任务名称"),
    status: Optional[StatusType] = Query(None, description="采集任务状态"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取数据采集任务列表

    - 支持按状态、名称、类型筛选
    - 默认按ID排序
    """
    # 处理来源数据库ID
    origin_database_type = []
    if origin_database_ids:
        # 创建一个新列表存储非字符串类型的ID
        numeric_target_ids = []
        for item in origin_database_ids:
            try:
                int(item)
                # 字符串类型（如mysql、达梦等）添加到database_type列表
                numeric_target_ids.append(item)
            except:
                # 非字符串类型（数字ID）保留在target_database_ids
                origin_database_type.append(item)
        origin_database_ids = numeric_target_ids

    # 处理目标数据库ID
    target_database_type = []
    if target_database_ids:
        # 创建一个新列表存储非字符串类型的ID
        numeric_target_ids = []
        for item in target_database_ids:
            try:
                int(item)
                # 字符串类型（如mysql、达梦等）添加到database_type列表
                numeric_target_ids.append(item)
            except:
                # 非字符串类型（数字ID）保留在target_database_ids
                target_database_type.append(item)
        target_database_ids = numeric_target_ids

    try:
        # 构建查询条件
        q = Q()
        if name:
            q &= Q(name__contains=name)
        if type:
            q &= Q(type=type)
        if status:
            q &= Q(status=status)

        # 处理origin条件，让type和ids是OR关系
        origin_condition = Q()
        if origin_database_type:
            origin_condition |= Q(origin_database__type__in=origin_database_type)
        if origin_database_ids:
            origin_condition |= Q(origin_database_id__in=origin_database_ids)
        if origin_database_type or origin_database_ids:
            q &= origin_condition

        # 处理target条件，让type和ids是OR关系
        target_condition = Q()
        if target_database_type:
            target_condition |= Q(target_database__type__in=target_database_type)
        if target_database_ids:
            target_condition |= Q(target_database_id__in=target_database_ids)
        if target_database_type or target_database_ids:
            q &= target_condition

        # 获取采集任务列表
        total, collect_objs = await collect_controller.get_list(
            page=page,
            page_size=page_size,
            search=q,
            order=["id"],
            prefetch=["origin_database", "target_database", "create_by", "update_by"],
        )

        # 转换为响应格式
        records = []
        for obj in collect_objs:
            collect_dict = await obj.to_dict()
            origin_db = await obj.origin_database
            target_db = await obj.target_database
            create_by = await obj.create_by
            update_by = await obj.update_by

            collect_dict["originDatabase"] = origin_db.name if origin_db else None
            collect_dict["targetDatabase"] = target_db.name if target_db else None
            collect_dict["createBy"] = create_by.user_name if create_by else "系统"
            collect_dict["updateBy"] = update_by.user_name if update_by else "系统"

            records.append(collect_dict)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectGet,
            log_detail=f"获取数据采集任务列表: 页码={page}, 每页={page_size}",
            by_user_id=user_id,
        )

        return SuccessExtra(
            data={"records": records}, total=total, page=page, page_size=page_size
        )

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectGet,
            log_detail=f"获取数据采集任务列表失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"查询失败: {str(e)}")


@router.post("/create", summary="创建数据采集任务")
async def create_collect(
    collect_in: CollectCreate,
    # user_id: int = Depends(get_current_user_id),
    user_id=1,
):
    """
    创建新的数据采集任务

    - 成功创建后返回新创建的采集任务ID
    """
    try:
        collect_in.create_by_id = user_id
        collect_in.update_by_id = user_id
        new_collect = await collect_controller.create(obj_in=collect_in)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectCreate,
            log_detail=f"创建数据采集任务: 名称={collect_in.name}, 类型={collect_in.type}",
            by_user_id=user_id,
        )

        return Success(msg="创建成功", data={"create_id": new_collect.id})

    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectCreate,
            log_detail=f"创建数据采集任务失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"创建失败: {str(e)}")


@router.patch("/{collect_id}", summary="更新数据采集任务")
async def update_collect(
    collect_id: int = Path(..., description="数据采集任务ID"),
    collect_in: CollectUpdate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    更新指定ID的数据采集任务
    """
    try:
        collect_in.update_by_id = user_id
        await collect_controller.update(id=collect_id, obj_in=collect_in)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectUpdate,
            log_detail=f"更新数据采集任务: ID={collect_id}",
            by_user_id=user_id,
        )

        return Success(msg="更新成功", data={"update_id": collect_id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectUpdate,
            log_detail=f"更新数据采集任务失败: ID={collect_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"更新失败: {str(e)}")


@router.delete("/{collect_id}", summary="删除数据采集任务")
async def delete_collect(
    collect_id: int = Path(..., description="数据采集任务ID"),
    user_id: int = Depends(get_current_user_id),
):
    """
    删除指定ID的数据采集任务

    - 成功删除后返回被删除的采集任务ID
    """
    try:
        # 获取任务信息用于日志记录
        collect_info = await collect_controller.get(id=collect_id)

        await collect_controller.remove(id=collect_id)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectDelete,
            log_detail=f"删除数据采集任务: ID={collect_id}, 名称={collect_info.name}",
            by_user_id=user_id,
        )

        return Success(msg="删除成功", data={"delete_id": collect_id})

    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectDelete,
            log_detail=f"删除数据采集任务失败: ID={collect_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"删除失败: {str(e)}")


@router.delete("/delete", summary="批量删除数据采集任务")
async def batch_delete_collects(
    ids: str = Query(..., description="采集任务ID列表，用逗号隔开"),
    user_id: int = Depends(get_current_user_id),
):
    """
    批量删除数据采集任务

    - 接受以逗号分隔的ID列表
    - 返回成功删除的ID列表
    """
    try:
        collect_ids = ids.split(",")
        deleted_ids = []
        failed_ids = []

        for collect_id in collect_ids:
            try:
                cid = int(collect_id)
                # 获取任务信息用于日志记录
                collect_info = await collect_controller.get(id=cid)
                if collect_info:
                    result = await collect_controller.remove(id=cid)
                    if result:
                        deleted_ids.append(cid)
                    else:
                        failed_ids.append(cid)
                else:
                    failed_ids.append(cid)
            except Exception:
                failed_ids.append(int(collect_id))

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectDelete,
            log_detail=f"批量删除数据采集任务: 成功={deleted_ids}, 失败={failed_ids}",
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
            log_detail_type=LogDetailType.CollectDelete,
            log_detail=f"批量删除数据采集任务失败: IDs={ids}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"批量删除失败: {str(e)}")


@router.post("/{collect_id}/toggle", summary="切换数据采集任务状态")
async def toggle_collect_status(
    collect_id: int = Path(..., description="数据采集任务ID"),
    status: StatusType = Body(..., description="要设置的状态"),
    user_id: int = Depends(get_current_user_id),
):
    """
    切换数据采集任务状态（启用/禁用）
    """
    try:
        await collect_controller.toggle_status(id=collect_id, status=status)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectUpdate,
            log_detail=f"切换数据采集任务状态: ID={collect_id}, 状态={status}",
            by_user_id=user_id,
        )

        return Success(
            msg="状态切换成功", data={"collect_id": collect_id, "status": status}
        )

    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectUpdate,
            log_detail=f"切换数据采集任务状态失败: ID={collect_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"状态切换失败: {str(e)}")


@router.post("/collects/{collect_id}/execute", summary="执行离线同步任务")
async def execute_offline_sync(
    collect_id: int = Path(..., description="数据采集任务ID"),
    user_id: int = Depends(get_current_user_id),
):
    """
    执行离线同步任务

    - 仅适用于离线同步类型的任务
    - 从MySQL/达梦同步数据到Hive
    """
    try:
        result = await collect_controller.execute_offline_sync(id=collect_id)

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectExecute,
            log_detail=f"执行离线同步任务: ID={collect_id}",
            by_user_id=user_id,
        )

        return Success(msg="任务执行已提交", data=result)

    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectExecute,
            log_detail=f"执行离线同步任务失败: ID={collect_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"任务执行失败: {str(e)}")


@router.post("/collects/{collect_id}/configure", summary="配置实时同步任务")
async def configure_realtime_sync(
    collect_id: int = Path(..., description="数据采集任务ID"),
    flume_config: dict = Body(..., description="Flume配置"),
    user_id: int = Depends(get_current_user_id),
):
    """
    配置实时同步任务

    - 仅适用于实时同步类型的任务
    - 配置Flume从日志文件同步到HDFS
    """
    try:
        result = await collect_controller.configure_realtime_sync(
            id=collect_id, flume_config=flume_config
        )

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectConfigure,
            log_detail=f"配置实时同步任务: ID={collect_id}",
            by_user_id=user_id,
        )

        return Success(msg="实时同步配置成功", data=result)

    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectConfigure,
            log_detail=f"配置实时同步任务失败: ID={collect_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"配置失败: {str(e)}")


@router.get("/collects/status", summary="获取所有采集任务状态")
async def get_collect_tasks_status(
    user_id: int = Depends(get_current_user_id),
):
    """
    获取所有采集任务的状态信息

    - 返回离线和实时任务的统计信息
    - 包括各状态的任务数量
    """
    try:
        # 获取所有任务
        all_tasks = await collect_controller.model.all()

        # 统计信息
        stats = {
            "total": len(all_tasks),
            "offline": {
                "total": sum(1 for task in all_tasks if task.type == CollectType.BATCH),
                "enabled": sum(
                    1
                    for task in all_tasks
                    if task.type == CollectType.BATCH
                    and task.status == StatusType.enable
                ),
                "disabled": sum(
                    1
                    for task in all_tasks
                    if task.type == CollectType.BATCH
                    and task.status == StatusType.disable
                ),
            },
            "STREAM": {
                "total": sum(
                    1 for task in all_tasks if task.type == CollectType.STREAM
                ),
                "enabled": sum(
                    1
                    for task in all_tasks
                    if task.type == CollectType.STREAM
                    and task.status == StatusType.enable
                ),
                "disabled": sum(
                    1
                    for task in all_tasks
                    if task.type == CollectType.STREAM
                    and task.status == StatusType.disable
                ),
            },
        }

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectGet,
            log_detail=f"获取所有采集任务状态",
            by_user_id=user_id,
        )

        return Success(msg="查询成功", data=stats)

    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.CollectGet,
            log_detail=f"获取采集任务状态失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"查询失败: {str(e)}")
