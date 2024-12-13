from app.models.report import Report


def test_get_report_list(client):
    """测试获取报告列表"""
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    assert response.json()["msg"] == "获取成功"


def test_create_report(client):
    """测试创建报告"""
    report_data = {
        "reportName": "测试报告",
        "reportType": "monthly",
        "reportDesc": "这是一个测试报告",
        "reportContent": "报告内容",
        "status": "1",
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "version": 1.00,
        "viewCount": 0,
        "collectCount": 0,
        "reportFormat": "PDF",
        "metric": 8,
        "createBy": "admin",
    }
    response = client.post("/api/v1/reports", json=report_data)
    assert response.status_code == 200
    result = response.json()
    assert result["msg"] == "创建成功"
    assert "create_id" in result["data"]
    report_id = result["data"]["create_id"]

    # 测试重复创建
    response = client.post("/api/v1/reports", json=report_data)
    assert response.status_code == 400
    assert response.json()["msg"] == "报告名称已存在"

    # 测试更新报告
    update_data = {"reportName": "更新后的报告", "reportDesc": "这是更新后的报告描述"}
    response = client.patch(f"/api/v1/reports/{report_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["msg"] == "更新成功"

    # 测试删除报告
    response = client.delete(f"/api/v1/reports/{report_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "删除成功"
