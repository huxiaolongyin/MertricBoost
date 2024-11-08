from fastapi import APIRouter
from app.schemas.base import Success
from tortoise.expressions import Q
from app.controllers import metric_controller
from app.schemas.metric import MetricCreate
from app.models.system import DataModel

router = APIRouter()


@router.get("/", summary="获取指标")
async def _(
    # id: int = None,
    # chineseName: str = None,
    # publishStatus: str = None,
    # favoriteStatus: str = None,
    # sensitivity: str = None,
    # createBy: str = None,
):
    q = Q()
    # if chineseName:
    #     q &= Q(chinese_name__icontains=chineseName)
    # if publishStatus:
    #     q &= Q(publish_status=publishStatus)
    # if favoriteStatus:
    #     q &= Q(favorite_status=favoriteStatus)
    # if sensitivity:
    #     q &= Q(sensitivity=sensitivity)

    # total, metric_objs =
    await metric_controller.list(
        page=1,
        page_size=12,
        search=q,
        order=["id"],
    )
    # 获取模型的数据
    # model = await DataModel.filter(id=metric_objs).first()
    # records = [await metric_obj.to_dict() for metric_obj in metric_objs]
    # return Success(total=total, data={"records": records})
    return Success("获取成功")


@router.post("/", summary="创建指标")
async def _(
    metric_in: MetricCreate,
):
    new_metric = await metric_controller.create(obj_in=metric_in)
    return Success(msg="创建成功", data={"create_id": new_metric.id})


@router.patch("/", summary="更新指标")
async def _(
    id: int,
    metric_in: MetricCreate,
):
    await metric_controller.update(id=id, obj_in=metric_in)
    return Success(msg="更新成功", data={"update_id": id})
