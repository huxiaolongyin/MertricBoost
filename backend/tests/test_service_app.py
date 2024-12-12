from fastapi.testclient import TestClient
from app import create_app

# 创建应用实例,
app = create_app()

# 测试数据
test_store_name = "test_store"
test_doc = "这是一个测试文档"


# 1. 测试应用列表获取
def test_get_app_list():
    # 使用 with 避免fastapi生命周期启动时,没有正确执行startup函数, 从而初始化ORM
    with TestClient(app) as client:
        response = client.get("/api/v1/service/app")
        assert response.status_code == 400
        assert response.json()["msg"] == "用户不存在"

        response = client.get("/api/v1/service/app", params={"userName": "admin"})
        assert response.status_code == 200
        assert response.json()["msg"] == "OK"
