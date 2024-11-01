from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.schemas.base import SuccessExtra, Success
from app.controllers import data_model_controller
from app.models.system import LogType, LogDetailType, User, DataDomain, TopicDomain
from app.api.v1.utils import insert_log
from app.schemas.data_model import DataModelCreate, DataModelUpdate
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/data-model", summary="获取主题模型信息")
async def _(
    current: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量"),
    status: str = Query(None, description="数据库状态"),
    dataModelName: str = Query(None, description="模型名称"),
    dataDomain: str = Query(None, description="数据域"),
    topicDomain: str = Query(None, description="主题域"),
    createBy: str = Query(None, description="创建人"),
):
    q = Q()  # Q() 是一个查询构造器，用于构建复杂的数据库查询条件
    if status:
        q &= Q(status__contains=status)
    if dataModelName:
        q &= Q(data_model_name__contains=dataModelName)
    if dataDomain:
        data_domain = await DataDomain.get_or_none(data_domain_name=dataDomain)
        if data_domain:
            q &= Q(data_domain_id=data_domain.id)
        else:
            q &= Q(data_domain_id=None)
    if topicDomain:
        topic_domain = await TopicDomain.get_or_none(topic_domain_name=topicDomain)
        if topic_domain:
            q &= Q(topic_domain_id=topic_domain.id)
        else:
            q &= Q(topic_domain_id=None)
    if createBy:
        user = await User.get_or_none(user_name=createBy)
        if user:
            q &= Q(create_by_id=user.id)
        else:
            q &= Q(create_by_id=None)

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

        # 获取关联数据
        create_by = await data_model_obj.create_by
        data_domain = await data_model_obj.data_domain
        topic_domain = await data_model_obj.topic_domain

        # 添加关联字段
        data_model_dict.update(
            {
                "createBy": create_by.user_name,
                "dataDomain": data_domain.data_domain_name,
                "topicDomain": topic_domain.topic_domain_name,
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


@router.post("/data-model", summary="创建主题模型信息")
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


@router.patch("/data-model/{id}", summary="更新主题模型信息")
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


@router.delete("/data-model/{id}", summary="删除主题模型信息")
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


@router.get("/data-model/data-preview", summary="预览数据")
async def _(
    databaseId: str = Query(None, description="数据库ID"),
    tableName: str = Query(None, description="表名"),
):

    total, response = await data_model_controller.fetch_table_data(
        databaseId, tableName
    )
    _, columns = await data_model_controller.fetch_columns_metadata(
        databaseId, tableName
    )
    return Success(
        msg="预览成功",
        total=total,
        columns=columns,
        data={"records": jsonable_encoder(response)},
    )


@router.get("/data-model/tables", summary="获取表的元数据")
async def _(databaseId: str = Query(None, description="数据库ID")):
    total, data = await data_model_controller.fetch_tables_metadata(databaseId)
    return Success(msg="获取元数据成功", total=total, data={"records": data})


@router.get("/data-model/columns-metadata", summary="获取表的字段元数据")
async def _(
    database_id: str = Query(None, description="数据库ID"),
    table_name: str = Query(None, description="表名"),
):
    total, data = await data_model_controller.fetch_columns_metadata(
        database_id, table_name
    )

    return Success(msg="获取元数据成功", total=total, data={"records": data})


@router.get("/data-model/aggregate-data", summary="获取表的聚合数据")
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
