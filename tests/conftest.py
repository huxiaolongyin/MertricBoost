"""
这是一个公共的测试模块，测试步骤
1. 连接现有的 mysql 数据库
2. 新建一个 **_test 的数据库
3. 根据配置文件，自动生成库表
4. 从 test/data 中，从csv中获取数据，插入测试数据
5. 进行测试
"""

import shutil
from pathlib import Path
from typing import Any, Dict

import aiomysql
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from metricboost.config import SETTINGS
from metricboost.logger import logger


def get_test_config() -> Dict[str, Any]:
    test_config = SETTINGS.TORTOISE_ORM.copy()

    test_config["connections"]["conn_system"]["credentials"][
        "database"
    ] = "metric_boost_test"
    return test_config


# TODO: 后面进行精简化
async def create_test_database():
    """创建测试数据库"""
    # 创建测试数据库
    logger.debug("创建测试数据库")
    conn = await aiomysql.connect(
        host=SETTINGS.MYSQL_DB_HOST,
        port=SETTINGS.MYSQL_DB_PORT,
        user=SETTINGS.MYSQL_DB_USER,
        password=SETTINGS.MYSQL_DB_PASSWORD,
        db=None,
        autocommit=True,
    )

    async with conn.cursor() as cursor:
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS `metric_boost_test`")


def delete_migrations_folder():
    # 删除 migrations 文件夹
    logger.debug("删除 migrations 文件夹...")
    migrations_dir = Path(__file__).parent.parent / "migrations"
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)


async def del_test_database():
    logger.debug("删除测试数据库...")
    conn = await aiomysql.connect(
        host=SETTINGS.MYSQL_DB_HOST,
        port=SETTINGS.MYSQL_DB_PORT,
        user=SETTINGS.MYSQL_DB_USER,
        password=SETTINGS.MYSQL_DB_PASSWORD,
        db=None,
        autocommit=True,
    )
    async with conn.cursor() as cursor:
        await cursor.execute(f"DROP DATABASE IF EXISTS `metric_boost_test`")


@pytest_asyncio.fixture(scope="session")
async def app_with_lifespan():
    """创建带有生命周期的应用实例"""
    from metricboost.app import create_app

    delete_migrations_folder()

    # 创建测试数据库
    await create_test_database()

    # 获取测试配置
    test_config = get_test_config()

    # 使用应用的生命周期上下文
    app = create_app(test_config)

    yield app

    # 清理测试数据库
    print("")

    await del_test_database()

    delete_migrations_folder()


@pytest.fixture(scope="session")
def client(app_with_lifespan):
    """创建测试客户端"""
    with TestClient(app_with_lifespan) as client:
        yield client
