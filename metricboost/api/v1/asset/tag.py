from typing import List, Optional

from cachetools import TTLCache
from fastapi import APIRouter, Body, Depends, Path, Query
from tortoise.expressions import Q

from metricboost.controllers.tag import tag_controller
from metricboost.core.ctx import get_current_user_id
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import insert_log
from metricboost.models.system import LogDetailType, LogType, User
from metricboost.schemas.tag import TagCreate, TagUpdate

router = APIRouter()

# 标签和指标标签的缓存
tag_cache = TTLCache(maxsize=200, ttl=300)  # 5分钟过期
metric_tag_cache = TTLCache(maxsize=300, ttl=180)  # 3分钟过期


@router.get("/tag", summary="获取标签信息")
async def get_tags(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量", alias="pageSize"),
    tagName: Optional[str] = Query(None, description="标签名称"),
    tagType: Optional[str] = Query(None, description="标签类型"),
    # with_metrics_count: bool = Query(False, description="是否返回关联的指标数量"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取标签信息列表

    - 支持按标签名称和类型搜索
    - 可选择是否返回关联的指标数量
    - 返回结果包含创建人信息
    """
    try:
        # 构建查询条件
        q = Q()
        if tagName:
            q &= Q(tag_name__contains=tagName)
        if tagType:
            q &= Q(tag_type=tagType)

        # 构建缓存键
        cache_key = f"tag_list_{tagType}_{tagName}_{page}_{page_size}"

        # 尝试从缓存获取数据
        if cache_key in tag_cache:
            total, data = tag_cache[cache_key]
        else:
            # 根据请求决定是否获取指标计数
            # if with_metrics_count:
            #     total, records = await tag_controller.get_tags_with_metrics_count(
            #         tag_type=tagType, page=page, page_size=size
            #     )
            #     data = {"records": records}
            # else:

            # 从数据库获取数据
            total, tag_objs = await tag_controller.get_list(
                page=page,
                page_size=page_size,
                search=q,
                order=["id"],
                # prefetch=["create_by"],
            )

            # 构建结果，包含创建人信息
            records = []
            for tag_obj in tag_objs:
                tag_dict = await tag_obj.to_dict()
                create_by = await tag_obj.create_by
                tag_dict.update(
                    {"createBy": create_by.user_name if create_by else "系统"}
                )
                records.append(tag_dict)

            data = {"records": records}

            # 存入缓存
            tag_cache[cache_key] = (total, data)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagGet,
            log_detail=f"获取标签列表，页码: {page}, 每页大小: {page_size}",
            by_user_id=user_id,
        )

        return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagGet,
            log_detail=f"获取标签列表失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"获取标签列表失败: {str(e)}")


@router.post("/tag", summary="创建标签信息")
async def create_tag(
    tag_in: TagCreate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    创建新的标签信息

    - 标签名称不能重复
    - 创建成功后返回新创建的标签ID
    """
    try:
        # 创建标签
        tag_in.create_by_id = user_id
        tag_in.update_by_id = user_id
        new_tag = await tag_controller.create(obj_in=tag_in)

        # 清除相关缓存
        keys_to_remove = [k for k in tag_cache.keys() if k.startswith("tag_list_")]
        for k in keys_to_remove:
            tag_cache.pop(k, None)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagCreate,
            log_detail=f"创建标签: {tag_in.tag_name}",
            by_user_id=user_id,
        )

        return Success(msg="创建成功", data={"create_id": new_tag.id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagCreate,
            log_detail=f"创建标签失败: {str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"创建标签失败: {str(e)}")


@router.patch("/tag/{tag_id}", summary="更新标签信息")
async def update_tag(
    tag_id: int = Path(..., description="标签ID"),
    tag_in: TagUpdate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    更新指定ID的标签信息

    - 如果更新标签名称，新名称不能与其他标签重复
    - 返回更新成功的标签ID
    """
    try:
        # 获取原始标签信息用于日志记录
        original_tag = await tag_controller.get(id=tag_id)
        if not original_tag:
            return Error(msg=f"标签ID {tag_id} 不存在")

        # 更新标签
        await tag_controller.update(id=tag_id, obj_in=tag_in)

        # 清除相关缓存
        keys_to_remove = [k for k in tag_cache.keys() if k.startswith("tag_list_")]
        for k in keys_to_remove:
            tag_cache.pop(k, None)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagUpdate,
            log_detail=f"更新标签: ID={tag_id}, 标签名={tag_in.tag_name or original_tag.tag_name}",
            by_user_id=user_id,
        )

        return Success(msg="更新成功", data={"update_id": tag_id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagUpdate,
            log_detail=f"更新标签失败: ID={tag_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"更新标签失败: {str(e)}")


@router.delete("/tag/{tag_id}", summary="删除标签信息")
async def delete_tag(
    tag_id: int = Path(..., description="标签ID"),
    user_id: int = Depends(get_current_user_id),
):
    """
    删除指定ID的标签信息

    - 如果标签已被指标关联，则不允许删除
    - 返回删除成功的标签ID
    """
    try:
        # 获取标签信息用于日志记录
        tag_info = await tag_controller.get(id=tag_id)

        # 删除标签
        await tag_controller.remove(id=tag_id)

        # 清除相关缓存
        keys_to_remove = [k for k in tag_cache.keys() if k.startswith("tag_list_")]
        for k in keys_to_remove:
            tag_cache.pop(k, None)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagDelete,
            log_detail=f"删除标签: ID={tag_id}, 标签名={tag_info.tag_name}",
            by_user_id=user_id,
        )

        return Success(msg="删除成功", data={"delete_id": tag_id})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagDelete,
            log_detail=f"删除标签失败: ID={tag_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"删除标签失败: {str(e)}")


@router.delete("/tag", summary="批量删除标签信息")
async def batch_delete_tag(
    ids: str = Query(..., description="标签ID列表，用逗号隔开"),
    user_id: int = Depends(get_current_user_id),
):
    """
    批量删除标签信息

    - 查询参数ids需要包含以逗号分隔的ID列表
    - 如有任一标签被指标关联，则该标签不会被删除
    - 返回成功和失败的ID列表
    """
    try:
        tag_ids = ids.split(",")
        deleted_ids = []
        failed_ids = []
        reason_map = {}

        for tag_id in tag_ids:
            try:
                tag_id = int(tag_id)

                # 删除标签
                await tag_controller.remove(id=tag_id)
                deleted_ids.append(tag_id)

            except Exception as e:
                failed_ids.append(int(tag_id))
                reason_map[int(tag_id)] = str(e)

        # 清除相关缓存
        keys_to_remove = [k for k in tag_cache.keys() if k.startswith("tag_list_")]
        for k in keys_to_remove:
            tag_cache.pop(k, None)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TagDelete,
            log_detail=f"批量删除标签: 成功IDs={deleted_ids}, 失败IDs={failed_ids}",
            by_user_id=user_id,
        )

        return Success(
            msg="批量删除成功",
            data={"deleted_ids": deleted_ids, "failed_ids": failed_ids},
        )
    except Exception as e:
        return Error(msg=f"批量删除失败: {str(e)}")


# @router.get(
#     "/metric-tag",
#     summary="获取指标的标签信息",
# )
# async def get_metric_tags(
#     metricIds: Optional[List[int]] = Query(None, description="指标ID列表"),
#     tagName: Optional[str] = Query(None, description="标签名称"),
#     user_id: int = Depends(get_current_user_id),
# ):
#     """
#     获取指标的标签信息

#     - 可通过指标ID列表过滤
#     - 可通过标签名称过滤
#     - 返回结果使用缓存提高性能
#     """
#     try:
#         # 构建缓存键
#         metric_ids_str = "_".join(map(str, metricIds)) if metricIds else "all"
#         cache_key = f"metric_tag_list_{metric_ids_str}_{tagName or 'all'}"

#         # 尝试从缓存获取数据
#         if cache_key in metric_tag_cache:
#             total, metric_tag_objs = metric_tag_cache[cache_key]
#         else:
#             # 从数据库获取数据
#             total, metric_tag_objs = await tag_controller.get_list(
#                 metric_ids=metricIds, tag_name=tagName
#             )

#             # 存入缓存
#             metric_tag_cache[cache_key] = (total, metric_tag_objs)

#         data = {"records": metric_tag_objs}

#         # 记录日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagGet,
#             log_detail=f"获取标签指标关联信息: 指标IDs={metricIds}, 标签名={tagName}",
#             by_user_id=user_id,
#         )

#         return SuccessExtra(total=total, data=data)

#     except Exception as e:
#         # 记录错误日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagGet,
#             log_detail=f"获取标签指标关联信息失败: {str(e)}",
#             by_user_id=user_id,
#         )
#         return Error(msg=f"获取标签指标关联信息失败: {str(e)}")


# @router.post("/metric-tag", summary="创建标签指标信息")
# async def create_metric_tag(
#     metric_tag_in: MetricTagCreate = Body(...),
#     user_id: int = Depends(get_current_user_id),
# ):
#     """
#     创建新的标签指标关联

#     - 指标ID必须存在
#     - 标签必须存在
#     - 同一指标不能关联相同标签多次
#     """
#     try:
#         # 创建标签指标关联
#         new_metric_tag = await metric_tag_controller.create(
#             obj_in=metric_tag_in, user_id=user_id
#         )

#         # 清除相关缓存
#         keys_to_remove = [k for k in metric_tag_cache.keys()]
#         for k in keys_to_remove:
#             metric_tag_cache.pop(k, None)

#         # 记录日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagCreate,
#             log_detail=f"创建标签指标关联: 指标ID={metric_tag_in.metric_id}, 标签={metric_tag_in.tag}",
#             by_user_id=user_id,
#         )

#         return Success(msg="创建成功", data={"create_id": new_metric_tag.id})

#     except ValueError as e:
#         # 记录验证错误
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagCreate,
#             log_detail=f"创建标签指标关联验证失败: {str(e)}",
#             by_user_id=user_id,
#         )
#         return Error(msg=str(e))

#     except Exception as e:
#         # 记录其他错误
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagCreate,
#             log_detail=f"创建标签指标关联失败: {str(e)}",
#             by_user_id=user_id,
#         )
#         return Error(msg=f"创建标签指标关联失败: {str(e)}")


# @router.delete("/metric-tag", summary="删除标签指标信息")
# async def delete_metric_tag(
#     metricId: int = Query(..., description="指标ID"),
#     tag: str = Query(..., description="标签名称"),
#     user_id: int = Depends(get_current_user_id),
# ):
#     """
#     删除指定的标签指标关联

#     - 需同时指定指标ID和标签名称
#     - 返回删除成功的信息
#     """
#     try:
#         # 删除标签指标关联
#         result = await metric_tag_controller.remove(metric_id=metricId, tag=tag)
#         if not result:
#             return Error(msg=f"未找到指标ID[{metricId}]和标签[{tag}]的关联")

#         # 清除相关缓存
#         keys_to_remove = [k for k in metric_tag_cache.keys()]
#         for k in keys_to_remove:
#             metric_tag_cache.pop(k, None)

#         # 记录日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagDelete,
#             log_detail=f"删除标签指标关联: 指标ID={metricId}, 标签={tag}",
#             by_user_id=user_id,
#         )

#         return Success(
#             msg="删除成功", data={"delete_id": f"指标id[{metricId}]，标签[{tag}]"}
#         )

#     except Exception as e:
#         # 记录错误日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagDelete,
#             log_detail=f"删除标签指标关联失败: 指标ID={metricId}, 标签={tag}, 错误={str(e)}",
#             by_user_id=user_id,
#         )
#         return Error(msg=f"删除标签指标关联失败: {str(e)}")


# @router.post("/metric-tag/batch", summary="批量创建标签指标信息")
# async def batch_create_metric_tag(
#     metric_tag_list: List[MetricTagCreate] = Body(...),
#     user_id: int = Depends(get_current_user_id),
# ):
#     """
#     批量创建标签指标关联

#     - 请求体包含多个标签指标关联对象
#     - 返回成功创建的ID列表和失败项
#     """
#     try:
#         created_ids = []
#         failed_items = []

#         for item in metric_tag_list:
#             try:
#                 new_metric_tag = await metric_tag_controller.create(
#                     obj_in=item, user_id=user_id
#                 )
#                 created_ids.append(new_metric_tag.id)
#             except Exception as inner_e:
#                 failed_items.append(
#                     {
#                         "metric_id": item.metric_id,
#                         "tag": item.tag,
#                         "reason": str(inner_e),
#                     }
#                 )

#         # 清除相关缓存
#         keys_to_remove = [k for k in metric_tag_cache.keys()]
#         for k in keys_to_remove:
#             metric_tag_cache.pop(k, None)

#         # 记录日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagCreate,
#             log_detail=f"批量创建标签指标关联: 成功数量={len(created_ids)}, 失败数量={len(failed_items)}",
#             by_user_id=user_id,
#         )

#         if failed_items:
#             return Success(
#                 msg=f"批量创建部分成功，{len(failed_items)}项失败",
#                 data={"created_ids": created_ids, "failed_items": failed_items},
#             )
#         return Success(msg="批量创建成功", data={"created_ids": created_ids})

#     except Exception as e:
#         # 记录错误日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagCreate,
#             log_detail=f"批量创建标签指标关联失败: {str(e)}",
#             by_user_id=user_id,
#         )
#         return Error(msg=f"批量创建标签指标关联失败: {str(e)}")


# @router.delete("/metric-tag/batch", summary="批量删除标签指标信息")
# async def batch_delete_metric_tag(
#     items: List[dict] = Body(..., description="指标ID和标签名称列表"),
#     user_id: int = Depends(get_current_user_id),
# ):
#     """
#     批量删除标签指标关联

#     - 请求体包含多个指标ID和标签名称对象
#     - 对象格式: {metricId: 1, tag: 'tag1'}
#     - 返回成功和失败的项目列表
#     """
#     try:
#         deleted_items = []
#         failed_items = []

#         for item in items:
#             try:
#                 metric_id = item.get("metricId")
#                 tag = item.get("tag")

#                 if not metric_id or not tag:
#                     failed_items.append(
#                         {"metric_id": metric_id, "tag": tag, "reason": "缺少必要参数"}
#                     )
#                     continue

#                 result = await metric_tag_controller.remove(
#                     metric_id=metric_id, tag=tag
#                 )
#                 if result:
#                     deleted_items.append({"metric_id": metric_id, "tag": tag})
#                 else:
#                     failed_items.append(
#                         {"metric_id": metric_id, "tag": tag, "reason": "关联不存在"}
#                     )
#             except Exception as inner_e:
#                 failed_items.append(
#                     {
#                         "metric_id": item.get("metricId"),
#                         "tag": item.get("tag"),
#                         "reason": str(inner_e),
#                     }
#                 )

#         # 清除相关缓存
#         keys_to_remove = [k for k in metric_tag_cache.keys()]
#         for k in keys_to_remove:
#             metric_tag_cache.pop(k, None)

#         # 记录日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagDelete,
#             log_detail=f"批量删除标签指标关联: 成功数量={len(deleted_items)}, 失败数量={len(failed_items)}",
#             by_user_id=user_id,
#         )

#         if failed_items:
#             return Success(
#                 msg=f"批量删除部分成功，{len(failed_items)}项失败",
#                 data={"deleted_items": deleted_items, "failed_items": failed_items},
#             )
#         return Success(msg="批量删除成功", data={"deleted_items": deleted_items})

#     except Exception as e:
#         # 记录错误日志
#         await insert_log(
#             log_type=LogType.SystemLog,
#             log_detail_type=LogDetailType.MetricTagDelete,
#             log_detail=f"批量删除标签指标关联失败: {str(e)}",
#             by_user_id=user_id,
#         )
#         return Error(msg=f"批量删除标签指标关联失败: {str(e)}")
