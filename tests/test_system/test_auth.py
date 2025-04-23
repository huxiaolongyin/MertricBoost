import pytest


@pytest.mark.asyncio
async def test_login_success(client):
    """测试用户登录成功"""
    # 修改字段名：username -> userName，符合CredentialsSchema定义
    login_data = {
        "userName": "admin",  # 使用正确的字段名
        "password": "admin",
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "token" in data["data"]  # access_token 的别名是 token
    assert "refreshToken" in data["data"]  # refresh_token 的别名是 refreshToken
    assert data["data"]["token"] is not None
    assert data["data"]["refreshToken"] is not None


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """测试用户登录失败 - 无效凭据"""
    login_data = {
        "userName": "nonexistent_user",  # 使用正确的字段名
        "password": "wrong_password",
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    # API可能返回200而不是400，错误信息在响应体中
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "4000"  # 应该返回错误码


@pytest.mark.asyncio
async def test_refresh_token(client):
    """测试刷新Token"""
    # 首先登录获取token
    login_data = {
        "userName": "super_admin",  # 使用正确的字段名
        "password": "admin",
    }
    login_response = client.post("/api/v1/auth/login", json=login_data)
    login_data = login_response.json()

    # 提取refresh_token，注意字段名使用refreshToken
    refresh_token = login_data["data"]["refreshToken"]

    # 使用refresh_token获取新token，注意字段名
    refresh_data = {
        "refreshToken": refresh_token,  # 使用正确的字段名
        "token": None,  # access_token的别名是token
    }

    response = client.post("/api/v1/auth/refreshToken", json=refresh_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "token" in data["data"]  # 检查正确的字段名
    assert "refreshToken" in data["data"]
    assert data["data"]["token"] is not None
    assert data["data"]["refreshToken"] is not None


@pytest.mark.asyncio
async def test_refresh_token_invalid(client):
    """测试使用无效的refresh_token"""
    refresh_data = {"refreshToken": "invalid_token", "token": None}  # 使用正确的字段名

    response = client.post("/api/v1/auth/refreshToken", json=refresh_data)
    # API可能始终返回200状态码，错误在响应体中
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "4010"  # 应该返回错误码


@pytest.mark.asyncio
async def test_get_user_info(client):
    """测试获取用户信息"""
    # 首先登录获取token
    login_data = {
        "userName": "admin",  # 使用正确的字段名
        "password": "admin",
    }
    login_response = client.post("/api/v1/auth/login", json=login_data)
    login_data = login_response.json()

    # 提取access_token，注意字段名
    access_token = login_data["data"]["token"]

    # 设置Authorization头
    headers = {"Authorization": f"Bearer {access_token}"}

    # 获取用户信息
    response = client.get("/api/v1/auth/getUserInfo", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    # 验证用户信息字段
    assert "userName" in data["data"]
    assert data["data"]["userName"] == "admin"
    assert "roles" in data["data"]
    assert "buttons" in data["data"]


@pytest.mark.asyncio
async def test_get_user_info_unauthorized(client):
    """测试未授权获取用户信息"""
    # 不提供Authorization头
    response = client.get("/api/v1/auth/getUserInfo")
    # API可能返回401或其他状态码，或者200但响应体中包含错误
    # 根据实际情况调整断言
    data = response.json()
    # 如果API始终返回200，响应体中会有错误码
    if response.status_code == 200:
        assert data["code"] != "0000"
    else:
        # 如果返回非200状态码
        assert response.status_code in [401, 403, 422]


@pytest.mark.asyncio
async def test_custom_error(client):
    """测试自定义错误端点"""
    # 测试标准错误
    response = client.get("/api/v1/auth/error?code=4000&msg=Custom%20error%20message")
    # API可能始终返回200状态码
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "4000"
    assert "Custom error message" in data["msg"]

    # 测试特殊错误码9999
    response = client.get("/api/v1/auth/error?code=9999&msg=Special%20error")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "4030"  # 特殊处理为4030
    assert "accessToken已过期" in data["msg"]
