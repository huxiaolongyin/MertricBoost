import time
from datetime import datetime, timedelta

import pytest

from metricboost.core.ctx import CTX_USER_ID
from metricboost.models.system import LogType


@pytest.mark.asyncio
async def test_get_logs_list(client):
    """测试获取日志列表接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 测试基本日志查询
    response = client.get("/api/v1/system/logs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "total" in data["data"]
    assert "records" in data["data"]
    assert isinstance(data["data"]["records"], list)

    # 测试带参数的日志查询 - API日志类型
    response = client.get("/api/v1/system/logs?logType=1&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 测试URL过滤条件
    response = client.get("/api/v1/system/logs?requestUrl=/api&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 测试日志详情过滤
    response = client.get("/api/v1/system/logs?logDetail=test&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 测试时间范围过滤
    now = int(time.time() * 1000)
    week_ago = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
    time_range = f"{week_ago},{now}"
    response = client.get(
        f"/api/v1/system/logs?timeRange={time_range}&page=1&page_size=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"


@pytest.mark.asyncio
async def test_logs_permission(client):
    """测试日志访问权限控制"""
    # 测试超级管理员权限
    CTX_USER_ID.set(2)  # 假设ID为1是超级管理员

    # 设置管理员权限
    # user_data = {
    #     "userName": "admin",
    #     "userEmail": "updated@example.com",
    #     "status": "1",
    #     "roles": ["R_SUPER"],
    # }
    # update_response = client.patch("/api/v1/system/users/1", json=user_data)
    # assert update_response.status_code == 200

    # 超级管理员应该可以查看各种类型的日志
    response = client.get(
        f"/api/v1/system/logs?logType={LogType.SystemLog}&page=1&page_size=10"
    )
    assert response.status_code == 200
    assert response.json()["code"] == "0000"

    # 测试普通用户权限
    CTX_USER_ID.set(1)  # 假设ID为1是普通用户

    # 普通用户尝试访问非API日志应该被拒绝
    response = client.get(
        f"/api/v1/system/logs?logType={LogType.SystemLog}&page=1&page_size=10"
    )
    data = response.json()
    assert data["code"] == "4000" or "Permission Denied" in data["msg"]

    # 普通用户可以查看API日志
    response = client.get(
        f"/api/v1/system/logs?logType={LogType.ApiLog}&page=1&page_size=10"
    )
    assert response.status_code == 200
    assert response.json()["code"] == "0000"


@pytest.mark.asyncio
async def test_get_log_detail(client):
    """测试获取日志详情接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先获取一个日志ID
    list_response = client.get("/api/v1/system/logs?page=1&page_size=1")
    list_data = list_response.json()

    if list_data["data"]["total"] > 0:
        log_id = list_data["data"]["records"][0]["id"]

        # 获取日志详情
        detail_response = client.get(f"/api/v1/system/logs/{log_id}")
        assert detail_response.status_code == 200
        detail_data = detail_response.json()
        assert detail_data["code"] == "0000"

        # 验证返回的字段
        assert "log_type" in detail_data["data"] or "logType" in detail_data["data"]


@pytest.mark.asyncio
async def test_update_log(client):
    """测试更新日志接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先获取一个日志ID
    list_response = client.get("/api/v1/system/logs?page=1&page_size=1")
    list_data = list_response.json()

    if list_data["data"]["total"] > 0:
        log_id = list_data["data"]["records"][0]["id"]

        # 更新日志
        update_data = {"logDetail": "Updated for testing"}

        response = client.patch(f"/api/v1/system/logs/{log_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0000"
        assert data["msg"] == "Update Successfully"

        # 验证更新结果
        check_response = client.get(f"/api/v1/system/logs/{log_id}")
        assert check_response.status_code == 200
        check_data = check_response.json()
        assert check_data["code"] == "0000"


@pytest.mark.asyncio
async def test_delete_log(client):
    """测试删除单个日志接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先获取一个日志ID
    list_response = client.get("/api/v1/system/logs?page=1&page_size=1")
    list_data = list_response.json()

    if list_data["data"]["total"] > 0:
        log_id = list_data["data"]["records"][0]["id"]

        # 删除该日志
        delete_response = client.delete(f"/api/v1/system/logs/{log_id}")
        assert delete_response.status_code == 200
        delete_data = delete_response.json()
        assert delete_data["code"] == "0000"
        assert delete_data["msg"] == "Deleted Successfully"
        assert delete_data["data"]["deleted_id"] == log_id

        # 验证删除结果
        check_response = client.get(f"/api/v1/system/logs/{log_id}")
        # 应返回错误或空数据，因为日志已被删除
        assert (
            check_response.status_code != 200 or check_response.json()["code"] != "0000"
        )


@pytest.mark.asyncio
async def test_batch_delete_logs(client):
    """测试批量删除日志接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 获取多个日志ID
    list_response = client.get("/api/v1/system/logs?page=1&page_size=3")
    list_data = list_response.json()

    if list_data["data"]["total"] >= 2:
        # 获取前两条日志的ID
        log_ids = [str(record["id"]) for record in list_data["data"]["records"][:2]]

        # 批量删除
        batch_delete_response = client.delete(
            f"/api/v1/system/logs?ids={','.join(log_ids)}"
        )
        assert batch_delete_response.status_code == 200
        batch_delete_data = batch_delete_response.json()
        assert batch_delete_data["code"] == "0000"
        assert batch_delete_data["msg"] == "Deleted Successfully"
        assert "deleted_ids" in batch_delete_data["data"]

        # 验证删除结果
        for log_id in log_ids:
            check_response = client.get(f"/api/v1/system/logs/{log_id}")
            # 应返回错误或空数据，因为日志已被删除
            assert (
                check_response.status_code != 200
                or check_response.json()["code"] != "0000"
            )
