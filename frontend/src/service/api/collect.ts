import Qs from 'qs';
import { request } from '../request';

// 获取数据采集任务列表
export function fetchCollectList(params?: Api.Collect.CollectSearchParams) {
  return request<Api.Collect.CollectList>({
    url: '/collect/list',
    method: 'get',
    params,
    paramsSerializer: {
      serialize: queryParams => Qs.stringify(queryParams, { arrayFormat: 'repeat' })
    }
  });
}

// 添加数据采集任务
export function fetchAddCollect(data?: Api.Collect.CollectAddParams) {
  return request<Api.Collect.CollectList, 'json'>({
    url: '/collect/create',
    method: 'post',
    data
  });
}

// 更新数据采集任务
export function fetchUpdateCollect(data?: Api.Collect.CollectUpdateParams) {
  return request<Api.Collect.CollectList, 'json'>({
    url: `/collect/${data?.id}`,
    method: 'post',
    data
  });
}

// 删除数据采集任务
export function fetchDeleteCollect(data?: Api.Common.CommonDeleteParams) {
  return request<Api.Collect.CollectList>({
    url: `/collect/${data?.id}`,
    method: 'delete'
  });
}

// 批量删除数据采集任务
export function fetchBatchDeleteCollect(ids: string) {
  return request<Api.Collect.CollectList>({
    url: `/collect/delete`,
    method: 'delete',
    params: { ids }
  });
}

// 切换数据采集任务状态
export function fetchToggleCollectStatus(id: number, status: string) {
  return request<Api.Collect.CollectList, 'json'>({
    url: `/collect/${id}/toggle`,
    method: 'post',
    params: { id, status }
  });
}

// // 执行离线同步任务
// export function fetchExecuteOfflineSync(id: number) {
//   return request<Api.Collect.CollectResult>({
//     url: `/asset/collects/${id}/execute`,
//     method: 'post'
//   });
// }

// // 配置实时同步任务
// export function fetchConfigureRealtimeSync(id: number, flumeConfig: any) {
//   return request<Api.Collect.CollectResult, 'json'>({
//     url: `/asset/collects/${id}/configure`,
//     method: 'post',
//     data: flumeConfig
//   });
// }

// // 获取所有采集任务状态
// export function fetchCollectStatus() {
//   return request<Api.Collect.CollectStatusResult>({
//     url: '/asset/collects/status',
//     method: 'get'
//   });
// }
