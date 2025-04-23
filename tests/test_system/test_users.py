import pytest


@pytest.mark.asyncio
async def test_get_users_list(client):
    """测试获取用户列表接口"""

    response = client.get("/api/v1/system/users?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["total"] >= 1
    assert len(data["data"]["records"]) >= 1
    assert data["data"]["records"][0]["userName"] == "admin"


@pytest.mark.asyncio
async def test_get_user_detail(client):
    """测试获取用户详情接口"""
    response = client.get("/api/v1/system/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["id"] == 1
    assert data["data"]["userName"] == "admin"


@pytest.mark.asyncio
async def test_get_nonexistent_user(client):
    """测试获取不存在的用户详情接口"""
    response = client.get("/api/v1/system/users/999")
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "4000"
    assert "不存在" in data["msg"]


@pytest.mark.asyncio
async def test_create_user(client):
    """测试创建用户接口"""
    # 准备测试数据
    user_data = {
        "userName": "new_user",
        "password": "password123",
        "nickName": "New User",
        "userGender": "1",
        "userEmail": "new@example.com",
        "userPhone": "12345678901",
        "status": "1",
        "roles": ["user"],
    }

    # 发送请求
    response = client.post("/api/v1/system/users", json=user_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["created_id"] >= 2


@pytest.mark.asyncio
async def test_create_duplicate_user(client):
    """测试创建重复用户名的用户"""
    # 准备测试数据
    user_data = {
        "userName": "new_user",
        "password": "password123",
        "nickName": "New User",
        "userGender": "1",
        "userEmail": "new@example.com",
        "userPhone": "12345678901",
        "status": "1",
        "roles": ["user"],
    }

    # 发送请求
    response = client.post("/api/v1/system/users", json=user_data)

    # 验证响应
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "4000"  # 应该是错误代码
    assert "已存在" in data["msg"]


@pytest.mark.asyncio
async def test_update_user(client):
    """测试更新用户接口"""
    # 准备测试数据
    user_data = {
        "userName": "Updated User",
        "userEmail": "updated@example.com",
        "status": "1",
    }

    # 发送请求
    response = client.patch("/api/v1/system/users/1", json=user_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["updated_id"] == 1


@pytest.mark.asyncio
async def test_delete_user(client):
    """测试删除用户接口"""
    # 发送请求
    response = client.delete("/api/v1/system/users/1")

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["deleted_id"] == 1
