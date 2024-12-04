from app.core.crud import CRUDBase
from app.models.asset import Database
from app.models.system import User
from app.schemas.database import DatabaseCreate, DatabaseUpdate
from tortoise import Tortoise
import asyncmy.errors


class DatabaseController(CRUDBase[Database, DatabaseCreate, DatabaseUpdate]):
    def __init__(self):
        super().__init__(model=Database)

    async def get_by_status(self, status: str) -> Database | None:
        return await self.model.filter(status=status).first()

    async def get_by_creator(self, creator: str) -> Database | None:
        return await self.model.filter(creator=creator).first()

    async def create(self, obj_in: DatabaseCreate) -> Database:  # type: ignore
        # 获取关联对象
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj = await super().create(obj_in)
        return obj

    async def update(self, database_id: int, obj_in: DatabaseUpdate) -> Database:  # type: ignore
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        return await super().update(id=database_id, obj_in=obj_in)

    async def remove(self, database_id: int) -> Database:
        return await super().remove(id=database_id)

    async def test_connection(self, obj_in: DatabaseCreate) -> Database:
        if obj_in.database_type.lower() == "mysql":
            try:
                connection_url = f"mysql://{obj_in.database_user}:{obj_in.password}@{obj_in.database_host}:{obj_in.database_port}/{obj_in.database_database}"

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
                return "连接成功", None

            except (asyncmy.errors.OperationalError, Exception) as e:
                # 确保关闭连接
                await Tortoise.close_connections()
                return "连接失败", str(e)
        return "连接失败", "不支持的数据库类型"


database_controller = DatabaseController()
