from app.core.crud import CRUDBase
from app.models.tag import Tag, MetricTag
from app.schemas.tag import TagCreate, TagUpdate, MetricTagCreate, MetricTagUpdate
from app.models.system import User


class TagController(CRUDBase[Tag, TagCreate, TagUpdate]):
    def __init__(self):
        super().__init__(model=Tag)

    async def create(self, obj_in: TagCreate) -> Tag:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj = await super().create(obj_in)
        return obj

    async def update(self, tag_id: int, obj_in: TagUpdate) -> Tag:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().update(id=tag_id, obj_in=obj_in)

    async def remove(self, tag_id: int) -> Tag:
        return await super().remove(id=tag_id)


class MetricTagController(CRUDBase[MetricTag, MetricTagCreate, MetricTagUpdate]):
    def __init__(self):
        super().__init__(model=MetricTag)

    async def list(self, metric_ids: list) -> list[MetricTag]:
        query = self.model.filter(metric_id__in=metric_ids).select_related(
            "tag", "create_by"
        )

        result = await query.values(
            "metric_id", tag="tag__tag_name", create_by="create_by__user_name"
        )

        formatted_result = {}
        for item in result:
            metric_id = item["metric_id"]
            if metric_id not in formatted_result:
                formatted_result[metric_id] = {
                    "metric_id": metric_id,
                    "tags": [],
                    "create_by": item["create_by"],
                }
            formatted_result[metric_id]["tags"].append(item["tag"])

        total = len(result)

        list_result = list(formatted_result.values())
        return total, list_result

    async def create(self, obj_in: MetricTagCreate) -> MetricTag:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj = await super().create(obj_in)
        return obj

    async def update(self, metric_tag_id: int, obj_in: MetricTagUpdate) -> MetricTag:
        return await super().update(id=metric_tag_id, obj_in=obj_in)

    async def remove(self, metric_id: int, tag: str) -> MetricTag:
        metric_tag_id = await self.model.filter(
            metric_id=metric_id, tag__tag_name=tag
        ).values_list("id", flat=True)
        if metric_tag_id:
            return await super().remove(id=metric_tag_id[0])
        else:
            return None
        # return await super().remove(id=metric_tag_id)


tag_controller = TagController()
metric_tag_controller = MetricTagController()
