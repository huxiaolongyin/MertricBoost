import pytest
from fastapi.testclient import TestClient
from app import create_app
from tortoise.contrib.test import initializer, finalizer
from app.models.system import User
from app.models.service import ServiceApp

# 创建应用实例,
app = create_app()


# 在模块级别初始化和终止数据库连接（似乎没什么用）
# @pytest.fixture(scope="module", autouse=True)
# async def initialize_db():
#     """
#     初始化数据库连接，在测试模块开始时执行。
#     """
#     initializer(
#         modules=[
#             "app.models.system",
#             "aerich.models",
#             "app.models.metric",
#             "app.models.asset",
#             "app.models.service",
#         ],  # 替换为您的实际模型模块路径
#         db_url="sqlite://:memory:",  # 设置测试数据库（使用内存数据库，避免影响生产数据）
#         app_label="app_system",
#     )

#     # 创建测试用户
#     test_user = await User.create(user_name="test", password="123456", status="1")

#     # 创建测试应用
#     test_app = await ServiceApp.create(
#         app_name="测试应用",
#         app_desc="这是一个测试应用",
#         status="1",
#         app_key="test_app_key",
#         app_secret="test_app_secret",
#         create_by=test_user,
#     )

#     yield
#     finalizer()


# 创建测试客户端, 避免fastapi生命周期启动时,没有正确执行startup函数, 从而初始化ORM
@pytest.fixture(scope="module")
def client():
    """创建测试客户端"""
    with TestClient(app) as c:
        yield c
