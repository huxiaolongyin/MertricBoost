import asyncmy.errors
from tortoise import Tortoise
from tortoise.functions import Count

from metricboost.core.crud import CRUDBase
from metricboost.models.asset import Database
from metricboost.schemas.database import DatabaseCreate, DatabaseUpdate


class DatabaseController(CRUDBase[Database, DatabaseCreate, DatabaseUpdate]):
    def __init__(self):
        super().__init__(model=Database)

    async def create(self, obj_in: DatabaseCreate, exclude=None):
        """创建数据库配置"""

        # 检查是否已存在相同配置的数据库
        existing = await self.model.filter(name=obj_in.name).first()

        if existing:
            raise ValueError("数据库名称已存在")

        # 创建数据库配置
        return await super().create(obj_in, exclude)

    async def update(self, id: int, obj_in: DatabaseUpdate) -> Database:
        """更新数据库配置"""

        # 检查数据库是否存在
        db = await self.get(id=id)

        if not db:
            raise ValueError("数据库不存在")

        # 更新数据库配置
        if obj_in.password:
            return await super().update(id=id, obj_in=obj_in)
        else:
            return await super().update(id=id, obj_in=obj_in, exclude=["password"])

    async def remove(self, id: int):
        """删除数据库配置"""

        # 检查数据库是否存在
        db = await self.get(id=id)
        if not db:
            raise ValueError("数据库不存在")

        # 删除数据库配置
        return await super().remove(id)

    async def test_connection(self, obj_in: DatabaseCreate) -> tuple[bool, str]:
        """测试数据库连接"""
        if obj_in.type.lower() == "mysql":
            try:
                connection_url = f"mysql://{obj_in.username}:{obj_in.password}@{obj_in.host}:{obj_in.port}/{obj_in.database}"

                # 创建测试连接
                await Tortoise.init(
                    db_url=connection_url,
                    modules={"models": []},
                    timezone="Asia/Shanghai",
                )
                # 测试连接
                conn = Tortoise.get_connection("default")
                await conn.execute_query("SELECT 1")

                # 关闭连接
                await Tortoise.close_connections()
                return True, "连接成功"

            except (asyncmy.errors.OperationalError, Exception) as e:
                # 确保关闭连接
                await Tortoise.close_connections()
                return False, str(e)
        return False, "不支持的数据库类型"

    async def get_databases_with_models_count(self, page: int = 1, page_size: int = 10):
        """获取数据库列表及其包含的模型数量"""
        query = self.model.all().annotate(models_count=Count("data_models"))

        # 查询总数
        total = await query.count()

        # 分页查询
        results = (
            await query.offset((page - 1) * page_size)
            .limit(page_size)
            .values(
                "id",
                "name",
                "type",
                "host",
                "port",
                "status",
                "description",
                "models_count",
            )
        )

        return total, results


database_controller = DatabaseController()
