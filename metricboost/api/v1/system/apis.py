from fastapi import APIRouter, Query
from fastapi.routing import APIRoute
from tortoise.expressions import Q

from metricboost.controllers.api import api_controller
from metricboost.controllers.user import user_controller
from metricboost.core.ctx import CTX_USER_ID
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import get_logger, insert_log
from metricboost.models.enums import LogDetailType, LogType
from metricboost.models.system import Api, Role
from metricboost.schemas.apis import ApiCreate, ApiUpdate

logger = get_logger(__name__)
router = APIRouter()


async def refresh_api_list():
    from metricboost.app import app

    existing_apis = [(str(api.method.value), api.path) for api in await Api.all()]

    app_routes = [route for route in app.routes if isinstance(route, APIRoute)]
    app_routes_compared = [
        (list(route.methods)[0].lower(), route.path_format) for route in app_routes
    ]

    for method, path in set(existing_apis) - set(app_routes_compared):
        logger.error(f"API Deleted {method} {path}")
        await Api.filter(method=method, path=path).delete()

    for route in app_routes:
        method = list(route.methods)[0].lower()
        path = route.path_format
        summary = route.summary
        tags = list(route.tags)
        await Api.update_or_create(
            path=path, method=method, defaults=dict(summary=summary, tags=tags)
        )


@router.get("/apis", summary="查看API列表")
async def _(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量", alias="pageSize"),
    path: str = Query(None, description="API路径"),
    summary: str = Query(None, description="API简介"),
    tags: str = Query(None, description="API模块"),
    status: str = Query(None, description="API状态"),
):
    q = Q()
    if path:
        q &= Q(path__contains=path)
    if summary:
        q &= Q(summary__contains=summary)
    if tags:
        q &= Q(tags__contains=tags.split("|"))
    if status:
        q &= Q(status__contains=status)

    user_id = CTX_USER_ID.get()
    user_obj = await user_controller.get(id=user_id)
    if not user_obj:
        return Error(msg="用户不存在")
    user_role_objs: list[Role] = await user_obj.roles
    user_role_codes = [role_obj.role_code for role_obj in user_role_objs]
    if "R_SUPER" in user_role_codes:
        total, api_objs = await api_controller.get_list(
            page=page,
            page_size=page_size,
            search=q,
            order=["tags", "id"],
        )
    else:
        api_objs: list[Api] = []
        for role_obj in user_role_objs:
            api_objs.extend([api_obj for api_obj in await role_obj.apis])

        unique_apis = list(set(api_objs))
        sorted_menus = sorted(unique_apis, key=lambda x: x.id)
        # 实现分页
        start = (page - 1) * page_size
        end = start + page_size
        api_objs = sorted_menus[start:end]
        total = len(sorted_menus)

    records = []
    for obj in api_objs:
        data = await obj.to_dict(exclude_fields=["create_time", "update_time"])
        data["tags"] = "|".join(data["tags"])
        records.append(data)
    data = {"records": records}
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiGetList,
        log_detail="查看API列表",
        by_user_id=user_obj.id,
    )
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/apis/{api_id}", summary="查看API")
async def _(api_id: int):
    api_obj = await api_controller.get(id=api_id)
    if not api_obj:
        return Error(msg="API不存在")
    data = await api_obj.to_dict(exclude_fields=["id", "create_time", "update_time"])
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiGetOne,
        log_detail="查看API详情",
        by_user_id=0,
    )
    return Success(data=data)


def build_api_tree(apis: list[Api]):
    parent_map = {"root": {"id": "root", "children": []}}
    # 遍历输入数据
    for api in apis:
        tags = api.tags
        parent_id = "root"
        for tag in tags:
            node_id = f"parent${tag}"
            # 如果当前节点不存在，则创建一个新的节点
            if node_id not in parent_map:
                node = {"id": node_id, "summary": tag, "children": []}
                parent_map[node_id] = node
                parent_map[parent_id]["children"].append(node)
            parent_id = node_id
        parent_map[parent_id]["children"].append(
            {
                "id": api.id,
                "summary": api.summary,
            }
        )
    return parent_map["root"]["children"]


@router.get("/apis/tree/", summary="查看API树")
async def _():
    api_objs = await Api.all()
    data = []
    if api_objs:
        data = build_api_tree(api_objs)
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiGetTree,
        log_detail="查看API树",
        by_user_id=0,
    )
    return Success(data=data)


@router.post("/apis", summary="创建API")
async def _(
    api_in: ApiCreate,
):
    if isinstance(api_in.tags, str):
        api_in.tags = api_in.tags.split("|")
    new_api = await api_controller.create(obj_in=api_in)
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiCreateOne,
        log_detail="创建API",
        by_user_id=0,
    )
    return Success(msg="Created Successfully", data={"created_id": new_api.id})


@router.patch("/apis/{api_id}", summary="更新API")
async def _(
    api_id: int,
    api_in: ApiUpdate,
):
    if isinstance(api_in.tags, str):
        api_in.tags = api_in.tags.split("|")
    await api_controller.update(id=api_id, obj_in=api_in)
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiUpdateOne,
        log_detail="更新API",
        by_user_id=0,
    )
    return Success(msg="Update Successfully", data={"updated_id": api_id})


@router.delete("/apis/{api_id}", summary="删除API")
async def _(
    api_id: int,
):
    await api_controller.remove(id=api_id)
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiDeleteOne,
        log_detail="删除API",
        by_user_id=0,
    )
    return Success(msg="Deleted Successfully", data={"deleted_id": api_id})


@router.delete("/apis", summary="批量删除API")
async def _(ids: str = Query(..., description="API ID列表, 用逗号隔开")):
    api_ids = ids.split(",")
    deleted_ids = []
    for api_id in api_ids:
        api_obj = await Api.get(id=int(api_id))
        await api_obj.delete()
        deleted_ids.append(int(api_id))
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiBatchDelete,
        log_detail="批量删除API",
        by_user_id=0,
    )
    return Success(msg="Deleted Successfully", data={"deleted_ids": deleted_ids})


@router.post("/apis/refresh/", summary="刷新API列表")
async def _():
    await refresh_api_list()
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.ApiRefresh,
        log_detail="刷新API列表",
        by_user_id=0,
    )
    return Success()
