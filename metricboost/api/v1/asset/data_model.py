import json
from typing import Optional

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from tortoise.expressions import Q

from metricboost.controllers.model import data_model_controller
from metricboost.core.ctx import get_current_user_id
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import get_logger, insert_log
from metricboost.models.enums import EditMode
from metricboost.models.system import LogDetailType, LogType
from metricboost.schemas.model import DataModelCreate, DataModelUpdate

logger = get_logger(__name__)

router = APIRouter()


@router.get("/model", summary="获取主题模型信息")
async def get_models(
    page: int = Query(1, description="页码", ge=1),
    page_size: int = Query(10, description="每页数量", ge=1, alias="pageSize"),
    status: Optional[str] = Query(None, description="模型状态"),
    name: Optional[str] = Query(None, description="模型名称"),
    database_id: Optional[int] = Query(
        None, description="数据库ID", alias="databaseId"
    ),
    domain_ids: Optional[list] = Query(None, description="域ID列表", alias="domainIds"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取主题模型信息列表

    - 支持按模型状态、名称和数据库ID筛选
    - 支持通过请求参数传递dataDomainList和topicDomainList进行过滤
    """
    try:

        # 构建查询条件
        q = Q()
        if status:
            q &= Q(status=status)
        if name:
            q &= Q(name__contains=name)
        if database_id:
            q &= Q(database_id=database_id)
        if domain_ids:
            # 方法1：使用正确的关系查询语法
            q &= Q(domains__id__in=domain_ids)
        # 获取数据
        total, data_model_objs = await data_model_controller.get_list(
            page=page,
            page_size=page_size,
            search=q,
            order=["id"],
            prefetch=["database", "update_by", "create_by", "domains"],
        )

        # 转换为响应格式
        records = []
        for data_model_obj in data_model_objs:
            # 构建基础数据字典
            data_model_dict = await data_model_obj.to_dict()
            try:
                columns_conf = eval(data_model_obj.columns_conf)
            except Exception:
                columns_conf = []
            # 添加关联字段
            data_model_dict.update(
                {
                    "updateBy": data_model_obj.update_by.user_name,
                    "createBy": data_model_obj.create_by.user_name,
                    "database": data_model_obj.database.name,
                    "columnsConf": columns_conf,
                    "dataDomains": [
                        domain.id
                        for domain in data_model_obj.domains
                        if domain.domain_type == "1"
                    ],
                    "topicDomains": [
                        domain.id
                        for domain in data_model_obj.domains
                        if domain.domain_type == "2"
                    ],
                }
            )
            records.append(data_model_dict)

        data = {"records": records}

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelGet,
            log_detail=f"获取主题模型列表: 页码={page}, 每页={page_size}",
            by_user_id=user_id,
        )

        return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelGet,
            log_detail=f"获取主题模型列表失败: {str(e)}",
            by_user_id=user_id,
        )
        logger.error(f"获取主题模型列表失败: {str(e)}")
        return Error(msg=f"获取主题模型列表失败: {str(e)}")


@router.post("/model", summary="创建主题模型信息")
async def create_model(
    data_model_in: DataModelCreate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    创建新的主题模型信息

    - 必须指定有效的数据库ID、数据域ID和主题域ID
    - 表名在同一数据库中不能重复
    """
    try:
        data_model_in.create_by_id = user_id
        data_model_in.update_by_id = user_id

        # 创建主题模型
        new_data_model = await data_model_controller.create(
            obj_in=data_model_in, exclude={"domain_ids"}
        )

        # 更新主题模型关联的域ID
        await data_model_controller.update_domain_ids(
            new_data_model, data_model_in.domain_ids
        )

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelCreate,
            log_detail=f"创建主题模型: 名称={data_model_in.name}, 表名={data_model_in.table_name}",
            by_user_id=user_id,
        )

        return Success(msg="创建成功", data={"create_id": new_data_model.id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelCreate,
            log_detail=f"创建主题模型失败: {str(e)}",
            by_user_id=user_id,
        )
        logger.error(f"创建主题模型失败: {str(e)}")
        return Error(msg=f"创建主题模型失败: {str(e)}")


@router.patch("/model/{id}", summary="更新主题模型信息")
async def update_model(
    id: int = Path(..., description="模型ID"),
    data_model_in: DataModelUpdate = Body(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    更新指定ID的主题模型信息

    - 如果更新表名，必须确保在同一数据库中不重复
    - 可以更新字段配置和关联的域信息
    """
    try:
        # 获取原始数据用于日志记录
        data_model_in.update_by_id = user_id
        original = await data_model_controller.get(id=id)
        if not original:
            return Error(msg=f"主题模型ID {id} 不存在")

        # 更新模型
        new_model = await data_model_controller.update(
            id=id, obj_in=data_model_in, exclude={"domain_ids"}
        )

        # 更新主题模型关联的域ID
        await data_model_controller.update_domain_ids(
            new_model, data_model_in.domain_ids
        )

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelUpdate,
            log_detail=f"更新主题模型: ID={id}, 名称={data_model_in.name or original.name}",
            by_user_id=user_id,
        )

        return Success(msg="更新成功", data={"update_id": id})

    except Exception as e:
        # 记录其他错误
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelUpdate,
            log_detail=f"更新主题模型失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"更新主题模型失败: {str(e)}")


@router.delete("/model/{id}", summary="删除主题模型信息")
async def delete_model(
    id: int = Path(..., description="模型ID"),
    user_id: int = Depends(get_current_user_id),
):
    """
    删除指定ID的主题模型信息

    - 如果模型已被指标关联，可能会导致删除失败
    """
    try:
        # 获取原始数据用于日志记录
        model_info = await data_model_controller.get(id=id)
        if not model_info:
            return Error(msg=f"主题模型ID {id} 不存在")

        # 删除模型
        await data_model_controller.remove(id=id)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelDelete,
            log_detail=f"删除主题模型: ID={id}, 名称={model_info.name}",
            by_user_id=user_id,
        )

        return Success(msg="删除成功", data={"delete_id": id})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataModelDelete,
            log_detail=f"删除主题模型失败: ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"删除主题模型失败: {str(e)}")


@router.get("/model/preview", summary="预览数据")
async def preview_model_data(
    databaseId: int = Query(..., description="数据库ID"),
    tableName: str = Query(..., description="表名"),
    page: int = Query(1, description="页码"),
    pageSize: int = Query(10, description="每页数量"),
    user_id: int = Depends(get_current_user_id),
):
    """
    预览数据模型中的数据

    - 返回指定表的数据和列信息
    - addOrEdit参数可选"add"或"edit"，决定是否加载已有配置
    """
    try:
        # 获取表数据
        total, response = await data_model_controller.fetch_table_preview(
            databaseId, tableName, page, pageSize
        )
        if not total:
            return Error(msg="表不存在或无数据")

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataPreview,
            log_detail=f"预览数据: 数据库ID={databaseId}, 表名={tableName}",
            by_user_id=user_id,
        )

        return SuccessExtra(
            msg="预览成功",
            total=total,
            page=page,
            size=pageSize,
            data={"records": jsonable_encoder(response)},
        )

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.DataPreview,
            log_detail=f"预览数据失败: 数据库ID={databaseId}, 表名={tableName}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"预览数据失败: {str(e)}")


@router.get("/model/tables", summary="获取表的元数据")
async def get_tables_metadata(
    database_id: int = Query(..., description="数据库ID", alias="databaseId"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取指定数据库中所有表的元数据

    - 返回表名和表注释

    """
    try:
        data = await data_model_controller.fetch_table_metadata(database_id)

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TableMetadata,
            log_detail=f"获取表元数据: 数据库ID={database_id}",
            by_user_id=user_id,
        )

        return Success(msg="获取元数据成功", data={"records": data})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.TableMetadata,
            log_detail=f"获取表元数据失败: 数据库ID={database_id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"获取表元数据失败: {str(e)}")


@router.get("/model/tables/columns", summary="获取表的字段元数据")
async def get_columns_metadata(
    database_id: int = Query(..., description="数据库ID", alias="databaseId"),
    table_name: str = Query(..., description="表名", alias="tableName"),
    edit_mode: EditMode = Query(..., description="编辑模式", alias="editMode"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取指定表的字段元数据

    - 返回字段名、类型和注释
    - 如果是编辑模式，会加载已有的字段配置
    """
    try:
        data = await data_model_controller.fetch_column_metadata(
            database_id, table_name, edit_mode
        )

        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ColumnMetadata,
            log_detail=f"获取字段元数据: 数据库ID={database_id}, 表名={table_name}",
            by_user_id=user_id,
        )

        return Success(msg="获取字段元数据成功", data={"records": data})

    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ColumnMetadata,
            log_detail=f"获取字段元数据失败: 数据库ID={database_id}, 表名={table_name}, 错误={str(e)}",
            by_user_id=user_id,
        )
        return Error(msg=f"获取字段元数据失败: {str(e)}")
