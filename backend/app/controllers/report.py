from typing import List, TypeVar, NewType, Optional
from pydantic import BaseModel
from tortoise.expressions import Q
from tortoise.models import Model
from tortoise.transactions import atomic

from app.core.crud import CRUDBase
from app.models.report.report import Report
from app.models.system import User
from app.models.metric import Metric  # Make sure to import Metric model
from app.schemas.report import ReportCreate, ReportUpdate

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ReportController(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def __init__(self):
        super().__init__(model=Report)

    # 需要执行数据库事务的方法上添加 @atomic() 装饰器，确保操作的原子性
    # @atomic()
    async def create(self, obj_in: ReportCreate, exclude: set = None) -> Report:
        """
        创建报告
        """
        if exclude is None:
            exclude = set()

        # 获取创建人和指标对象
        create_by = await User.get(user_name=obj_in.create_by)
        metric = await Metric.get(id=obj_in.metric)

        # 创建报告实例
        report = self.model(
            **obj_in.model_dump(exclude={"create_by", "metric"}),
            create_by=create_by,
            metric=metric,
        )

        await report.save()
        return report

    async def get_report_by_name(self, report_name: str) -> Optional[Report]:
        """
        根据报告名称获取报告
        """
        return await self.model.get_or_none(report_name=report_name)

    # @atomic()
    async def update(
        self, id: int, obj_in: ReportUpdate, exclude: set = None
    ) -> Report:
        """
        更新报告
        """
        return await super().update(id, obj_in, exclude)


report_controller = ReportController()
