# 1. 测试应用列表获取
def test_get_app_list(client):
    # 测试未提供用户名的情况
    response = client.get("/api/v1/service/app")
    assert response.status_code == 400
    assert response.json()["msg"] == "用户不存在"

    # 测试提供不存在的用户名
    response = client.get("/api/v1/service/app", params={"userName": "nonexistent"})
    assert response.status_code == 400
    assert response.json()["msg"] == "用户不存在"

    # 测试提供存在的用户名
    response = client.get("/api/v1/service/app", params={"userName": "admin"})
    assert response.status_code == 200
    assert response.json()["msg"] == "OK"


# 2. 测试应用创建\更新\删除
def test_create_app(client):
    app_data = {
        "appName": "新建测试应用",
        "appDesc": "这是一个新建的测试应用",
        "status": "1",
        "appKey": "test_app_key",
        "appSecret": "test_app_secret",
        "createBy": "admin",
    }
    response = client.post("/api/v1/service/app", json=app_data)
    assert response.status_code == 200
    create_result = response.json()
    assert create_result["msg"] == "创建成功"
    assert "create_id" in create_result["data"]

    app_id = create_result["data"]["create_id"]

    # 新建重复应用
    response = client.post("/api/v1/service/app", json=app_data)
    assert response.status_code == 400
    assert response.json()["msg"] == "应用名称已存在"

    # 更新应用信息
    update_data = {
        "appName": "已更新应用",
        "appDesc": "这是一个已更新的应用",
        "status": "1",
        "appKey": "test_app_key",
        "appSecret": "test_app_secret",
        "createBy": "admin",
    }
    response = client.patch(f"/api/v1/service/app/{app_id}", json=update_data)
    assert response.status_code == 200
    update_result = response.json()
    assert update_result["msg"] == "更新成功"
    assert "update_id" in update_result["data"]

    update_id = update_result["data"]["update_id"]

    # 删除应用
    response = client.delete(
        f"/api/v1/service/app/{update_id}", params={"userName": "admin"}
    )
    assert response.status_code == 200
    delete_result = response.json()
    assert delete_result["msg"] == "删除成功"
    assert "delete_id" in delete_result["data"]
