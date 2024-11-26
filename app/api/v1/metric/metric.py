from fastapi import APIRouter, Request
from app.schemas.base import Success
from tortoise.expressions import Q
from app.controllers import metric_controller
from app.schemas.metric import MetricCreate, MetricSearch
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pyinstrument import Profiler

router = APIRouter()


@router.post("/detail/", summary="获取指标")
async def _(
    metric_search: MetricSearch,
):
    profiler = Profiler()
    profiler.start()

    # 获取 date_range、conditions 参数
    if metric_search.dateRange:
        date_range = [
            datetime.fromtimestamp(int(item) / 1000) for item in metric_search.dateRange
        ]
    else:
        date_range = None
    conditions = metric_search.conditions
    comparisonOperators = metric_search.comparisonOperators
    dimensionFilter = metric_search.dimensionFilter
    chineseName = metric_search.chineseName
    favoriteStatus = metric_search.favoriteStatus
    sensitivity = metric_search.sensitivity
    publishStatus = metric_search.publishStatus
    topicDomain = metric_search.topicDomain
    dimensionDrillDown = metric_search.dimensionDrillDown
    createBy = metric_search.createBy

    # 拼接筛选语句
    if dimensionFilter and comparisonOperators and conditions:
        condition_sql_string = (
            "and "
            + dimensionFilter
            + " "
            + comparisonOperators
            + " ("
            + ", ".join(f"'{x}'" for x in conditions)
            + ")"
        )
    else:
        condition_sql_string = ""

    q = Q()
    if chineseName:
        q &= Q(chinese_name__icontains=chineseName)
    if publishStatus:
        q &= Q(publish_status=publishStatus)
    if favoriteStatus:
        q &= Q(favorite_status=favoriteStatus)
    if sensitivity:
        q &= Q(sensitivity=sensitivity)
    if topicDomain:
        q &= Q(data_model__topic_domain_id=topicDomain)
    if createBy:
        q &= Q(create_by__user_name=createBy)

    total, metric_objs = await metric_controller.list(
        page=1,
        page_size=10,
        search=q,
        search_dimensions=dimensionDrillDown,
        condition_sql_string=condition_sql_string,
        date_range=date_range,
        order=["id"],
    )

    # 获取模型的数据
    records = []
    for metric_obj in metric_objs:
        # 构建基础数据字典
        metric_dict = await metric_obj.to_dict()

        # 获取用户关联数据
        create_by = await metric_obj.create_by

        # 添加关联字段
        metric_dict.update(
            {
                "createBy": create_by.user_name,
                "dataModel": metric_obj.data_model_id,
            }
        )
        metric_dict.pop("createById", "dataModelId")
        records.append(metric_dict)

    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))

    return Success(total=total, data={"records": jsonable_encoder(records)})


@router.post("/detail/{id}", summary="获取指标")
async def _(
    metric_search: MetricSearch,
    id: int | None = None,
):
    # 获取 date_range、conditions 参数
    if metric_search.dateRange:
        date_range = [
            datetime.fromtimestamp(int(item) / 1000) for item in metric_search.dateRange
        ]
    else:
        date_range = None
    conditions = (
        metric_search.conditions
        if isinstance(metric_search.conditions, list)
        else [metric_search.conditions]
    )

    (
        comparisonOperators,
        dimensionFilter,
        dimensionDrillDown,
        statistical_period,
        sort,
    ) = (
        metric_search.comparisonOperators,
        metric_search.dimensionFilter,
        metric_search.dimensionDrillDown,
        metric_search.statisticalPeriod,
        metric_search.sort,
    )

    # 拼接筛选语句
    if dimensionFilter and comparisonOperators and conditions:
        condition_sql_string = (
            "and "
            + dimensionFilter
            + " "
            + comparisonOperators
            + " ("
            + ", ".join(f"'{x}'" for x in conditions)
            + ")"
        )
    else:
        condition_sql_string = ""

    q = Q()
    if id:
        q &= Q(id=id)

    total, metric_objs = await metric_controller.list(
        page=1,
        page_size=10,
        search=q,
        search_dimensions=dimensionDrillDown,
        condition_sql_string=condition_sql_string,
        date_range=date_range,
        statistical_period=statistical_period,
        sort=sort,
        order=["id"],
    )

    # 获取模型的数据
    records = []
    for metric_obj in metric_objs:
        # 构建基础数据字典
        metric_dict = await metric_obj.to_dict()
        # 获取用户关联数据
        create_by = await metric_obj.create_by
        # 添加关联字段
        metric_dict.update(
            {
                "createBy": create_by.user_name,
                "dataModel": metric_obj.data_model_id,
            }
        )
        metric_dict.pop("createById", "dataModelId")
        records.append(metric_dict)

    return Success(total=total, data={"records": jsonable_encoder(records)})


@router.post("/", summary="创建指标")
async def _(
    metric_in: MetricCreate,
):
    new_metric = await metric_controller.create(obj_in=metric_in)
    return Success(msg="创建成功", data={"create_id": new_metric.id})


@router.patch("/{id}", summary="更新指标")
async def _(
    id: int,
    metric_in: MetricCreate,
):
    await metric_controller.update(id=id, obj_in=metric_in)
    return Success(msg="更新成功", data={"update_id": id})
