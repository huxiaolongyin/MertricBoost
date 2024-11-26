from app.core.crud import CRUDBase
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate
from app.models.system import User


class TagController(CRUDBase[Tag, TagCreate, TagUpdate]):
    def __init__(self):
        super().__init__(model=Tag)

    async def create(self, obj_in: TagCreate) -> Tag:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj = await super().create(obj_in)
        return obj

    async def update(self, tag_id: int, obj_in: TagUpdate) -> Tag:
        return await super().update(id=tag_id, obj_in=obj_in)

    async def remove(self, tag_id: int) -> Tag:
        return await super().remove(id=tag_id)


tag_controller = TagController()
