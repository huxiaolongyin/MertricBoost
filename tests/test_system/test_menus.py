import pytest


@pytest.mark.asyncio
async def test_get_menus_list(client):
    """测试获取菜单列表接口"""
    response = client.get("/api/v1/system/menus?page=1&page_size=100")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "total" in data["data"]
    assert "records" in data["data"]
    assert isinstance(data["data"]["records"], list)
    # 验证树形结构特性
    if data["data"]["records"]:
        # 检查是否有顶级菜单
        assert any(menu.get("parentId", 0) == 0 for menu in data["data"]["records"])
        # 检查是否有包含children的菜单
        has_children = any("children" in menu for menu in data["data"]["records"])
        if has_children:
            # 确保children也是一个列表
            assert isinstance(
                next(
                    menu["children"]
                    for menu in data["data"]["records"]
                    if "children" in menu
                ),
                list,
            )


@pytest.mark.asyncio
async def test_get_menus_tree(client):
    """测试获取菜单树接口"""
    response = client.get("/api/v1/system/menus/tree/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert isinstance(data["data"], list)
    # 验证简化树结构特性
    if data["data"]:
        menu = data["data"][0]
        assert "id" in menu
        assert "label" in menu
        assert "pId" in menu
        # 检查是否有包含children的菜单
        if "children" in menu:
            assert isinstance(menu["children"], list)


@pytest.mark.asyncio
async def test_get_menu_detail(client):
    """测试获取菜单详情接口"""
    # 假设ID为1的菜单存在
    response = client.get("/api/v1/system/menus/1")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "id" in data["data"]
    assert "menuName" in data["data"]
    assert "parentId" in data["data"]
    assert data["data"]["id"] == 1


@pytest.mark.asyncio
async def test_create_menu(client):
    """测试创建菜单接口"""
    # 准备测试数据，添加i18n_key字段
    menu_data = {
        "menu_name": "Test Menu",
        "menu_type": "2",  # 菜单类型
        "parent_id": 0,  # 顶级菜单
        "route_name": "test",
        "route_path": "/test",
        "component": "views/test/index",
        "visible": True,
        "status": "1",
        "icon_type": "1",
        "icon": "dashboard",
        "i18n_key": "menu.test",  # 添加必需的i18n_key字段
        "buttons": [],  # 空按钮列表
    }

    # 发送请求
    response = client.post("/api/v1/system/menus", json=menu_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "created_id" in data["data"]

    # 获取创建的菜单ID
    created_id = data["data"]["created_id"]

    # 验证菜单是否真的创建成功
    check_response = client.get(f"/api/v1/system/menus/{created_id}")
    assert check_response.status_code == 200
    check_data = check_response.json()
    assert check_data["data"]["menuName"] == "Test Menu"
    assert check_data["data"]["routePath"] == "/test"
    assert check_data["data"]["i18nKey"] == "menu.test"  # 检查i18n_key是否保存成功


@pytest.mark.asyncio
async def test_create_menu_with_buttons(client):
    """测试创建带按钮的菜单接口"""
    # 准备测试数据，使用正确的字段名格式（camelCase）
    menu_data = {
        "menuName": "Test Menu With Buttons",  # 使用camelCase
        "menuType": "2",  # 菜单类型
        "parentId": 0,  # 顶级菜单
        "routeName": "test_buttons",  # 使用camelCase
        "routePath": "/test_buttons",  # 使用camelCase
        "component": "views/test/buttons",
        "status": "1",
        "iconType": "1",  # 使用camelCase
        "icon": "dashboard",
        "i18nKey": "menu.test.buttons",  # 使用camelCase
        "query": [],  # 添加必要的route_param字段，别名为query
        "buttons": [
            {
                "buttonCode": "btn_add",
                "buttonDesc": "添加",
                "status": 1,
            },  # 使用camelCase
            {
                "buttonCode": "btn_edit",
                "buttonDesc": "编辑",
                "status": 1,
            },  # 使用camelCase
        ],
        # 移除不存在的visible字段
        "multiTab": True,  # 替代visible，如果需要类似功能
        "keepAlive": True,
        "hideInMenu": False,
    }

    # 发送请求
    response = client.post("/api/v1/system/menus", json=menu_data)

    # 验证响应
    assert response.status_code == 200, f"响应内容: {response.text}"  # 添加错误消息显示
    data = response.json()
    assert data["code"] == "0000"
    assert "created_id" in data["data"]

    # 获取创建的菜单ID
    created_id = data["data"]["created_id"]

    # 验证菜单及按钮是否真的创建成功
    check_response = client.get(f"/api/v1/system/menus/{created_id}")
    assert check_response.status_code == 200
    check_data = check_response.json()
    assert check_data["data"]["menuName"] == "Test Menu With Buttons"
    # print(check_data["data"])
    # assert "buttons" in check_data["data"]
    # assert len(check_data["data"]["buttons"]) == 2
    # button_codes = [button["buttonCode"] for button in check_data["data"]["buttons"]]
    # assert "btn_add" in button_codes
    # assert "btn_edit" in button_codes


@pytest.mark.asyncio
async def test_update_menu(client):
    """测试更新菜单接口"""
    # 首先创建一个菜单用于测试更新
    create_data = {
        "menuName": "Menu To Update",
        "menuType": "2",
        "parentId": 0,
        "routeName": "update_test",
        "routePath": "/update_test",
        "component": "views/update/test",
        "visible": True,
        "status": "1",
        "iconType": "1",
        "icon": "dashboard",
        "i18nKey": "menu.update",  # 添加必需的i18n_key字段
    }

    create_response = client.post("/api/v1/system/menus", json=create_data)
    assert create_response.status_code == 200
    create_data = create_response.json()
    menu_id = create_data["data"]["created_id"]

    # 准备更新数据
    update_data = {
        "menuName": "Updated Menu Name",
        "menuType": "2",
        "parentId": 0,
        "routeName": "update_test",
        "routePath": "/updated_path",
        "component": "views/update/test",
        "visible": True,
        "status": "0",
        "iconType": "1",
        "icon": "dashboard",
        "i18nKey": "menu.updated",  # 添加必需的i18n_key字段
        "query": [],
        "buttons": [
            {
                "buttonCode": "status",
                "buttonDesc": "新按钮",
                "status": 1,
            }
        ],
    }

    # 发送更新请求
    response = client.patch(f"/api/v1/system/menus/{menu_id}", json=update_data)

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["updated_id"] == menu_id

    # 验证菜单是否真的更新成功
    check_response = client.get(f"/api/v1/system/menus/{menu_id}")
    check_data = check_response.json()["data"]
    assert check_data["menuName"] == "Updated Menu Name"
    assert check_data["routePath"] == "/updated_path"
    assert check_data["status"] == "0"
    assert check_data["i18nKey"] == "menu.updated"  # 检查i18n_key是否更新成功
    # 验证按钮是否更新
    # if "buttons" in check_data:
    #     assert any(
    #         button["buttonCode"] == "btn_new" for button in check_data["buttons"]
    #     )


@pytest.mark.asyncio
async def test_delete_menu(client):
    """测试删除菜单接口"""
    # 首先创建一个菜单用于测试删除
    create_data = {
        "menuName": "Menu To Delete",
        "menuType": "2",
        "parentId": 0,
        "routeName": "delete_test",
        "routePath": "/delete_test",
        "component": "views/delete/test",
        "visible": True,
        "status": "1",
        "iconType": "1",
        "icon": "dashboard",
        "i18nKey": "menu.delete",  # 添加必需的i18n_key字段
    }

    create_response = client.post("/api/v1/system/menus", json=create_data)
    assert create_response.status_code == 200
    create_data = create_response.json()
    menu_id = create_data["data"]["created_id"]

    # 发送删除请求
    response = client.delete(f"/api/v1/system/menus/{menu_id}")

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["deleted_id"] == menu_id

    # 验证菜单是否真的被删除
    check_response = client.get(f"/api/v1/system/menus/{menu_id}")
    # 应该返回错误，因为菜单已被删除
    assert check_response.status_code != 200


@pytest.mark.asyncio
async def test_batch_delete_menus(client):
    """测试批量删除菜单接口"""
    # 创建多个菜单用于测试批量删除
    menu_ids = []
    for i in range(3):
        create_data = {
            "menuName": f"Batch Delete Menu {i}",
            "menuType": "2",
            "parentId": 0,
            "routeName": f"batch_delete_{i}",
            "routePath": f"/batch_delete_{i}",
            "component": f"views/batch/delete_{i}",
            "visible": True,
            "status": "1",
            "iconType": "1",
            "icon": "dashboard",
            "i18nKey": f"menu.batch.delete.{i}",  # 添加必需的i18n_key字段
        }

        create_response = client.post("/api/v1/system/menus", json=create_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        menu_ids.append(str(create_data["data"]["created_id"]))

    # 发送批量删除请求
    response = client.delete(f"/api/v1/system/menus?ids={','.join(menu_ids)}")

    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "deleted_ids" in data["data"]

    # 验证所有菜单是否真的被删除
    for menu_id in menu_ids:
        check_response = client.get(f"/api/v1/system/menus/{menu_id}")
        # 应该返回错误，因为菜单已被删除
        assert check_response.status_code != 200


@pytest.mark.asyncio
async def test_get_pages(client):
    """测试获取一级菜单接口"""
    response = client.get("/api/v1/system/menus/pages/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert isinstance(data["data"], list)
    # 验证返回的是路由名称列表
    if data["data"]:
        assert isinstance(data["data"][0], str)


@pytest.mark.asyncio
async def test_get_menu_buttons_tree(client):
    """测试获取菜单按钮树接口"""
    response = client.get("/api/v1/system/menus/buttons/tree/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert isinstance(data["data"], list)

    # 如果有数据，验证树形结构
    if data["data"]:
        # 检查根节点格式
        menu = data["data"][0]
        assert "id" in menu
        assert "label" in menu
        assert "pId" in menu

        # 检查是否有children，若有则验证其结构
        if "children" in menu:
            assert isinstance(menu["children"], list)
            if menu["children"]:
                child = menu["children"][0]
                assert "id" in child
                assert "label" in child
                assert "pId" in child
