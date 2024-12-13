from fastapi.testclient import TestClient
from app import create_app
import pytest

# 创建应用实例,
app = create_app()


# 创建测试客户端, 避免fastapi生命周期启动时,没有正确执行startup函数, 从而初始化ORM
@pytest.fixture(scope="module")
def client():
    app = create_app()
    with TestClient(app) as c:
        yield c


# 1. 测试应用列表获取
def test_get_api_list(client):
    # 测试未提供用户名的情况
    response = client.get("/api/v1/service/api")
    assert response.status_code == 200
    assert response.json()["msg"] == "获取成功"


# 2. 测试应用创建\更新\删除
def test_get_api_list_with_user(client):
    api_data = {
        "apiName": "新建一个测试API",
        "apiPath": "/test",
        "apiDesc": "这是一个测试API",
        "apiMethod": "get",
        "status": "1",
        "createBy": "admin",
        "appId": 1,
        "metricId": 14,
        "params": [],
    }
    response = client.post("/api/v1/service/api", json=api_data)
    assert response.status_code == 200
    create_result = response.json()
    assert create_result["msg"] == "创建成功"
    assert "create_id" in create_result["data"]
    api_id = create_result["data"]["create_id"]

    # 名称重复
    response = client.post("/api/v1/service/api", json=api_data)
    assert response.status_code == 400
    assert response.json()["msg"] == "API名称已存在"

    # 路径重复
    api_path_data = {
        "apiName": "另一个测试API",
        "apiPath": "/test",
        "apiDesc": "这是一个测试API",
        "apiMethod": "get",
        "status": "1",
        "createBy": "admin",
        "appId": 1,
        "metricId": 14,
        "params": [],
    }
    response = client.post("/api/v1/service/api", json=api_path_data)
    assert response.status_code == 400
    assert response.json()["msg"] == "API路径已存在"

    # 更新API
    update_data = {
        "apiName": "更新后的测试API",
        "apiPath": "/test",
        "apiDesc": "这是一个测试API",
        "apiMethod": "get",
        "status": "1",
        "createBy": "admin",
        "appId": 1,
        "metricId": 14,
        "params": [],
    }
    response = client.patch(
        "/api/v1/service/api", params={"id": api_id}, json=update_data
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "更新成功"

    # 删除API
    response = client.delete(f"/api/v1/service/api", params={"id": api_id})
    assert response.status_code == 200
    assert response.json()["msg"] == "删除成功"
