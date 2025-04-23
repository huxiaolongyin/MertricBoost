from typing import Optional

from cachetools import TTLCache
from fastapi import APIRouter, Body, Depends, Path, Query
from tortoise.expressions import Q

from metricboost.controllers.domain import domain_controller
from metricboost.core.ctx import get_current_user_id
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import insert_log
from metricboost.models.enums import DomainType
from metricboost.models.system import LogDetailType, LogType
from metricboost.schemas.domain import DomainCreate, DomainUpdate

router = APIRouter()

# 统一缓存实例，为不同类型域分别设置缓存键前缀
domain_cache = TTLCache(maxsize=300, ttl=300)  # 5分钟过期


@router.get(
    "/domains",
    summary="获取域信息列表",
)
async def get_domains(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量", alias="pageSize"),
    domain_name: Optional[str] = Query(None, description="域名称", alias="domainName"),
    domain_type: Optional[DomainType] = Query(
        None, description="域类型: 1=数据域, 2=主题域", alias="domainType"
    ),
    with_metrics_count: bool = Query(False, description="是否返回关联的指标数量"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取域信息列表

    - 支持按域名称和类型筛选
    - 可选择是否返回关联的指标数量
    - 返回结果使用缓存提高性能
    """
    try:
        # 构建查询条件
        q = Q()
        if domain_name:
            q &= Q(domain_name__contains=domain_name)
        if domain_type:
            q &= Q(domain_type=domain_type)

        # 构建缓存键
        cache_key = f"domain_list_{domain_type}_{domain_name}_{page}_{page_size}_{with_metrics_count}"

        # 尝试从缓存获取数据
        if cache_key in domain_cache:
            total, records = domain_cache[cache_key]
        else:
            # 根据请求决定是否获取指标计数
            if with_metrics_count:
                total, records = await domain_controller.get_domains_with_metrics_count(
                    domain_type=domain_type, page=page, page_size=page_size
                )
            else:
                # 从数据库获取标准域信息
                total, domain_objs = await domain_controller.get_list(
                    page=page,
                    page_size=page_size,
                    search=q,
                    order=["id"],
                    # prefetch=["create_by"],
                )

                # 转换为响应格式
                records = []
                for domain in domain_objs:
                    domain_dict = await domain.to_dict()
                    create_by = await domain.create_by
                    domain_dict["createBy"] = (
                        create_by.user_name if create_by else "系统"
                    )
                    records.append(domain_dict)

            # 存入缓存
            domain_cache[cache_key] = (total, records)

        # 记录日志
        domain_type_name = (
            "数据域" if domain_type == 1 else "主题域" if domain_type == 2 else "所有域"
        )
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainGet,
            log_detail=f"获取{domain_type_name}列表，页码: {page}, 每页: {page_size}",
            by_user_id=user_id,
        )

        return SuccessExtra(
            data={"records": records}, total=total, page=page, page_size=page_size
        )

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainGet,
            log_detail=f"获取域列表失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"获取域列表失败: {str(e)}")


@router.post("/domains", summary="创建域信息")
async def create_domain(
    domain_in: DomainCreate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    创建新的域信息

    - domain_type必须为1(数据域)或2(主题域)
    - 同类型域名不能重复
    """

    try:
        # 创建域
        domain_in.create_by_id = user_id
        domain_in.update_by_id = user_id
        new_domain = await domain_controller.create(obj_in=domain_in)

        # 清除相关缓存
        keys_to_remove = [
            k for k in domain_cache.keys() if k.startswith("domain_list_")
        ]
        for k in keys_to_remove:
            domain_cache.pop(k, None)

        # 记录日志
        domain_type_name = (
            "数据域" if domain_in.domain_type == DomainType.DATA else "主题域"
        )

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainCreate,
            log_detail=f"创建{domain_type_name}: 名称={domain_in.domain_name}",
            by_user_id=user_id,
        )

        return Success(msg="创建成功", data={"create_id": new_domain.id})

    except ValueError as e:
        # 记录验证错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainCreate,
            log_detail=f"创建域验证失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=str(e))

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainCreate,
            log_detail=f"创建域失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"创建域失败: {str(e)}")


@router.patch("/domains/{id}", summary="更新域信息")
async def update_domain(
    id: int = Path(..., description="域ID"),
    domain_in: DomainUpdate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    更新指定ID的域信息

    - 可以修改域名称和描述
    - 更新域类型时需谨慎
    """
    try:
        # 获取原始数据用于日志记录
        domain_in.update_by_id = user_id
        original = await domain_controller.get(id=id)

        # 更新域
        await domain_controller.update(id=id, obj_in=domain_in)

        # 清除相关缓存
        keys_to_remove = [
            k for k in domain_cache.keys() if k.startswith("domain_list_")
        ]
        for k in keys_to_remove:
            domain_cache.pop(k, None)

        # 记录日志
        domain_type_name = (
            "数据域" if original.domain_type == DomainType.DATA else "主题域"
        )

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainUpdate,
            log_detail=f"更新{domain_type_name}: ID={id}, 名称={domain_in.domain_name or original.domain_name}",
            by_user_id=user_id,
        )

        return Success(msg="更新成功", data={"update_id": id})

    except ValueError as e:
        # 记录验证错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainUpdate,
            log_detail=f"更新域验证失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=str(e))

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainUpdate,
            log_detail=f"更新域失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"更新域失败: {str(e)}")


@router.delete("/domains/{id}", summary="删除域信息")
async def delete_domain(
    id: int = Path(..., description="域ID"),
    user_id: int = Depends(get_current_user_id),
):
    """
    删除指定ID的域信息

    - 如果域已被模型或指标关联，可能会导致删除失败
    """
    try:
        # 获取原始数据用于日志记录
        domain_info = await domain_controller.get(id=id)

        # 删除域
        await domain_controller.remove(id=id)

        # 清除相关缓存
        keys_to_remove = [
            k for k in domain_cache.keys() if k.startswith("domain_list_")
        ]
        for k in keys_to_remove:
            domain_cache.pop(k, None)

        # 记录日志
        domain_type_name = (
            "数据域" if domain_info.domain_type == DomainType.DATA else "主题域"
        )

        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainDelete,
            log_detail=f"删除{domain_type_name}: ID={id}, 名称={domain_info.domain_name}",
            by_user_id=user_id,
        )

        return Success(msg="删除成功", data={"delete_id": id})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainDelete,
            log_detail=f"删除域失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"删除域失败: {str(e)}")


@router.delete("/domains", summary="批量删除域信息")
async def batch_delete_domain(
    ids: str = Query(..., description="域ID列表，用逗号隔开"),
    user_id: int = Depends(get_current_user_id),
):
    """
    批量删除域信息

    - 接受以逗号分隔的ID列表
    - 返回成功删除的ID列表及失败的ID列表
    """
    try:
        domain_ids = ids.split(",")
        deleted_ids = []
        failed_ids = []

        for domain_id in domain_ids:
            try:
                # 获取原始数据用于日志记录
                domain_info = await domain_controller.get(id=int(domain_id))
                if domain_info:
                    result = await domain_controller.remove(id=int(domain_id))
                    if result:
                        deleted_ids.append(int(domain_id))
                    else:
                        failed_ids.append(int(domain_id))
                else:
                    failed_ids.append(int(domain_id))
            except Exception:
                failed_ids.append(int(domain_id))

        # 清除相关缓存
        keys_to_remove = [
            k for k in domain_cache.keys() if k.startswith("domain_list_")
        ]
        for k in keys_to_remove:
            domain_cache.pop(k, None)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainDelete,
            log_detail=f"批量删除域: 成功IDs={deleted_ids}, 失败IDs={failed_ids}",
            by_user_id=user_id,
        )

        if failed_ids:
            return Success(
                msg=f"批量删除部分成功，{len(failed_ids)}个ID删除失败",
                data={"deleted_ids": deleted_ids, "failed_ids": failed_ids},
            )
        return Success(msg="批量删除成功", data={"deleted_ids": deleted_ids})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DomainDelete,
            log_detail=f"批量删除域失败: IDs={ids}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"批量删除域失败: {str(e)}")
