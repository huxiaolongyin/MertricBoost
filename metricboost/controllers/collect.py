from tortoise.functions import Count

from metricboost.core.crud import CRUDBase
from metricboost.models.collect.collect import Collect
from metricboost.models.enums import CollectType, StatusType
from metricboost.schemas.collect import CollectCreate, CollectUpdate


class CollectController(CRUDBase[Collect, CollectCreate, CollectUpdate]):
    def __init__(self):
        super().__init__(model=Collect)

    async def create(self, obj_in: CollectCreate, exclude=None):
        """创建数据采集任务"""
        # 检查是否已存在相同名称的采集任务
        existing = await self.model.filter(name=obj_in.name).first()
        if existing:
            raise ValueError("采集任务名称已存在")

        # 创建采集任务
        return await super().create(obj_in, exclude)

    async def update(self, id: int, obj_in: CollectUpdate) -> Collect:
        """更新数据采集任务"""
        # 检查采集任务是否存在
        task = await self.get(id=id)
        if not task:
            raise ValueError("采集任务不存在")

        # 更新采集任务
        return await super().update(id=id, obj_in=obj_in)

    async def remove(self, id: int):
        """删除数据采集任务"""
        # 检查采集任务是否存在
        task = await self.get(id=id)
        if not task:
            raise ValueError("采集任务不存在")

        # 删除采集任务
        return await super().remove(id)

    async def toggle_status(self, id: int, status: StatusType) -> Collect:
        """切换采集任务状态（启用/禁用）"""
        task = await self.get(id=id)
        if not task:
            raise ValueError("采集任务不存在")

        task.status = status
        await task.save()
        return task

    async def get_collect_tasks(
        self, page: int = 1, page_size: int = 10, task_type: CollectType = None
    ):
        """获取数据采集任务列表"""
        query = self.model.all()

        # 按类型筛选
        if task_type:
            query = query.filter(type=task_type)

        # 查询总数
        total = await query.count()

        # 分页查询
        results = (
            await query.offset((page - 1) * page_size)
            .limit(page_size)
            .prefetch_related(
                "origin_database", "target_database", "create_by", "update_by"
            )
        )

        return total, results

    async def execute_offline_sync(self, id: int):
        """执行离线同步任务（MySQL/达梦 -> Hive）"""
        task = await self.get(id=id)
        if not task:
            raise ValueError("采集任务不存在")

        if task.type != CollectType.BATCH:
            raise ValueError("只能执行离线同步任务")

        # TODO: 实现实际的离线同步逻辑
        # 1. 从源数据库读取数据
        # 2. 转换数据格式
        # 3. 写入Hive

        return {"status": "success", "message": "离线同步任务已提交"}

    async def configure_realtime_sync(self, id: int, flume_config: dict):
        """配置实时同步任务（日志文件 -> Flume -> HDFS）"""
        task = await self.get(id=id)
        if not task:
            raise ValueError("采集任务不存在")

        if task.type != CollectType.STREAM:
            raise ValueError("只能配置实时同步任务")

        # TODO: 实现实际的Flume配置逻辑
        # 1. 生成Flume配置文件
        # 2. 部署Flume配置
        # 3. 启动Flume agent

        return {"status": "success", "message": "实时同步任务已配置"}


collect_controller = CollectController()
