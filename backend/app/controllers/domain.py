from app.core.crud import CRUDBase
from app.models.asset import TopicDomain, DataDomain
from app.models.system import User
from app.schemas.domain import DomainCreate, DomainUpdate


class TopicDomainController(CRUDBase[TopicDomain, DomainCreate, DomainUpdate]):

    def __init__(self):
        super().__init__(model=TopicDomain)

    async def create(self, obj_in: DomainCreate) -> TopicDomain:  # type: ignore
        # 获取关联对象
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj = await super().create(obj_in)
        return obj

    async def update(self, id: int, obj_in: DomainUpdate) -> TopicDomain:  # type: ignore
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().update(id=id, obj_in=obj_in)


topic_domain_controller = TopicDomainController()


class DataDomainController(CRUDBase[DataDomain, DomainCreate, DomainUpdate]):
    def __init__(self):
        super().__init__(model=DataDomain)

    async def create(self, obj_in: DomainCreate) -> DataDomain:  # type: ignore
        # 获取关联对象
        obj_dict = obj_in.model_dump(exclude={"create_by"})
        obj_dict["create_by"] = await User.get(user_name=obj_in.create_by)
        return await super().create(obj_in)

    async def update(self, id: int, obj_in: DomainUpdate) -> DataDomain:  # type: ignore
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().update(id=id, obj_in=obj_in)


data_domain_controller = DataDomainController()
