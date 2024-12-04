import { request } from '../request';

// 获取数据库
export function fetchDatabaseList(params?: Api.SystemManage.DatabaseSearchParams) {
  return request<Api.SystemManage.DatabaseList>({
    url: '/asset/databases',
    method: 'get',
    params
  });
}

// 添加数据库
export function fetchAddDatabase(data?: Api.SystemManage.DatabaseAddParams) {
  return request<Api.SystemManage.DatabaseList, 'json'>({
    url: '/asset/databases',
    method: 'post',
    data
  });
}

// 更新数据库
export function fetchUpdateDatabase(data?: Api.SystemManage.DatabaseUpdateParams) {
  return request<Api.SystemManage.DatabaseList, 'json'>({
    url: `/asset/databases/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除数据库
export function fetchDeleteDatabase(data?: Api.Common.CommonDeleteParams) {
  return request<Api.SystemManage.DatabaseList>({
    url: `/asset/databases/${data?.id}`,
    method: 'delete'
  });
}

// 测试数据库连接
export function fetchTestDatabase(data?: Api.SystemManage.DatabaseTestParams) {
  const params = new URLSearchParams();
  if (data?.id) {
    params.append('database_id', data?.id.toString());
  }
  return request<Api.SystemManage.DatabaseList>({
    url: `/asset/databases/test${params.toString() ? `?${params.toString()}` : ''}`,
    method: 'post',
    data
  });
}

// 获取数据域信息
export function fetchGetDataDomainList(params?: Api.SystemManage.DomainSearchParams) {
  return request<Api.SystemManage.DomainList>({
    url: '/asset/data-domain',
    method: 'get',
    params
  });
}

// 添加数据域信息
export function fetchAddDataDomain(data?: Api.SystemManage.DomainAddParams) {
  return request<Api.SystemManage.DomainList, 'json'>({
    url: '/asset/data-domain',
    method: 'post',
    data
  });
}

// 更新数据域信息
export function fetchUpdateDataDomain(data?: Api.SystemManage.DomainUpdateParams) {
  return request<Api.SystemManage.DomainList, 'json'>({
    url: `/asset/data-domain/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除数据域信息
export function fetchDeleteDataDomain(data?: Api.Common.CommonDeleteParams) {
  return request<Api.SystemManage.DomainList>({
    url: `/asset/data-domain/${data?.id}`,
    method: 'delete'
  });
}

// 获取主题域信息
export function fetchGetTopicDomainList(params?: Api.SystemManage.DomainSearchParams) {
  return request<Api.SystemManage.DomainList>({
    url: '/asset/topic-domain',
    method: 'get',
    params
  });
}

// 添加主题域信息
export function fetchAddTopicDomain(data?: Api.SystemManage.DomainAddParams) {
  return request<Api.SystemManage.DomainList, 'json'>({
    url: '/asset/topic-domain',
    method: 'post',
    data
  });
}

// 更新主题域信息
export function fetchUpdateTopicDomain(data?: Api.SystemManage.DomainUpdateParams) {
  return request<Api.SystemManage.DomainList, 'json'>({
    url: `/asset/topic-domain/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除主题域信息
export function fetchDeleteTopicDomain(data?: Api.Common.CommonDeleteParams) {
  return request<Api.SystemManage.DomainList>({
    url: `/asset/topic-domain/${data?.id}`,
    method: 'delete'
  });
}

// 获取主题数据模型
export function fetchDataModelList(params?: Api.SystemManage.DataModelSearchParams) {
  return request<Api.SystemManage.DataModelList>({
    url: '/asset/model',
    method: 'get',
    params
  });
}

// 添加主题数据模型
export function fetchAddDataModel(data?: Api.SystemManage.DataModelAddParams) {
  return request<Api.SystemManage.DataModelList, 'json'>({
    url: '/asset/model',
    method: 'post',
    data
  });
}

// 更新主题数据模型
export function fetchUpdateDataModel(data?: Api.SystemManage.DataModelUpdateParams) {
  return request<Api.SystemManage.DataModelList, 'json'>({
    url: `/asset/model/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除主题数据模型
export function fetchDeleteDataModel(data?: Api.Common.CommonDeleteParams) {
  return request<Api.SystemManage.DataModelList>({
    url: `/asset/model/${data?.id}`,
    method: 'delete'
  });
}

// 通过数据库、sql获取数据预览
export function fetchDataPreview(params?: Api.SystemManage.DataPreviewSearchParams) {
  return request<Api.SystemManage.DataPreviewList>({
    url: '/asset/model/data-preview',
    method: 'get',
    params
  });
}

// 获取数据表信息
export function fetchGetTableList(params?: Api.SystemManage.TableSearchParams) {
  return request<Api.SystemManage.TableList>({
    url: '/asset/model/tables',
    method: 'get',
    params
  });
}

// 获取数据表的字段信息
export function fetchTableColumns(params?: Api.SystemManage.TableColumnsSearchParams) {
  return request<Api.SystemManage.TableColumnsList>({
    url: '/asset/model/tables/columns',
    method: 'get',
    params
  });
}


// 获取标签列表
export function fetchTag(params?: Api.DataAsset.TagSearchParams) {
  return request<Api.DataAsset.TagList, 'json'>({
    url: `/asset/tag`,
    method: 'get',
    params
  });
}

// 创建标签
export function fetchAddTag(data?: Api.DataAsset.TagAddParams) {
  return request<Api.DataAsset.TagData, 'json'>({
    url: `/asset/tag`,
    method: 'post',
    data
  });
}

// 更新标签
export function fetchUpdateTag(data?: Api.DataAsset.TagUpdateParams) {
  return request<Api.DataAsset.TagData, 'json'>({
    url: `/asset/tag/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除标签
export function fetchDeleteTag(data?: Api.Common.CommonDeleteParams) {
  return request<Api.DataAsset.TagData, 'json'>({
    url: `/asset/tag/${data?.id}`,
    method: 'delete'
  });
}

// 创建指标标签
export function fetchAddMetricTag(data?: Api.DataAsset.MetricTagAddParams) {
  return request<Api.DataAsset.TagData, 'json'>({
    url: `/asset/metric-tag`,
    method: 'post',
    data
  });
}

// 删除指标标签
export function fetchDeleteMetricTag(params?: Api.DataAsset.MetricTagDeleteParams) {
  return request<Api.DataAsset.TagData, 'json'>({
    url: `/asset/metric-tag`,
    method: 'delete',
    params
  });
}
