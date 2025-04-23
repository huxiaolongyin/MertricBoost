import pytest

from metricboost.core.ctx import CTX_USER_ID


@pytest.mark.asyncio
async def test_get_tags(client):
    """测试获取标签列表接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 基本标签列表查询
    response = client.get("/api/v1/asset/tag?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["data"]["total"] >= 1
    assert len(data["data"]["records"]) >= 1
    assert isinstance(data["data"]["records"], list)

    # 测试带名称过滤条件的查询
    response = client.get("/api/v1/asset/tag?page=1&page_size=10&tagName=test")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"


@pytest.mark.asyncio
async def test_create_tag(client):
    """测试创建标签接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 准备测试数据
    tag_data = {"tagName": "测试标签", "tagDesc": "用于测试的标签"}

    # 发送创建请求
    response = client.post("/api/v1/asset/tag", json=tag_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "创建成功"
    assert "create_id" in data["data"]

    # 记录创建的ID，用于后续测试
    created_id = data["data"]["create_id"]

    # 验证创建结果
    check_response = client.get(f"/api/v1/asset/tag?tagName=测试标签")
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    assert len(check_data["data"]["records"]) > 0
    assert any(
        record["tagName"] == "测试标签" for record in check_data["data"]["records"]
    )

    return created_id  # 返回创建的ID供其他测试使用


@pytest.mark.asyncio
async def test_update_tag(client):
    """测试更新标签接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先创建一个标签
    tag_data = {"tagName": "新建的一个标签", "tagDesc": "用于测试的标签"}
    response = client.post("/api/v1/asset/tag", json=tag_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    tag_id = data["data"]["create_id"]

    # 准备更新数据
    update_data = {"tagName": "更新后的标签", "tagDesc": "已更新的测试标签"}

    # 发送更新请求
    response = client.patch(f"/api/v1/asset/tag/{tag_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "更新成功"
    assert data["data"]["update_id"] == tag_id

    # 验证更新结果
    check_response = client.get(f"/api/v1/asset/tag?tagName=更新后的标签")
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    assert len(check_data["data"]["records"]) > 0
    found = False
    for record in check_data["data"]["records"]:
        if record["id"] == tag_id:
            assert record["tagName"] == "更新后的标签"
            assert record["tagDesc"] == "已更新的测试标签"
            found = True
            break
    assert found, "更新后的标签记录未找到"

    return tag_id  # 返回ID供其他测试使用


@pytest.mark.asyncio
async def test_delete_tag(client):
    """测试删除标签接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先创建一个标签
    tag_data = {"tagName": "新建的一个标签", "tagDesc": "用于测试的标签"}
    response = client.post("/api/v1/asset/tag", json=tag_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    tag_id = data["data"]["create_id"]

    # 发送删除请求
    response = client.delete(f"/api/v1/asset/tag/{tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert data["msg"] == "删除成功"
    assert data["data"]["delete_id"] == tag_id

    # 验证删除结果 - 应该找不到该记录
    check_response = client.get(f"/api/v1/asset/tag?page=1&page_size=10")
    check_data = check_response.json()
    assert check_data["code"] == "0000"
    records = check_data["data"]["records"]
    assert not any(record["id"] == tag_id for record in records), "标签记录未被成功删除"


@pytest.mark.asyncio
async def test_batch_delete_tag(client):
    """测试批量删除标签接口"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 创建多个标签用于测试批量删除
    tag_ids = []
    for i in range(3):
        # 准备测试数据
        tag_data = {
            "tagName": f"批量删除测试标签{i}",
            "tagDesc": f"批量删除测试标签{i}",
        }

        # 发送创建请求
        response = client.post("/api/v1/asset/tag", json=tag_data)
        data = response.json()
        tag_ids.append(str(data["data"]["create_id"]))

    # 发送批量删除请求
    response = client.delete(f"/api/v1/asset/tag?ids={','.join(tag_ids)}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "0000"
    assert "deleted_ids" in data["data"]

    # 验证删除结果 - 所有记录都应该被删除
    for tag_id in tag_ids:
        check_response = client.get(f"/api/v1/asset/tag?page=1&page_size=10")
        check_data = check_response.json()
        records = check_data["data"]["records"]
        assert not any(
            record["id"] == int(tag_id) for record in records
        ), f"标签记录 {tag_id} 未被成功删除"


# @pytest.mark.asyncio
# async def test_get_metric_tags(client):
#     """测试获取标签指标关联接口"""
#     # 设置测试用户ID上下文
#     CTX_USER_ID.set(1)

#     # 基本查询
#     response = client.get("/api/v1/asset/metric-tag")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["code"] == "0000"
#     assert "records" in data["data"]

#     # 按指标ID过滤查询
#     response = client.get("/api/v1/asset/metric-tag?metricIds=1")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["code"] == "0000"

#     # 按标签名称过滤查询
#     response = client.get("/api/v1/asset/metric-tag?tagName=test")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["code"] == "0000"


# @pytest.mark.asyncio
# async def test_create_metric_tag(client):
#     """测试创建标签指标关联接口"""
#     # 设置测试用户ID上下文
#     CTX_USER_ID.set(1)

#     # 先创建一个标签
#     tag_data = {"tagName": "指标关联测试标签", "tagDesc": "用于测试指标关联的标签"}
#     tag_response = client.post("/api/v1/asset/tag", json=tag_data)
#     tag_name = "指标关联测试标签"

#     # 准备测试数据 - 假设有一个ID为1的指标
#     metric_id = 1
#     metric_tag_data = {"metricId": metric_id, "tag": tag_name}

#     # 发送创建请求
#     response = client.post("/api/v1/asset/metric-tag", json=metric_tag_data)
#     assert response.status_code == 200
#     data = response.json()

#     # 如果创建失败(可能因为指标不存在)，则跳过后续测试
#     if data["code"] != "0000":
#         pytest.skip(f"创建标签指标关联失败: {data['msg']}")

#     assert data["msg"] == "创建成功"
#     assert "create_id" in data["data"]

#     # 验证创建结果
#     check_response = client.get(f"/api/v1/asset/metric-tag?metricIds={metric_id}")
#     check_data = check_response.json()
#     assert check_data["code"] == "0000"

#     # 清理 - 删除关联
#     client.delete(f"/api/v1/asset/metric-tag?metricId={metric_id}&tag={tag_name}")

#     return {"metric_id": metric_id, "tag": tag_name}


# @pytest.mark.asyncio
# async def test_delete_metric_tag(client):
#     """测试删除标签指标关联接口"""
#     # 设置测试用户ID上下文
#     CTX_USER_ID.set(1)

#     # 先创建一个标签和关联
#     relation = await test_create_metric_tag(client)
#     metric_id = relation["metric_id"]
#     tag_name = relation["tag"]

#     # 创建关联 - 如果前面的测试已删除
#     metric_tag_data = {"metricId": metric_id, "tag": tag_name}
#     client.post("/api/v1/asset/metric-tag", json=metric_tag_data)

#     # 发送删除请求
#     response = client.delete(
#         f"/api/v1/asset/metric-tag?metricId={metric_id}&tag={tag_name}"
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["code"] == "0000"
#     assert data["msg"] == "删除成功"
#     assert f"指标id[{metric_id}]，标签[{tag_name}]" in data["data"]["delete_id"]

#     # 验证删除结果 - 应该找不到该记录
#     check_response = client.get(f"/api/v1/asset/metric-tag?metricIds={metric_id}")
#     check_data = check_response.json()
#     assert check_data["code"] == "0000"
#     records = check_data["data"]["records"]
#     assert not any(
#         record.get("tag") == tag_name and record.get("metricId") == metric_id
#         for record in records
#     ), "标签指标关联记录未被成功删除"


# @pytest.mark.asyncio
# async def test_batch_create_metric_tag(client):
#     """测试批量创建标签指标关联接口"""
#     # 设置测试用户ID上下文
#     CTX_USER_ID.set(1)

#     # 先创建几个标签
#     tag_names = []
#     for i in range(2):
#         tag_data = {
#             "tagName": f"批量关联测试标签{i}",
#             "tagDesc": f"批量关联测试标签{i}",
#         }
#         client.post("/api/v1/asset/tag", json=tag_data)
#         tag_names.append(f"批量关联测试标签{i}")

#     # 准备测试数据 - 假设有ID为1和2的指标
#     metric_ids = [1, 2]
#     metric_tag_list = []

#     for metric_id in metric_ids:
#         for tag_name in tag_names:
#             metric_tag_list.append({"metricId": metric_id, "tag": tag_name})

#     # 发送批量创建请求
#     response = client.post("/api/v1/asset/metric-tag/batch", json=metric_tag_list)
#     assert response.status_code == 200
#     data = response.json()

#     # 如果创建失败(可能因为指标不存在)，则跳过后续测试
#     if data["code"] != "0000":
#         pytest.skip(f"批量创建标签指标关联失败: {data['msg']}")

#     # 清理 - 批量删除关联
#     batch_delete_items = []
#     for metric_id in metric_ids:
#         for tag_name in tag_names:
#             batch_delete_items.append({"metricId": metric_id, "tag": tag_name})

#     client.delete("/api/v1/asset/metric-tag/batch", json=batch_delete_items)


# @pytest.mark.asyncio
# async def test_batch_delete_metric_tag(client):
#     """测试批量删除标签指标关联接口"""
#     # 设置测试用户ID上下文
#     CTX_USER_ID.set(1)

#     # 先创建几个标签
#     tag_names = []
#     for i in range(2):
#         tag_data = {
#             "tagName": f"批量删除关联测试标签{i}",
#             "tagDesc": f"批量删除关联测试标签{i}",
#         }
#         client.post("/api/v1/asset/tag", json=tag_data)
#         tag_names.append(f"批量删除关联测试标签{i}")

#     # 准备测试数据 - 假设有ID为1和2的指标
#     metric_ids = [1, 2]
#     metric_tag_list = []

#     for metric_id in metric_ids:
#         for tag_name in tag_names:
#             metric_tag_list.append({"metricId": metric_id, "tag": tag_name})

#     # 先创建关联
#     client.post("/api/v1/asset/metric-tag/batch", json=metric_tag_list)

#     # 准备批量删除请求数据
#     batch_delete_items = []
#     for metric_id in metric_ids:
#         for tag_name in tag_names:
#             batch_delete_items.append({"metricId": metric_id, "tag": tag_name})

#     # 发送批量删除请求
#     response = client.delete("/api/v1/asset/metric-tag/batch", json=batch_delete_items)
#     assert response.status_code == 200
#     data = response.json()

#     # 验证删除结果
#     for metric_id in metric_ids:
#         check_response = client.get(f"/api/v1/asset/metric-tag?metricIds={metric_id}")
#         check_data = check_response.json()
#         assert check_data["code"] == "0000"
#         records = check_data["data"]["records"]
#         for tag_name in tag_names:
#             assert not any(
#                 record.get("tag") == tag_name and record.get("metricId") == metric_id
#                 for record in records
#             ), f"标签指标关联记录(指标:{metric_id},标签:{tag_name})未被成功删除"


@pytest.mark.asyncio
async def test_tag_cache_invalidation(client):
    """测试标签缓存失效机制"""
    # 设置测试用户ID上下文
    CTX_USER_ID.set(1)

    # 先获取标签列表，触发缓存
    client.get("/api/v1/asset/tag?page=1&page_size=10")

    # 创建新标签
    tag_data = {"tagName": "缓存测试标签", "tagDesc": "用于测试缓存失效"}
    response = client.post("/api/v1/asset/tag", json=tag_data)
    created_id = response.json()["data"]["create_id"]

    # 再次获取列表，应该能看到新创建的标签（证明缓存已更新）
    check_response = client.get("/api/v1/asset/tag?page=1&page_size=10")
    check_data = check_response.json()
    assert any(
        record["id"] == created_id for record in check_data["data"]["records"]
    ), "缓存未正确失效"

    # 删除该记录进行清理
    client.delete(f"/api/v1/asset/tag/{created_id}")
