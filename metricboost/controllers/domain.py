from tortoise.expressions import Q
from tortoise.functions import Count

from metricboost.core.crud import CRUDBase
from metricboost.models.asset import Domain
from metricboost.schemas.domain import DomainCreate, DomainResponse, DomainUpdate


class DomainController(CRUDBase[Domain, DomainCreate, DomainUpdate]):
    def __init__(self):
        super().__init__(model=Domain)

    async def create(self, obj_in: DomainCreate) -> Domain:
        """创建域信息"""

        # 检查是否已存在同名域
        existing = await self.model.filter(
            domain_name=obj_in.domain_name, domain_type=obj_in.domain_type
        ).first()

        if existing:
            raise ValueError(f"已存在同名同类型的域: {obj_in.domain_name}")

        # 创建域
        return await super().create(obj_in)

    async def update(self, id: int, obj_in: DomainUpdate) -> Domain:
        """更新域信息"""

        # 检查域是否存在
        domain = await self.get(id=id)
        if not domain:
            raise ValueError("域不存在")

        # 如果更新了名称，检查是否会导致重名
        if obj_in.domain_name and obj_in.domain_name != domain.domain_name:
            existing = (
                await self.model.filter(
                    domain_name=obj_in.domain_name,
                    domain_type=obj_in.domain_type or domain.domain_type,
                )
                .exclude(id=id)
                .first()
            )

            if existing:
                raise ValueError(f"已存在同名同类型的域: {obj_in.domain_name}")

        # 更新域
        return await super().update(id=id, obj_in=obj_in)

    async def remove(self, id):
        """删除域"""

        # 检查域是否存在
        domain = await self.get(id=id)

        if not domain:
            raise ValueError("域不存在")

        # 删除域
        return await super().remove(id)

    async def get_domains_by_type(
        self, domain_type: int, page: int = 1, page_size: int = 100
    ):
        """按类型获取域列表"""
        total, domains = await self.get_list(
            page=page, page_size=page_size, search=Q(domain_type=domain_type)
        )

        return total, domains

    async def get_domains_with_metrics_count(
        self, domain_type: int = None, page: int = 1, page_size: int = 10
    ):
        """获取域列表及其关联的指标数量"""
        query = self.model.all().annotate(metrics_count=Count("metrics"))

        if domain_type is not None:
            query = query.filter(domain_type=domain_type)

        # 查询总数
        total = await query.count()

        # 分页查询
        results = (
            await query.offset((page - 1) * page_size)
            .limit(page_size)
            .values("id", "domain_name", "domain_desc", "domain_type", "metrics_count")
        )

        return total, results


domain_controller = DomainController()
