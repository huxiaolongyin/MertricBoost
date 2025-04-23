import pytest

from metricboost.core.ctx import CTX_USER_ID
from metricboost.models.enums import DomainType


@pytest.mark.asyncio
async def test_get_domains(client):
    """测试获取域列表接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 基本域列表查询
    response = client.get("/api/v1/asset/domains?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "total" in data["data"]
    assert "records" in data["data"]
    assert isinstance(data["data"]["records"], list)

    # 测试按域类型过滤 - 数据域
    response = client.get("/api/v1/asset/domains?page=1&page_size=10&domainType=1")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 测试按域类型过滤 - 主题域
    response = client.get("/api/v1/asset/domains?page=1&page_size=10&domainType=2")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"

    # 测试带名称过滤条件的查询
    response = client.get("/api/v1/asset/domains?page=1&page_size=10&domainName=test")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"


@pytest.mark.asyncio
async def test_create_data_domain(client):
    """测试创建数据域接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 准备测试数据
    domain_data = {
        "domainName": "测试数据域",
        "domainDesc": "用于测试的数据域",
        "domainType": "1",
    }

    # 发送创建请求
    response = client.post("/api/v1/asset/domains", json=domain_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "创建成功"
    assert "create_id" in data["data"]

    # 记录创建的ID，用于后续测试
    created_id = data["data"]["create_id"]

    # 验证创建结果
    check_response = client.get(
        f"/api/v1/asset/domains?domainName=测试数据域&domainType={DomainType.DATA}"
    )
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    assert len(check_data["data"]["records"]) > 0
    assert any(
        record["domainName"] == "测试数据域" for record in check_data["data"]["records"]
    )

    return created_id  # 返回创建的ID供其他测试使用


@pytest.mark.asyncio
async def test_create_topic_domain(client):
    """测试创建主题域接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 准备测试数据
    domain_data = {
        "domainName": "测试的主题域",
        "domainDesc": "用于测试的主题域",
        "domainType": "2",
    }

    # 发送创建请求
    response = client.post("/api/v1/asset/domains", json=domain_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "创建成功"
    assert "create_id" in data["data"]

    # 验证创建结果
    check_response = client.get(
        f"/api/v1/asset/domains?domainName=测试主题域&domainType={DomainType.TOPIC}"
    )
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    assert len(check_data["data"]["records"]) > 0
    assert any(
        record["domainName"] == "测试主题域" for record in check_data["data"]["records"]
    )


@pytest.mark.asyncio
async def test_update_domain(client):
    """测试更新域信息接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先创建一个数据域
    domain_data = {
        "domainName": "需要更新的测试主题域",
        "domainDesc": "用于测试的主题域",
        "domainType": DomainType.TOPIC,
    }

    # 发送创建请求
    response = client.post("/api/v1/asset/domains", json=domain_data)
    assert response.status_code == 200
    data = response.json()
    domain_id = data["data"]["create_id"]

    # 准备更新数据
    update_data = {
        "domainName": "更新后的数据域",
        "domainDesc": "已更新的测试数据域",
        "domainType": DomainType.DATA,
    }

    # 发送更新请求
    response = client.patch(f"/api/v1/asset/domains/{domain_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "更新成功"
    assert data["data"]["update_id"] == domain_id

    # 验证更新结果
    check_response = client.get(f"/api/v1/asset/domains?domainName=更新后的数据域")
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    assert len(check_data["data"]["records"]) > 0
    found = False
    for record in check_data["data"]["records"]:
        if record["id"] == domain_id:
            assert record["domainName"] == "更新后的数据域"
            assert record["domainDesc"] == "已更新的测试数据域"
            found = True
            break
    assert found, "更新后的域记录未找到"

    return domain_id  # 返回ID供其他测试使用


@pytest.mark.asyncio
async def test_delete_domain(client):
    """测试删除域信息接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先创建一个数据域
    domain_data = {
        "domainName": "需要删除的测试主题域",
        "domainDesc": "用于测试的主题域",
        "domainType": DomainType.TOPIC,
    }

    # 发送创建请求
    response = client.post("/api/v1/asset/domains", json=domain_data)
    assert response.status_code == 200
    data = response.json()
    domain_id = data["data"]["create_id"]

    # 发送删除请求
    response = client.delete(f"/api/v1/asset/domains/{domain_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "删除成功"
    assert data["data"]["delete_id"] == domain_id

    # 验证删除结果 - 应该找不到该记录
    check_response = client.get(f"/api/v1/asset/domains?page=1&page_size=10")
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    records = check_data["data"]["records"]
    assert not any(
        record["id"] == domain_id for record in records
    ), "域记录未被成功删除"


@pytest.mark.asyncio
async def test_batch_delete_domain(client):
    """测试批量删除域信息接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 创建多个域用于测试批量删除
    domain_ids = []
    for i in range(3):
        # 准备测试数据
        domain_data = {
            "domainName": f"批量删除测试域{i}",
            "domainDesc": f"批量删除测试域{i}",
            "domainType": DomainType.DATA if i % 2 == 0 else DomainType.TOPIC,
        }

        # 发送创建请求
        response = client.post("/api/v1/asset/domains", json=domain_data)
        data = response.json()
        domain_ids.append(str(data["data"]["create_id"]))

    # 发送批量删除请求
    response = client.delete(f"/api/v1/asset/domains?ids={','.join(domain_ids)}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "deleted_ids" in data["data"]

    # 验证删除结果 - 所有记录都应该被删除
    for domain_id in domain_ids:
        check_response = client.get(f"/api/v1/asset/domains?page=1&page_size=10")
        check_data = check_response.json()
        records = check_data["data"]["records"]
        assert not any(
            record["id"] == int(domain_id) for record in records
        ), f"域记录 {domain_id} 未被成功删除"


@pytest.mark.asyncio
async def test_cache_invalidation(client):
    """测试缓存失效机制"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先获取域列表，触发缓存
    client.get("/api/v1/asset/domains?page=1&page_size=10")

    # 创建新域
    domain_data = {
        "domainName": "缓存测试域",
        "domainDesc": "用于测试缓存失效",
        "domainType": DomainType.DATA,
    }
    response = client.post("/api/v1/asset/domains", json=domain_data)
    created_id = response.json()["data"]["create_id"]

    # 再次获取列表，应该能看到新创建的域（证明缓存已更新）
    check_response = client.get("/api/v1/asset/domains?page=1&page_size=10")
    check_data = check_response.json()
    assert any(
        record["id"] == created_id for record in check_data["data"]["records"]
    ), "缓存未正确失效"

    # 删除该记录进行清理
    client.delete(f"/api/v1/asset/domains/{created_id}")
