import json
from fastapi import APIRouter, Query, Request
from tortoise.expressions import Q
from app.schemas.base import SuccessExtra, Success
from app.controllers import data_model_controller
from app.models.system import LogType, LogDetailType, User
from app.api.v1.utils import insert_log
from app.schemas.data_model import DataModelCreate, DataModelUpdate
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/model", summary="获取主题模型信息")
async def _(
    request: Request,
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    status: str = Query(None, description="模型状态"),
    dataModelName: str = Query(None, description="模型名称"),
    createBy: str = Query(None, description="创建人"),
):
    params = dict(request.query_params)

    # 提取dataDomainList参数
    dataDomainList = []
    topicDomainList = []

    for key, value in params.items():
        if key.startswith("dataDomainList["):
            dataDomainList.append(int(value))
        if key.startswith("topicDomainList["):
            topicDomainList.append(int(value))

    q = Q()  # Q() 是一个查询构造器，用于构建复杂的数据库查询条件
    # 进行模型状态的筛选
    if status:
        q &= Q(status__contains=status)

    # 进行模型名称的筛选
    if dataModelName:
        q &= Q(data_model_name__contains=dataModelName)

    # 进行数据域筛选
    if dataDomainList:
        q &= Q(data_domain_id__in=dataDomainList)

    # 进行主题域筛选
    if topicDomainList:
        q &= Q(topic_domain_id__in=topicDomainList)

    # 进行创建人的筛选
    if createBy:
        q &= Q(create_by__user_name=createBy)

    total, data_model_objs = await data_model_controller.list(
        page=current,
        page_size=size,
        search=q,
        order=["id"],
    )
    records = []
    for data_model_obj in data_model_objs:
        # 构建基础数据字典
        data_model_dict = await data_model_obj.to_dict()

        # 获取用户关联数据
        create_by = await data_model_obj.create_by

        # 添加关联字段
        data_model_dict.update(
            {
                "createBy": create_by.user_name,
                "dataDomain": data_model_obj.data_domain_id,
                "topicDomain": data_model_obj.topic_domain_id,
                "database": data_model_obj.database_id,
                "fieldConf": (
                    json.loads(data_model_obj.field_conf)
                    if data_model_obj.field_conf
                    else None
                ),
            }
        )
        records.append(data_model_dict)

    data = {"records": records}
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataModelGet,
        by_user_id=0,
    )
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.post("/model", summary="创建主题模型信息")
async def _(
    data_model_in: DataModelCreate,
):
    new_data_model = await data_model_controller.create(obj_in=data_model_in)

    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataModelCreate,
        by_user_id=0,
    )
    return Success(msg="创建成功", data={"create_id": new_data_model.id})


@router.patch("/model/{id}", summary="更新主题模型信息")
async def _(
    id: int,
    data_model_in: DataModelUpdate,
):
    await data_model_controller.update(id=id, obj_in=data_model_in)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataModelUpdate,
        by_user_id=0,
    )
    return Success(msg="更新成功", data={"update_id": id})


@router.delete("/model/{id}", summary="删除主题模型信息")
async def _(
    id: int,
):
    await data_model_controller.remove(id=id)
    await insert_log(
        log_type=LogType.SystemLog,
        log_detail_type=LogDetailType.DataModelDelete,
        by_user_id=0,
    )
    return Success(msg="删除成功", data={"delete_id": id})


@router.get("/model/preview", summary="预览数据")
async def _(
    databaseId: str = Query(None, description="数据库ID"),
    tableName: str = Query(None, description="表名"),
    addOrEdit: str = Query(None, description="新增或编辑"),
):

    total, response = await data_model_controller.fetch_table_data(
        databaseId, tableName
    )
    _, columns = await data_model_controller.fetch_columns_metadata(
        databaseId, tableName, addOrEdit
    )
    return Success(
        msg="预览成功",
        total=total,
        columns=columns,
        data={"records": jsonable_encoder(response)},
    )


@router.get("/model/tables", summary="获取表的元数据")
async def _(database: str = Query(None, description="数据库ID")):
    total, data = await data_model_controller.fetch_tables_metadata(database)
    return Success(msg="获取元数据成功", total=total, data={"records": data})


@router.get("/model/tables/columns", summary="获取表的字段元数据")
async def _(
    database: str = Query(None, description="数据库ID"),
    tableName: str = Query(None, description="表名"),
    addOrEdit: str = Query(None, description="新增或编辑"),
):
    total, data = await data_model_controller.fetch_columns_metadata(
        database, tableName, addOrEdit
    )

    return Success(msg="获取元数据成功", total=total, data={"records": data})


@router.get("/model/aggregate-data", summary="获取表的聚合数据")
async def _(
    data_model_id: str = Query(None, description="数据模型ID"),
    statistic_column: str = Query(None, description="统计字段"),
    statistic_type: str = Query(None, description="统计方式"),
    aggregated_column: str = Query(None, description="聚合字段"),
):
    total, data = await data_model_controller.fetch_aggregate_data(
        data_model_id, statistic_column, statistic_type, aggregated_column
    )
    return Success(
        msg="获取聚合数据成功", total=total, data=jsonable_encoder({"records": data})
    )
