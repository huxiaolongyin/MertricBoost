import pytest

from metricboost.core.ctx import CTX_USER_ID


@pytest.mark.asyncio
async def test_get_roles_list(client):
    """测试获取角色列表接口"""
    response = client.get("/api/v1/system/roles?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["total"] >= 1
    assert len(data["data"]["records"]) >= 1
    # 假设测试数据中有一个角色名为"普通用户"
    assert any(role["roleName"] == "普通用户" for role in data["data"]["records"])


@pytest.mark.asyncio
async def test_get_role_detail(client):
    """测试获取角色详情接口"""
    response = client.get("/api/v1/system/roles/1")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["id"] == 1
    # 假设ID为1的角色名为"测试"
    assert data["data"]["roleName"] == "普通用户"


@pytest.mark.asyncio
async def test_get_nonexistent_role(client):
    """测试获取不存在的角色详情接口"""
    response = client.get("/api/v1/system/roles/999")
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "4000"
    assert "不存在" in data["msg"]


@pytest.mark.asyncio
async def test_create_role(client):
    """测试创建角色接口"""
    # 准备测试数据
    role_data = {
        "roleName": "new_role",
        "roleCode": "R_NEW",
        "roleDesc": "This is a new test role",
        "status": "1",
    }

    # 发送请求
    response = client.post("/api/v1/system/roles", json=role_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "created_id" in data["data"]
    created_id = data["data"]["created_id"]

    # 验证角色是否真的创建成功
    check_response = client.get(f"/api/v1/system/roles/{created_id}")
    assert check_response.status_code == 200
    check_data = check_response.json()
    assert check_data["data"]["roleName"] == "new_role"
    assert check_data["data"]["roleCode"] == "R_NEW"


@pytest.mark.asyncio
async def test_create_duplicate_role(client):
    """测试创建重复角色代码的角色"""
    # 准备测试数据
    role_data = {
        "roleName": "duplicate_role",
        "roleCode": "R_NEW",  # 使用上一个测试中已创建的角色代码
        "roleDesc": "This will fail due to duplicate role code",
        "status": "1",
    }

    # 发送请求
    response = client.post("/api/v1/system/roles", json=role_data)

    # 验证响应
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "4090"  # 根据roles.py中的错误代码
    assert "已存在" in data["msg"].lower()


@pytest.mark.asyncio
async def test_update_role(client):
    """测试更新角色接口"""
    # 首先创建一个角色用于测试更新
    create_data = {
        "roleName": "update_test_role",
        "roleCode": "R_UPDATE",
        "roleDesc": "Role to be updated",
        "status": "1",
    }

    create_response = client.post("/api/v1/system/roles", json=create_data)
    assert create_response.status_code == 200
    create_data = create_response.json()
    role_id = create_data["data"]["created_id"]
    assert role_id > 0

    # 准备更新数据
    update_data = {
        "roleName": "Updated Role Name",
        "roleCode": "R_UPDATE",
        "roleDesc": "Updated role description",
        "status": "0",  # 改为禁用状态
    }

    # 发送更新请求
    response = client.patch(f"/api/v1/system/roles/{role_id}", json=update_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["updated_id"] == role_id

    # 验证角色是否真的更新成功
    check_response = client.get(f"/api/v1/system/roles/{role_id}")
    check_data = check_response.json()["data"]
    assert check_data["roleName"] == "Updated Role Name"
    assert check_data["roleDesc"] == "Updated role description"
    assert check_data["status"] == "0"


@pytest.mark.asyncio
async def test_delete_role(client):
    """测试删除角色接口"""
    # 首先创建一个角色用于测试删除
    create_data = {
        "roleName": "delete_test_role",
        "roleCode": "R_DELETE",
        "roleDesc": "Role to be deleted",
        "status": "1",
    }

    create_response = client.post("/api/v1/system/roles", json=create_data)
    create_data = create_response.json()
    role_id = create_data["data"]["created_id"]

    # 发送删除请求
    response = client.delete(f"/api/v1/system/roles/{role_id}")

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["deleted_id"] == role_id

    # 验证角色是否真的被删除
    check_response = client.get(f"/api/v1/system/roles/{role_id}")
    assert check_response.status_code == 400
    assert check_response.json()["code"] == "4000"  # 表示找不到资源


@pytest.mark.asyncio
async def test_batch_delete_roles(client):
    """测试批量删除角色接口"""
    # 创建多个角色用于测试批量删除
    role_ids = []
    for i in range(3):
        create_data = {
            "roleName": f"batch_delete_role_{i}",
            "roleCode": f"R_BATCH_{i}",
            "roleDesc": f"Role {i} to be batch deleted",
            "status": "1",
        }

        create_response = client.post("/api/v1/system/roles", json=create_data)
        create_data = create_response.json()
        role_ids.append(str(create_data["data"]["created_id"]))

    # 发送批量删除请求
    response = client.delete(f"/api/v1/system/roles?ids={','.join(role_ids)}")

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "deleted_ids" in data["data"]
    # 验证所有ID都在返回的删除列表中
    for role_id in role_ids:
        assert int(role_id) in data["data"]["deleted_ids"]

    # 验证所有角色是否真的被删除
    for role_id in role_ids:
        check_response = client.get(f"/api/v1/system/roles/{role_id}")
        assert check_response.status_code == 400


@pytest.mark.asyncio
async def test_get_role_menus(client):
    """测试获取角色菜单接口"""
    response = client.get("/api/v1/system/roles/1/menus")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "roleHome" in data["data"]
    assert "menuIds" in data["data"]
    assert isinstance(data["data"]["menuIds"], list)


@pytest.mark.asyncio
async def py(client):
    """测试更新角色菜单接口"""
    # 首先获取现有菜单ID
    get_response = client.get("/api/v1/system/roles/1/menus")
    assert get_response.status_code == 200
    current_menus = get_response.json()["data"]["menuIds"]

    # 准备更新数据(假设我们要添加ID为1的菜单)
    # update_data = {
    #     "roleHome": "/dashboard",
    #     "menuIds": current_menus + [1] if 1 not in current_menus else current_menus,
    # }
    update_data = {"roleHome": "/dashboard", "menuIds": [1]}

    # 发送更新请求
    response = client.patch("/api/v1/system/roles/1/menus", json=update_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["updated_role_home"] == "/dashboard"
    assert 1 in data["data"]["updated_menu_ids"]


@pytest.mark.asyncio
async def test_get_role_buttons(client):
    """测试获取角色按钮接口"""
    response = client.get("/api/v1/system/roles/1/buttons")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "buttonIds" in data["data"]
    assert isinstance(data["data"]["buttonIds"], list)


@pytest.mark.asyncio
async def test_update_role_buttons(client):
    """测试更新角色按钮接口"""
    # 准备更新数据(假设我们要添加ID为1和2的按钮)
    update_data = {"buttonIds": [1, 2]}

    # 发送更新请求
    response = client.patch("/api/v1/system/roles/1/buttons", json=update_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["button_ids"] == [1, 2]

    # 验证按钮是否真的更新成功
    check_response = client.get("/api/v1/system/roles/1/buttons")
    check_data = check_response.json()
    assert 1 in check_data["data"]["buttonIds"]
    assert 2 in check_data["data"]["buttonIds"]


@pytest.mark.asyncio
async def test_get_role_apis(client):
    """测试获取角色API接口"""
    response = client.get("/api/v1/system/roles/1/apis")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "apiIds" in data["data"]
    assert isinstance(data["data"]["apiIds"], list)


@pytest.mark.asyncio
async def test_update_role_apis(client):
    """测试更新角色API接口"""
    CTX_USER_ID.set(1)
    # 准备更新数据(假设我们要添加ID为1和2的API)

    api_data = {
        "method": "get",
        "path": "/api/test/update-api",
        "summary": "新创建API",
        "status": "0",
        "tags": ["system", "updated"],
    }

    # 发送更新请求
    response = client.post(f"/api/v1/system/apis", json=api_data)
    assert response.status_code == 200
    apiId = response.json()["data"]["created_id"]
    assert apiId > 0

    update_data = {"apiIds": [apiId]}
    print("update_data", update_data)

    # 发送更新请求
    response = client.patch("/api/v1/system/roles/1/apis", json=update_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["api_ids"] == [apiId]

    # 验证API是否真的更新成功
    check_response = client.get("/api/v1/system/roles/1/apis")
    check_data = check_response.json()
    assert apiId in check_data["data"]["apiIds"]
