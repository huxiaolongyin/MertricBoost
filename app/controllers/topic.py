from app.core.crud import CRUDBase
from app.models.system import User, TopicDomain, DataDomain
from app.schemas.topic import (
    TopicDomainCreate,
    TopicDomainUpdate,
    DataDomainCreate,
    DataDomainUpdate,
)


class TopicDomainController(
    CRUDBase[TopicDomain, TopicDomainCreate, TopicDomainUpdate]
):
    def __init__(self):
        super().__init__(model=TopicDomain)

    async def get_by_status(self, status: str) -> TopicDomain | None:
        return await self.model.filter(status=status).first()

    async def get_by_creator(self, creator: str) -> TopicDomain | None:
        return await self.model.filter(creator=creator).first()

    async def create(self, obj_in: TopicDomainCreate) -> TopicDomain:  # type: ignore
        # 获取关联对象
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj = await super().create(obj_in)
        return obj

    async def update(self, id: int, obj_in: TopicDomainUpdate) -> TopicDomain:  # type: ignore
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().update(id=id, obj_in=obj_in)

    async def remove(self, id: int) -> TopicDomain:
        return await super().remove(id=id)


topic_domain_controller = TopicDomainController()


class DataDomainController(CRUDBase[DataDomain, DataDomainCreate, DataDomainUpdate]):
    def __init__(self):
        super().__init__(model=DataDomain)

    async def get_by_status(self, status: str) -> DataDomain | None:
        return await self.model.filter(status=status).first()

    async def get_by_creator(self, creator: str) -> DataDomain | None:
        return await self.model.filter(creator=creator).first()

    async def create(self, obj_in: DataDomainCreate) -> DataDomain:  # type: ignore
        # 获取关联对象
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj = await super().create(obj_in)
        return obj

    async def update(self, id: int, obj_in: DataDomainUpdate) -> DataDomain:  # type: ignore
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().update(id=id, obj_in=obj_in)

    async def remove(self, id: int) -> DataDomain:
        return await super().remove(id=id)


data_domain_controller = DataDomainController()
