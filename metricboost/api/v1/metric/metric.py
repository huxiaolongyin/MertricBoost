from datetime import datetime
from types import NoneType
from typing import List

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from tortoise.expressions import Q

from metricboost.controllers.metric import metric_controller
from metricboost.core.ctx import get_current_user_id
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import insert_log
from metricboost.models.system import LogDetailType, LogType, Role, User
from metricboost.schemas.metric import MetricCreate, MetricUpdate

router = APIRouter()


async def get_role_auth(user_id: int):
    user = await User.get(id=user_id).prefetch_related("roles")
    roles: List[Role] = await user.roles

    # 获取角色关联的域ID列表
    allowed_domain_ids = []

    # 获取最高敏感度级别
    max_sensitivity_level = 0

    # 管理员角色标识
    is_admin = False

    for role in roles:
        # 检查是否是管理员角色
        if role.is_admin:
            is_admin = True
            break

        # 获取角色关联的域
        await role.fetch_related("domains")
        allowed_domain_ids.extend([domain.id for domain in role.domains])

        # 更新最高敏感度级别
        if int(role.sensitivity) > max_sensitivity_level:
            max_sensitivity_level = int(role.sensitivity)

    return is_admin, allowed_domain_ids, max_sensitivity_level


@router.get("/list", summary="获取指标列表")
async def get_metric_list(
    name_or_desc: str = Query(None, alias="nameOrDesc"),
    domain_ids: List[int] = Query([], alias="domainIds"),
    tag_ids: List[int] = Query([], alias="tagIds"),
    sensitivity: str = Query(None),
    page: int = Query(1, alias="page"),
    page_size: int = Query(10, alias="pageSize"),
    order: list[str] = Query(None),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取指标列表

    - 支持按名称、描述、主题域、标签等筛选
    - 支持分页和排序
    - 返回指标的基本信息，不包含数据
    """

    if order is None or len(order) == 0 or order[0] == "":
        order = ["-id"]
    try:
        # 获取用户权限信息
        is_admin, allowed_domain_ids, max_sensitivity_level = await get_role_auth(
            user_id
        )

        # 构建查询条件
        q = Q()

        # 名称或描述的过滤
        if name_or_desc:
            q &= Q(metric_name__icontains=name_or_desc) | Q(
                metric_desc__icontains=name_or_desc
            )

        # 主题域过滤（结合权限）
        if domain_ids:  # 避免对可能是整数的值调用len()
            # 确保domain_ids是列表
            domain_ids_list = (
                domain_ids if isinstance(domain_ids, list) else [domain_ids]
            )

            if not is_admin:
                # 找出用户请求的域和有权限的域的交集
                accessible_domain_ids = set(allowed_domain_ids) & set(domain_ids_list)
                if not accessible_domain_ids:
                    return Error(msg="没有权限查看指定域的指标")
                # 修改为通过data_model关联查询域
                q &= Q(data_model__domains__id__in=list(accessible_domain_ids))
            else:
                # 管理员可以查看所有请求的域
                q &= Q(data_model__domains__id__in=domain_ids_list)
        elif not is_admin:
            # 如果用户没有指定域过滤，则只查看用户有权限的域
            if allowed_domain_ids:
                # 修改为通过data_model关联查询域
                q &= Q(data_model__domains__id__in=allowed_domain_ids)
            else:
                return Error(msg="没有权限查看任何域的指标")

        # 标签过滤
        if tag_ids and len(tag_ids):
            q &= Q(tags__id__in=tag_ids)

        # 敏感度过滤（结合权限）
        if sensitivity:
            # 如果用户指定了敏感度过滤，则只查看用户有权限的敏感度级别
            if not is_admin and int(sensitivity) > max_sensitivity_level:
                return Error(msg="没有权限查看该敏感度级别的指标")
            q &= Q(sensitivity=sensitivity)
        elif not is_admin:
            # 如果用户没有指定敏感度过滤，则只查看用户有权限的敏感度级别
            q &= Q(sensitivity__lte=str(max_sensitivity_level))
            pass

        # if domains
        total, metric_data = await metric_controller.get_list(
            page=page,
            page_size=page_size,
            search=q,
            order=order,
            distinct=True,
        )

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricGet,
            log_detail=f"获取指标列表: 页码={page}, 每页={page_size}",
            by_user_id=user_id,
        )

        return SuccessExtra(
            data={"records": jsonable_encoder(metric_data)},
            total=total,
            page=page,
            page_size=page_size,
        )

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricGet,
            log_detail=f"获取指标列表失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"获取指标列表失败: {str(e)}")


@router.post("/tag", summary="添加指标标签")
async def add_tag(
    metric_id: int = Body(..., description="指标ID", alias="metricId"),
    tag_id: int = Body(..., description="标签ID", alias="tagId"),
    user_id: int = Depends(get_current_user_id),
):
    """添加指标标签"""
    try:
        await metric_controller.add_tag(metric_id=metric_id, tag_id=tag_id)
    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricAddTag,
            log_detail=f"添加指标标签失败: metric_id={metric_id}, tag_id={tag_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"添加标签失败: {str(e)}")

    return Success(msg="添加标签成功")


@router.post("/create", summary="创建指标")
async def create_metric(
    metric_in: MetricCreate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    创建新的指标

    - 必须提供数据模型ID、指标名称和统计配置
    - 返回新创建的指标ID
    """
    try:
        # 创建指标
        metric_in.create_by_id = user_id
        metric_in.update_by_id = user_id
        new_metric = await metric_controller.create(obj_in=metric_in)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricCreate,
            log_detail=f"创建指标: 名称={metric_in.metric_name}, 数据模型ID={metric_in.data_model_id}",
            by_user_id=user_id,
        )

        return Success(msg="创建成功", data={"create_id": new_metric.id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricCreate,
            log_detail=f"创建指标失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"创建指标失败: {str(e)}")


@router.post("/{id}", summary="获取单个指标详情")
async def get_metric_detail(
    id: int = Path(..., description="指标ID"),
    date_range: list = Body(
        None, description="数据日期范围, Unix 时间戳毫秒级别格式", alias="dateRange"
    ),
    statistical_period: str = Body(
        None, description="统计周期", alias="statisticalPeriod"
    ),
    dim_select: str = Body(None, description="选择的维度列表", alias="dimSelect"),
    dim_filter: list[str] = Body(None, description="维度的过滤条件", alias="dimFilter"),
    sort: str = Body(None, description="排序方式", alias="sort"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取单个指标的详细信息和数据

    - 通过ID精确获取指标
    - 支持维度钻取和条件过滤
    - 支持自定义统计周期和日期范围
    """
    # 处理日期范围
    if date_range and len(date_range) == 2:
        # 时间戳 转 %Y-%m-%d
        date_range = [
            datetime.fromtimestamp(int(date_range[0]) / 1000).strftime("%Y-%m-%d"),
            datetime.fromtimestamp(int(date_range[1]) / 1000).strftime("%Y-%m-%d"),
        ]
    elif isinstance(date_range, NoneType):
        date_range = None
    elif not date_range[0] and len(date_range) == 1:
        date_range = None
    else:
        return Error(msg="日期范围不正确")

    # 处理统计周期
    if not statistical_period:
        statistical_period = None

    # 处理维度选择
    if not dim_select or not dim_select[0]:
        dim_select = None

    try:
        metric_data = await metric_controller.get_detail(
            id,
            user_id,
            date_range,
            statistical_period,
            dim_select,
            dim_filter,
            sort=sort,
        )

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricGet,
            log_detail=f"获取指标详情: ID={id}, 维度={dim_select}, 日期范围={date_range}, 统计周期={statistical_period}",
            by_user_id=user_id,
        )

        return Success(msg="获取成功", data={"records": jsonable_encoder(metric_data)})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricGet,
            log_detail=f"获取指标详情失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"获取指标详情失败: {str(e)}")


@router.patch("/{id}", summary="更新指标")
async def update_metric(
    id: int = Path(..., description="指标ID"),
    metric_in: MetricUpdate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    更新指定ID的指标

    - 可以更新名称、统计配置、敏感度等属性
    - 返回更新成功的指标ID
    """
    try:
        # 获取原始数据用于日志记录
        original = await metric_controller.get(id=id)
        if not original:
            return Error(msg=f"指标ID {id} 不存在")

        # 更新指标
        await metric_controller.update(id=id, obj_in=metric_in)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricUpdate,
            log_detail=f"更新指标: ID={id}, 名称={metric_in.metric_name or original.metric_name}",
            by_user_id=user_id,
        )

        return Success(msg="更新成功", data={"update_id": id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricUpdate,
            log_detail=f"更新指标失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"更新指标失败: {str(e)}")


@router.delete("/tag", summary="移除指标标签")
async def remove_tag(
    metric_id: int = Query(..., description="指标ID", alias="metricId"),
    tag_name: str = Query(..., description="标签名称", alias="tagName"),
    user_id: int = Depends(get_current_user_id),
):
    """移除指标标签"""
    try:
        await metric_controller.remove_tag(metric_id=metric_id, tag_name=tag_name)
    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricRemoveTag,
            log_detail=f"移除指标标签失败: metric_id={metric_id}, tag_name={tag_name}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"移除标签失败: {str(e)}")

    return Success(msg="移除标签成功")


@router.delete("/{id}", summary="删除指标")
async def delete_metric(
    id: int = Path(..., description="指标ID"),
    user_id: int = Depends(get_current_user_id),
):
    """
    删除指定ID的指标

    - 同时会删除与该指标关联的标签关系
    - 返回删除成功的指标ID
    """
    try:
        # 获取原始数据用于日志记录
        metric_info = await metric_controller.get(id=id)
        if not metric_info:
            return Error(msg=f"指标ID {id} 不存在")

        # 删除指标
        await metric_controller.remove(id=id)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricDelete,
            log_detail=f"删除指标: ID={id}, 名称={metric_info.metric_name}",
            by_user_id=user_id,
        )

        return Success(msg="删除成功", data={"delete_id": id})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricDelete,
            log_detail=f"删除指标失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"删除指标失败: {str(e)}")


@router.delete("/", summary="批量删除指标")
async def batch_delete_metric(
    ids: str = Query(..., description="指标ID列表，用逗号隔开"),
    user_id: int = Depends(get_current_user_id),
):
    """
    批量删除指标

    - 接受以逗号分隔的ID列表
    - 返回成功删除的ID列表及失败的ID列表
    """
    try:
        metric_ids = ids.split(",")
        deleted_ids = []
        failed_ids = []
        reason_map = {}

        for metric_id in metric_ids:
            try:
                metric_id = int(metric_id)

                # 检查指标是否存在
                metric_info = await metric_controller.get(id=metric_id)
                if not metric_info:
                    failed_ids.append(metric_id)
                    reason_map[metric_id] = "指标不存在"
                    continue

                # 删除指标
                result = await metric_controller.remove(id=metric_id)
                if result:
                    deleted_ids.append(metric_id)
                else:
                    failed_ids.append(metric_id)
                    reason_map[metric_id] = "删除失败"

            except Exception as e:
                failed_ids.append(int(metric_id))
                reason_map[int(metric_id)] = str(e)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricDelete,
            log_detail=f"批量删除指标: 成功IDs={deleted_ids}, 失败IDs={failed_ids}",
            by_user_id=user_id,
        )

        if failed_ids:
            return Success(
                msg=f"批量删除部分成功，{len(failed_ids)}个指标删除失败",
                data={
                    "deleted_ids": deleted_ids,
                    "failed_ids": failed_ids,
                    "reasons": reason_map,
                },
            )
        return Success(msg="批量删除成功", data={"deleted_ids": deleted_ids})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.MetricDelete,
            log_detail=f"批量删除指标失败: IDs={ids}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"批量删除指标失败: {str(e)}")
