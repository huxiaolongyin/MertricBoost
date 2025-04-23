import pytest

from metricboost.core.ctx import CTX_USER_ID


@pytest.mark.asyncio
async def test_get_apis_list(client):
    """测试获取API列表接口"""
    CTX_USER_ID.set(1)
    response = client.get("/api/v1/system/apis?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "total" in data["data"]
    assert "records" in data["data"]
    assert isinstance(data["data"]["records"], list)


@pytest.mark.asyncio
async def test_get_apis_with_filters(client):
    """测试带过滤条件获取API列表接口"""
    CTX_USER_ID.set(1)
    response = client.get(
        "/api/v1/system/apis?page=1&page_size=10&path=/api&summary=测试&tags=system&status=1"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "total" in data["data"]
    assert "records" in data["data"]


@pytest.mark.asyncio
async def test_get_api_detail(client):
    """测试获取API详情接口"""
    # 首先获取API列表以获取有效的API ID
    CTX_USER_ID.set(1)
    list_response = client.get("/api/v1/system/apis?page=1&page_size=1")
    list_data = list_response.json()
    if list_data["data"]["total"] > 0:
        api_id = list_data["data"]["records"][0]["id"]

        # 获取特定API详情
        response = client.get(f"/api/v1/system/apis/{api_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0000"
        assert "method" in data["data"]
        assert "path" in data["data"]
        assert "summary" in data["data"]
        assert "tags" in data["data"]


@pytest.mark.asyncio
async def test_get_apis_tree(client):
    """测试获取API树接口"""
    response = client.get("/api/v1/system/apis/tree/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert isinstance(data["data"], list)

    # 如果数据不为空，检查树结构
    if data["data"]:
        item = data["data"][0]
        assert "id" in item
        assert "summary" in item
        if "children" in item:
            assert isinstance(item["children"], list)


@pytest.mark.asyncio
async def test_create_api(client):
    """测试创建API接口"""
    api_data = {
        "method": "get",
        "path": "/api/test/new-api",
        "summary": "测试API",
        "tags": "system|test",  # 或者直接使用列表 ["system", "test"]
        "status": "1",
    }

    response = client.post("/api/v1/system/apis", json=api_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "created_id" in data["data"]

    # 获取创建的API ID
    created_id = data["data"]["created_id"]

    # 验证API是否真的创建成功
    check_response = client.get(f"/api/v1/system/apis/{created_id}")
    assert check_response.status_code == 200
    check_data = check_response.json()
    assert check_data["data"]["path"] == "/api/test/new-api"
    assert check_data["data"]["summary"] == "测试API"


@pytest.mark.asyncio
async def test_update_api(client):
    """测试更新API接口"""
    # 首先创建一个API用于测试更新
    create_data = {
        "method": "get",
        "path": "/api/test/update-api",
        "summary": "待更新API",
        "tags": ["system", "test"],
        "status": "1",
    }

    create_response = client.post("/api/v1/system/apis", json=create_data)
    create_data = create_response.json()
    api_id = create_data["data"]["created_id"]

    # 准备更新数据
    update_data = {
        "method": "get",
        "path": "/api/test/update-api",
        "summary": "已更新API",
        "status": "0",
        "tags": ["system", "updated"],
    }

    # 发送更新请求
    response = client.patch(f"/api/v1/system/apis/{api_id}", json=update_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "updated_id" in data["data"]
    assert data["data"]["updated_id"] == api_id

    # 验证API是否真的更新成功
    check_response = client.get(f"/api/v1/system/apis/{api_id}")
    check_data = check_response.json()["data"]
    assert check_data["summary"] == "已更新API"
    assert check_data["status"] == "0"
    assert set(check_data["tags"]) == {"system", "updated"}


@pytest.mark.asyncio
async def test_delete_api(client):
    """测试删除API接口"""
    # 首先创建一个API用于测试删除
    create_data = {
        "method": "get",
        "path": "/api/test/delete-api",
        "summary": "待删除API",
        "tags": "system|test",
        "status": "1",
    }

    create_response = client.post("/api/v1/system/apis", json=create_data)
    create_data = create_response.json()
    api_id = create_data["data"]["created_id"]

    # 发送删除请求
    response = client.delete(f"/api/v1/system/apis/{api_id}")

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["deleted_id"] == api_id

    # 验证API是否真的被删除
    check_response = client.get(f"/api/v1/system/apis/{api_id}")
    # 应当返回错误，因为API已被删除
    assert check_response.status_code != 200 or check_response.json()["code"] != "0000"


@pytest.mark.asyncio
async def test_batch_delete_apis(client):
    """测试批量删除API接口"""
    # 创建多个API用于测试批量删除
    api_ids = []
    for i in range(3):
        create_data = {
            "method": "get",
            "path": f"/api/test/batch-delete-{i}",
            "summary": f"批量删除测试API {i}",
            "tags": "system|test",
            "status": "1",
        }

        create_response = client.post("/api/v1/system/apis", json=create_data)
        create_data = create_response.json()
        api_ids.append(str(create_data["data"]["created_id"]))

    # 发送批量删除请求
    response = client.delete(f"/api/v1/system/apis?ids={','.join(api_ids)}")

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "deleted_ids" in data["data"]

    # 验证API是否真的被删除
    for api_id in api_ids:
        check_response = client.get(f"/api/v1/system/apis/{api_id}")
        # 应当返回错误，因为API已被删除
        assert (
            check_response.status_code != 200 or check_response.json()["code"] != "0000"
        )


@pytest.mark.asyncio
async def test_refresh_apis(client):
    """测试刷新API列表接口"""
    CTX_USER_ID.set(1)
    response = client.post("/api/v1/system/apis/refresh/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 验证API列表是否被刷新 - 可以通过检查列表数量变化
    list_response = client.get("/api/v1/system/apis?page=1&page_size=10")
    assert list_response.status_code == 200
    assert list_response.json()["code"] == "0000"
