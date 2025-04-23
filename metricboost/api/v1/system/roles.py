from fastapi import APIRouter, Query
from tortoise.expressions import Q

from metricboost.controllers.menu import menu_controller
from metricboost.controllers.role import role_controller
from metricboost.core.exceptions import HTTPException
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import insert_log
from metricboost.models.system import Api, Button, LogDetailType, LogType, Role
from metricboost.schemas.roles import RoleCreate, RoleUpdate, RoleUpdateAuthrization

router = APIRouter()


@router.get("/roles", summary="查看角色列表")
async def _(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量", alias="pageSize"),
    roleName: str = Query(None, description="角色名称"),
    roleCode: str = Query(None, description="角色编码"),
    status: str = Query(None, description="用户状态"),
):
    q = Q()
    if roleName:
        q &= Q(role_name__contains=roleName)
    if roleCode:
        q &= Q(role_code__contains=roleCode)
    if status:
        q &= Q(status__contains=status)

    total, role_objs = await role_controller.get_list(
        page=page,
        page_size=page_size,
        search=q,
        order=["id"],
    )
    records = [
        await role_obj.to_dict(exclude_fields=["role_desc"]) for role_obj in role_objs
    ]
    data = {"records": records}
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleGetList,
        log_detail="查看角色列表",
        by_user_id=0,
    )
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/roles/{role_id}", summary="查看角色")
async def get_role(role_id: int):
    role_obj: Role = await role_controller.get(id=role_id)
    if not role_obj:
        return Error(msg="角色不存在")
    data = await role_obj.to_dict()
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleGetOne,
        log_detail="查看角色",
        by_user_id=0,
    )
    return Success(data=data)


@router.post("/roles", summary="创建角色")
async def _(role_in: RoleCreate):
    role = await role_controller.model.exists(role_code=role_in.role_code)
    if role:
        return Error(code="4090", msg="角色编码已存在")

    new_user = await role_controller.create(obj_in=role_in)
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleCreateOne,
        log_detail="创建角色",
        by_user_id=0,
    )
    return Success(msg="Created Successfully", data={"created_id": new_user.id})


@router.patch("/roles/{role_id}", summary="更新角色")
async def _(role_id: int, role_in: RoleUpdate):
    await role_controller.update(id=role_id, obj_in=role_in)
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleUpdateOne,
        log_detail="更新角色",
        by_user_id=0,
    )
    return Success(msg="Updated Successfully", data={"updated_id": role_id})


@router.delete("/roles/{role_id}", summary="删除角色")
async def _(role_id: int):
    await role_controller.remove(id=role_id)
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleDeleteOne,
        log_detail="删除角色",
        by_user_id=0,
    )
    return Success(msg="Deleted Successfully", data={"deleted_id": role_id})


@router.delete("/roles", summary="批量删除角色")
async def _(ids: str = Query(..., description="角色ID列表, 用逗号隔开")):
    role_ids = ids.split(",")
    deleted_ids = []
    for role_id in role_ids:
        role_obj = await role_controller.get(id=int(role_id))
        await role_obj.delete()
        deleted_ids.append(int(role_id))
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleBatchDeleteOne,
        log_detail="批量删除角色",
        by_user_id=0,
    )
    return Success(msg="Deleted Successfully", data={"deleted_ids": deleted_ids})


@router.get("/roles/{role_id}/menus", summary="查看角色菜单")
async def _(role_id: int):
    role_obj = await role_controller.get(id=role_id)
    if role_obj.role_code == "R_SUPER":
        menu_objs = await menu_controller.model.filter(constant=False)
    else:
        menu_objs = await role_obj.menus
    data = {
        "roleHome": role_obj.role_home,
        "menuIds": [menu_obj.id for menu_obj in menu_objs],
    }
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleGetMenus,
        log_detail="查看角色菜单",
        by_user_id=0,
    )
    return Success(data=data)


@router.patch("/roles/{role_id}/menus", summary="更新角色菜单")
async def _(role_id: int, role_in: RoleUpdateAuthrization):
    if role_in.role_home is not None:
        role_obj = await role_controller.update(
            id=role_id, obj_in=dict(role_home=role_in.role_home)
        )
        if role_in.menu_ids:
            await role_obj.menus.clear()
            for menu_id in role_in.menu_ids:
                menu_objs = [await menu_controller.get(id=menu_id)]
                if not menu_objs:
                    raise Exception(msg="菜单不存在", code=400)
                while len(menu_objs) > 0:
                    menu_obj = menu_objs.pop()
                    await role_obj.menus.add(menu_obj)
                    if menu_obj.parent_id != 0:  # 子节点
                        menu_objs.append(
                            await menu_controller.get(id=menu_obj.parent_id)
                        )  # 父节点

    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleUpdateMenus,
        log_detail="更新角色菜单",
        by_user_id=0,
    )
    return Success(
        msg="Updated Successfully",
        data={
            "updated_menu_ids": role_in.menu_ids,
            "updated_role_home": role_in.role_home,
        },
    )


@router.get("/roles/{role_id}/buttons", summary="查看角色按钮")
async def _(role_id: int):
    role_obj = await role_controller.get(id=role_id)
    if role_obj.role_code == "R_SUPER":
        button_objs = await Button.all()
    else:
        button_objs = await role_obj.buttons

    data = {"buttonIds": [button_obj.id for button_obj in button_objs]}
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleGetButtons,
        log_detail="查看角色按钮",
        by_user_id=0,
    )
    return Success(data=data)


@router.patch("/roles/{role_id}/buttons", summary="更新角色按钮")
async def _(role_id: int, role_in: RoleUpdateAuthrization):
    role_obj = await role_controller.get(id=role_id)
    if role_in.button_ids is not None:
        await role_obj.buttons.clear()
        for button_id in role_in.button_ids:
            button_obj = await Button.get(id=button_id)
            await role_obj.buttons.add(button_obj)

    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleUpdateButtons,
        log_detail="更新角色按钮",
        by_user_id=0,
    )
    return Success(msg="Updated Successfully", data={"button_ids": role_in.button_ids})


@router.get("/roles/{role_id}/apis", summary="查看角色API")
async def _(role_id: int):
    role_obj = await role_controller.get(id=role_id)
    if role_obj.role_code == "R_SUPER":
        api_objs = await Api.all()
    else:
        api_objs = await role_obj.apis

    data = {"apiIds": [api_obj.id for api_obj in api_objs]}
    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleGetApis,
        log_detail="查看角色API",
        by_user_id=0,
    )
    return Success(data=data)


@router.patch("/roles/{role_id}/apis", summary="更新角色API")
async def _(role_id: int, role_in: RoleUpdateAuthrization):
    role_obj = await role_controller.get(id=role_id)
    if role_in.api_ids is None:
        return Error(msg="No APIs to update")
    await role_obj.apis.clear()
    for api_id in role_in.api_ids:
        api_obj = await Api.get(id=api_id)
        await role_obj.apis.add(api_obj)

    await insert_log(
        log_type=LogType.AdminLog,
        log_detail_type=LogDetailType.RoleUpdateApis,
        log_detail="更新角色API",
        by_user_id=0,
    )
    return Success(msg="Updated Successfully", data={"api_ids": role_in.api_ids})
