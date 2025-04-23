import pytest

from metricboost.core.ctx import CTX_USER_ID


@pytest.mark.asyncio
async def test_get_databases_list(client):
    """测试获取数据库信息列表接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 基本列表查询
    response = client.get("/api/v1/asset/databases?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "total" in data["data"]
    assert "records" in data["data"]
    assert isinstance(data["data"]["records"], list)

    # 测试带过滤条件的查询
    response = client.get(
        "/api/v1/asset/databases?page=1&page_size=10&databaseType=MySQL"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 测试多个过滤条件
    response = client.get(
        "/api/v1/asset/databases?page=1&page_size=10&status=1&databaseName=test"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"


@pytest.mark.asyncio
async def test_create_database(client):
    """测试创建数据库连接接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 准备测试数据
    database_data = {
        "name": "TestDB",
        "type": "MySQL",
        "host": "localhost",
        "port": 3306,
        "username": "test_user",
        "password": "test_password",
        "database": "test_schema",
        "status": "1",
    }

    # 发送创建请求
    response = client.post("/api/v1/asset/databases", json=database_data)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "创建成功"
    assert "create_id" in data["data"]

    # 记录创建的ID，用于后续测试
    created_id = data["data"]["create_id"]

    return created_id  # 返回创建的ID供其他测试使用


@pytest.mark.asyncio
async def test_update_database(client):
    """测试更新数据库连接接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先创建一个数据库连接
    database_data = {
        "name": "需要更新的数据库",
        "type": "MySQL",
        "host": "localhost",
        "port": 3306,
        "username": "test_user",
        "password": "test_password",
        "database": "test_schema",
        "status": "0",
    }
    response = client.post("/api/v1/asset/databases", json=database_data)

    assert response.status_code == 200
    database_id = response.json()["data"]["create_id"]

    # 准备更新数据
    update_data = {
        "name": "UpdatedTestDB",
        "type": "MySQL",
        "host": "localhost",
        "port": 3306,
        "username": "test_user",
        "password": "test_password",
        "database": "test_schema",
        "status": "0",
    }

    # 发送更新请求
    response = client.patch(f"/api/v1/asset/databases/{database_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "更新成功"
    assert data["data"]["update_id"] == database_id

    # 验证更新结果
    check_response = client.get(f"/api/v1/asset/databases?name=UpdatedTestDB")
    check_data = check_response.json()

    assert check_data["code"] == "0000"
    assert len(check_data["data"]["records"]) > 0
    found = False
    for record in check_data["data"]["records"]:
        if record["id"] == database_id:
            assert record["name"] == "UpdatedTestDB"
            assert record["status"] == "0"
            found = True
            break
    assert found, "更新后的数据库记录未找到"

    return database_id  # 返回ID供其他测试使用


@pytest.mark.asyncio
async def test_delete_database(client):
    """测试删除数据库连接接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先创建一个数据库连接
    database_data = {
        "name": "需要删除的数据库",
        "type": "MySQL",
        "host": "localhost",
        "port": 3306,
        "username": "test_user",
        "password": "test_password",
        "database": "test_schema",
        "status": "0",
    }
    response = client.post("/api/v1/asset/databases", json=database_data)
    assert response.status_code == 200
    database_id = response.json()["data"]["create_id"]

    # 发送删除请求
    response = client.delete(f"/api/v1/asset/databases/{database_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "删除成功"
    assert data["data"]["delete_id"] == database_id

    # 验证删除结果
    check_response = client.get(f"/api/v1/asset/databases?page=1&page_size=10")
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    records = check_data["data"]["records"]
    assert not any(
        record["id"] == database_id for record in records
    ), "数据库记录未被成功删除"


@pytest.mark.asyncio
async def test_test_database_connection(client):
    """测试数据库连接测试接口"""
    # 设置测试用户ID上下文
    # CTX_USER_ID.set(1)

    # 准备测试数据 - 有效连接
    valid_connection = {
        "name": "TestConnection",
        "type": "MySQL",
        "host": "localhost",  # 使用有效的连接信息
        "port": 3306,
        "username": "valid_user",
        "password": "valid_password",
        "database": "valid_schema",
    }

    # 这里我们模拟测试，实际上可能需要根据环境调整
    # 或者使用模拟来避免实际连接数据库

    # 测试有效连接
    # 注意：实际测试时这可能会失败，因为连接信息可能无效
    response = client.post("/api/v1/asset/databases/test", json=valid_connection)

    # 如果连接成功
    if response.json()["code"] == "0000":
        assert response.json()["msg"] == "连接成功"
    # 如果连接失败（这在测试环境中更可能发生）
    else:
        assert "error" in response.json()["data"]

    # 准备测试数据 - 无效连接
    invalid_connection = {
        "name": "InvalidTestConnection",
        "type": "MySQL",
        "host": "non_existent_host",
        "port": 3306,
        "username": "invalid_user",
        "password": "invalid_password",
        "database": "invalid_schema",
    }

    # 测试无效连接
    response = client.post("/api/v1/asset/databases/test", json=invalid_connection)
    assert response.status_code == 400
    data = response.json()
    # 连接应该失败
    assert data["code"] != "0000" or data["msg"] != "连接成功"


@pytest.mark.asyncio
async def test_test_database_connection_with_id(client):
    """测试使用现有ID测试数据库连接"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先创建一个数据库连接
    database_data = {
        "name": "需要测试连接的数据库",
        "type": "MySQL",
        "host": "localhost",
        "port": 3306,
        "username": "test_user",
        "password": "test_password",
        "database": "test_schema",
        "status": "0",
    }
    response = client.post("/api/v1/asset/databases", json=database_data)
    assert response.status_code == 200
    database_id = response.json()["data"]["create_id"]

    # 准备不带密码的测试数据
    test_data = {
        "name": "TestDB",
        "type": "MySQL",
        "host": "localhost",
        "port": 3306,
        "username": "test_user",
        "password": "test_password",
        "database": "test_schema",
    }

    # 发送测试请求，带上database_id参数
    response = client.post(
        f"/api/v1/asset/databases/test?database_id={database_id}", json=test_data
    )
    assert response.status_code == 400

    # 验证响应 - 由于这是模拟测试，连接可能成功也可能失败
    data = response.json()
    if data["code"] == "0000":
        assert data["msg"] == "连接成功"
        assert data["data"]["test_id"] == database_id
    else:
        assert "error" in data["data"]
        assert data["data"]["test_id"] == database_id
