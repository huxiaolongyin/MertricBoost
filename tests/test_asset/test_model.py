import pytest

from metricboost.core.ctx import CTX_USER_ID


# 测试获取模型列表
@pytest.mark.asyncio
async def test_get_models(client):
    """测试获取模型列表接口"""
    CTX_USER_ID.set(1)

    # 基本查询
    response = client.get("/api/v1/asset/model?page=1&page_size=10")

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "records" in data["data"]

    # 带过滤条件查询
    response = client.get(
        "/api/v1/asset/model?page=1&page_size=10&status=1&name=test&databaseId=1"
    )
    assert response.status_code == 200
    assert data["code"] == "0000"


# 测试创建模型
@pytest.mark.asyncio
async def test_create_model(client):
    """测试创建模型接口"""
    CTX_USER_ID.set(1)

    # 创建模型数据
    model_data = {
        "name": "需要创建的模型",
        "tableName": "test_table",
        "databaseId": 1,
        "columnsConf": [
            {
                "columnName": "answer_text",
                "columnType": "text",
                "columnComment": "问题内容",
                "isDimension": "1",
                "aggMethod": "",
                "format": "",
                "extraCaculate": "",
            }
        ],
    }
    response = client.post("/api/v1/asset/model", json=model_data)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 重复表名测试
    response = client.post("/api/v1/asset/model", json=model_data)
    assert response.status_code == 400
    assert "已存在" in response.json()["msg"]


# 测试更新模型
@pytest.mark.asyncio
async def test_update_model(client):
    """测试更新模型接口"""
    CTX_USER_ID.set(1)
    # 使用创建的测试数据
    model_data = {
        "name": "需要更新的模型",
        "tableName": "test_table2",
        "databaseId": 1,
        "columnsConf": [
            {
                "columnName": "answer_text",
                "columnType": "text",
                "columnComment": "问题内容",
                "isDimension": "1",
                "aggMethod": "",
                "format": "",
                "extraCaculate": "",
            }
        ],
    }
    response = client.post("/api/v1/asset/model", json=model_data)
    created_id = response.json()["data"]["create_id"]

    # 合法更新
    update_data = {
        "name": "已经更新的模型",
        "columnsConf": [
            {
                "columnName": "answer_text",
                "columnType": "text",
                "columnComment": "问题内容",
                "isDimension": "1",
                "aggMethod": "",
                "format": "",
                "extraCaculate": "",
            }
        ],
    }
    response = client.patch(f"/api/v1/asset/model/{created_id}", json=update_data)
    print(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 无效ID测试
    response = client.patch("/api/v1/asset/model/999999", json=update_data)
    assert response.status_code == 400


# 测试删除模型
@pytest.mark.asyncio
async def test_delete_model(client):
    """测试删除模型接口"""
    CTX_USER_ID.set(1)
    # 使用创建的测试数据
    model_data = {
        "name": "需要删除的模型",
        "tableName": "test_table3",
        "databaseId": 1,
        "columnsConf": [
            {
                "columnName": "answer_text",
                "columnType": "text",
                "columnComment": "问题内容",
                "isDimension": "1",
                "aggMethod": "",
                "format": "",
                "extraCaculate": "",
            }
        ],
    }
    response = client.post("/api/v1/asset/model", json=model_data)

    assert response.status_code == 200
    model_id = response.json()["data"]["create_id"]

    # 合法删除
    response = client.delete(f"/api/v1/asset/model/{model_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 重复删除测试
    response = client.delete(f"/api/v1/asset/model/{model_id}")
    assert response.status_code == 400


# 测试数据预览
@pytest.mark.asyncio
async def test_preview_model(client):
    """测试数据预览接口"""
    CTX_USER_ID.set(1)

    # 创建数据库连接
    json_data = {
        "name": "大数据结果数据库",
        "type": "MySQL",
        "host": "192.168.30.149",
        "port": 3636,
        "username": "htw_user",
        "password": "12345@HTW",
        "database": "ads",
        "status": "1",
        "description": "大数据结果数据库",
    }
    response = client.post("/api/v1/asset/databases", json=json_data)

    assert response.status_code == 200
    database_id = response.json()["data"]["create_id"]

    # 正常预览
    response = client.get(
        f"/api/v1/asset/model/preview?databaseId={database_id}&tableName=ads_aiui_service_stats"
    )

    assert response.status_code == 200
    data = response.json()
    assert "records" in data["data"]

    # 无效表测试
    response = client.get(
        f"/api/v1/asset/model/preview?databaseId={database_id}&tableName=invalid_table"
    )
    assert response.status_code == 400


# 测试元数据获取
@pytest.mark.asyncio
async def test_metadata(client):
    """测试元数据接口"""
    CTX_USER_ID.set(1)

    # 创建数据库连接
    json_data = {
        "name": "大数据结果数据库2",
        "type": "MySQL",
        "host": "192.168.30.149",
        "port": 3636,
        "username": "htw_user",
        "password": "12345@HTW",
        "database": "ads",
        "status": "1",
        "description": "大数据结果数据库",
    }
    response = client.post("/api/v1/asset/databases", json=json_data)
    database_id = response.json()["data"]["create_id"]

    # 表元数据
    response = client.get(f"/api/v1/asset/model/tables?databaseId={database_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"]["records"], list)

    # 字段元数据
    response = client.get(
        f"/api/v1/asset/model/tables/columns?databaseId={database_id}&tableName=ads_aiui_service_stats&editMode=add"
    )
    assert response.status_code == 200
    assert "tableComment" in data["data"]["records"][0]


# 测试异常情况
@pytest.mark.asyncio
async def test_error_cases(client):
    """测试异常情况处理"""
    CTX_USER_ID.set(1)

    # 无效分页参数
    response = client.get("/api/v1/asset/model?page=0&page_size=0")
    assert response.status_code == 422

    # 缺失必要参数
    response = client.get("/api/v1/asset/model/preview?databaseId=1")  # 缺少tableName
    assert response.status_code == 422

    # 无效JSON配置
    invalid_model = {
        "model_name": "invalid_model",
        "table_name": "invalid_table",
        "database_id": 1,
        "columns_conf": "invalid_json",  # 应该为字典
    }
    response = client.post("/api/v1/asset/model", json=invalid_model)
    assert response.status_code == 422
