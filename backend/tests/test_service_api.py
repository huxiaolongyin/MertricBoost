# 1. 测试应用列表获取
def test_get_api_list(client):
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
    response = client.patch(f"/api/v1/service/api/{api_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["msg"] == "更新成功"

    # 删除API
    response = client.delete(f"/api/v1/service/api/{api_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "删除成功"
