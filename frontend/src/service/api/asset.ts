import Qs from 'qs';
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
    params.append('databaseId', data?.id.toString());
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
    url: '/asset/domains?domainType=1',
    method: 'get',
    params
  });
}

// 获取所有域信息
export function fetchGetDomainList(params?: Api.SystemManage.DomainSearchParams) {
  return request<Api.SystemManage.DomainList>({
    url: '/asset/domains',
    method: 'get',
    params
  });
}

// 获取主题域信息
export function fetchGetTopicDomainList(params?: Api.SystemManage.DomainSearchParams) {
  return request<Api.SystemManage.DomainList>({
    url: '/asset/domains?domainType=2',
    method: 'get',
    params
  });
}

// 添加数据域信息
export function fetchAddDataDomain(data?: Api.SystemManage.DomainAddParams) {
  return request<Api.SystemManage.DomainList, 'json'>({
    url: '/asset/domains',
    method: 'post',
    data: {
      ...data,
      domainType: '1'
    }
  });
}

// 添加主题域信息
export function fetchAddTopicDomain(data?: Api.SystemManage.DomainAddParams) {
  return request<Api.SystemManage.DomainList, 'json'>({
    url: '/asset/domains',
    method: 'post',
    data: {
      ...data,
      domainType: '2'
    }
  });
}

// 更新域信息
export function fetchUpdateDomain(data?: Api.SystemManage.DomainUpdateParams) {
  return request<Api.SystemManage.DomainList, 'json'>({
    url: `/asset/domains/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除域信息
export function fetchDeleteDomain(data?: Api.Common.CommonDeleteParams) {
  return request<Api.SystemManage.DomainList>({
    url: `/asset/domains/${data?.id}`,
    method: 'delete'
  });
}

// 获取域分类树
export function fetchGetDomainTree(params?: Api.SystemManage.DomainSearchParams) {
  return request<Api.SystemManage.DomainTree[]>({
    url: '/asset/domains/tree',
    method: 'get',
    params
  });
}
// 获取主题数据模型
export function fetchDataModelList(modelParams?: Api.SystemManage.DataModelSearchParams) {
  return request<Api.SystemManage.DataModelList>({
    url: '/asset/model',
    method: 'get',
    params: modelParams,
    paramsSerializer: {
      serialize: params => Qs.stringify(params, { arrayFormat: 'repeat' })
    }
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
    url: '/asset/model/preview',
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
export function fetchGetTagList(params?: Api.Asset.TagSearchParams) {
  return request<Api.Asset.TagList, 'json'>({
    url: `/asset/tag`,
    method: 'get',
    params
  });
}

// 创建标签
export function fetchAddTag(data?: Api.Asset.TagAddParams) {
  return request<Api.Asset.TagData, 'json'>({
    url: `/asset/tag`,
    method: 'post',
    data
  });
}

// 更新标签
export function fetchUpdateTag(data?: Api.Asset.TagUpdateParams) {
  return request<Api.Asset.TagData, 'json'>({
    url: `/asset/tag/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除标签
export function fetchDeleteTag(data?: Api.Common.CommonDeleteParams) {
  return request<Api.Asset.TagData, 'json'>({
    url: `/asset/tag/${data?.id}`,
    method: 'delete'
  });
}

// 创建指标标签关系
export function fetchAddMetricTag(data?: Api.Asset.MetricTagAddParams) {
  return request<Api.Asset.TagData, 'json'>({
    url: `/metric/tag`,
    method: 'post',
    data
  });
}

// 删除指标标签关系
export function fetchDeleteMetricTag(params?: Api.Asset.MetricTagDeleteParams) {
  return request<Api.Asset.TagData, 'json'>({
    url: `/metric/tag`,
    method: 'delete',
    params
  });
}
