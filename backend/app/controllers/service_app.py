from pydantic import BaseModel
from app.core.crud import CRUDBase
from app.models.system import User
from typing import NewType, TypeVar
from tortoise.expressions import Q
from tortoise.models import Model
from app.models.service import ServiceApp
from app.schemas.service_app import ServiceAppCreate, ServiceAppUpdate

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ServiceAppController(CRUDBase[ServiceApp, ServiceAppCreate, ServiceAppUpdate]):
    def __init__(self):
        super().__init__(model=ServiceApp)

    async def get_app_list(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Q = Q(),
    ):
        """
        获取应用列表
        """
        query = self.model.filter(search)

        # 获取总数
        total = await query.count()

        # 分页查询，预加载关联数据
        result = (
            await query.prefetch_related("create_by")
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return Total(total), result

    async def create(self, obj_in: ServiceAppCreate, exclude=None) -> ServiceApp:
        """
        创建应用
        """
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().create(obj_in, exclude)

    async def get_app_by_name(self, app_name: str) -> ServiceApp:
        """
        根据应用名称获取应用
        """
        return await self.model.get_or_none(app_name=app_name)

    async def update(self, id, obj_in: ServiceAppUpdate, exclude=None):
        """
        更新应用
        """
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().update(id, obj_in, exclude)

    async def remove(self, id):
        """
        删除应用
        """
        return await super().remove(id)


service_app_controller = ServiceAppController()
