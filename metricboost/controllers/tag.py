from typing import List, Tuple

from tortoise.expressions import Q
from tortoise.functions import Count

from metricboost.core.crud import CRUDBase
from metricboost.models.asset import Tag
from metricboost.models.metric import Metric
from metricboost.schemas.tag import MetricTagLink, TagCreate, TagUpdate


class TagController(CRUDBase[Tag, TagCreate, TagUpdate]):
    def __init__(self):
        super().__init__(model=Tag)

    async def create(self, obj_in: TagCreate) -> Tag:
        """创建标签"""
        # 检查是否已存在同名标签
        existing = await self.model.filter(tag_name=obj_in.tag_name).first()
        if existing:
            raise ValueError(f"已存在同名标签: {obj_in.tag_name}")

        # 创建标签
        tag = await super().create(obj_in)
        return tag

    async def update(self, id: int, obj_in: TagUpdate) -> Tag:
        """更新标签"""
        tag = await self.get(id=id)
        if not tag:
            raise ValueError("标签不存在")

        # 如果更新了名称，检查是否会导致重名
        if obj_in.tag_name and obj_in.tag_name != tag.tag_name:
            existing = (
                await self.model.filter(tag_name=obj_in.tag_name).exclude(id=id).first()
            )
            if existing:
                raise ValueError(f"已存在同名标签: {obj_in.tag_name}")

        # 更新标签
        updated_tag = await super().update(id=id, obj_in=obj_in)
        return updated_tag

    async def remove(self, id: int | List[int]):
        """删除标签"""
        # 检查标签是否存在
        obj = await self.get(id=id)
        if not obj:
            raise ValueError(f"标签{id}不存在")

        # 检查是否存在标签指标关联
        metric_tag_objs = await Tag.get(id=id).prefetch_related("metrics")
        if await metric_tag_objs.metrics.all():
            raise ValueError("存在标签指标关联，不允许删除")
        return await super().remove(id)

    async def get_tags_by_type(
        self,
        tag_type: str = None,
        page: int = 1,
        page_size: int = 100,
    ):
        """按类型获取标签列表"""
        search = Q() if tag_type is None else Q(tag_type=tag_type)

        total, tags = await self.get_list(page=page, page_size=page_size, search=search)

        return total, tags

    async def get_tags_with_metrics_count(
        self,
        tag_type: str = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[int, List[Tag]]:
        """获取标签列表及其关联的指标数量"""
        query = self.model.all().annotate(metrics_count=Count("metrics"))

        if tag_type is not None:
            query = query.filter(tag_type=tag_type)

        # 查询总数
        total = await query.count()

        # 分页查询
        results = (
            await query.offset((page - 1) * page_size)
            .limit(page_size)
            .values("id", "tag_name", "tag_type", "tag_desc", "metrics_count")
        )

        return total, results

    async def link_tag_to_metric(self, link: MetricTagLink) -> bool:
        """将标签关联到指标"""
        # 检查指标和标签是否存在
        metric = await Metric.get_or_none(id=link.metric_id)
        if not metric:
            raise ValueError(f"指标ID: {link.metric_id} 不存在")

        tag = await self.get(id=link.tag_id)
        if not tag:
            raise ValueError(f"标签ID: {link.tag_id} 不存在")

        # 建立关联
        await metric.tags.add(tag)
        return True

    async def unlink_tag_from_metric(self, link: MetricTagLink) -> bool:
        """取消标签与指标的关联"""
        # 检查指标和标签是否存在
        metric = await Metric.get_or_none(id=link.metric_id)
        if not metric:
            raise ValueError(f"指标ID: {link.metric_id} 不存在")

        tag = await self.get(id=link.tag_id)
        if not tag:
            raise ValueError(f"标签ID: {link.tag_id} 不存在")

        # 移除关联
        await metric.tags.remove(tag)
        return True

    async def get_metric_tags(self, metric_id: int) -> List[Tag]:
        """获取指标关联的标签列表"""
        metric = await Metric.get_or_none(id=metric_id)
        if not metric:
            return []

        return await metric.tags.all()


tag_controller = TagController()
