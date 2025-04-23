import Qs from 'qs';
import { request } from '../request';

// 获取指标列表
export function fetchGetMetricList(metricParams?: Api.Metric.MetricListSearchParams) {
  return request<Api.Metric.MetricList, 'json'>({
    url: `/metric/list`,
    method: 'get',
    params: metricParams,
    paramsSerializer: {
      serialize: params => Qs.stringify(params, { arrayFormat: 'repeat' })
    }
  });
}

// 获取指标详情
export function fetchGetMetricDetail(data?: Api.Metric.MetricDetailSearchParams) {
  // 从params中提取id，其余参数将放入body
  const id = data?.id;
  // 创建一个新对象，排除id字段
  const { id: _, ...bodyParams } = data || {};

  return request<Api.Metric.MetricDetail, 'json'>({
    url: `/metric/${id}`,
    method: 'post',
    data: bodyParams // 使用data而不是params发送请求体
  });
}

// 添加指标
export function fetchAddMetric(data?: Api.Metric.MetricAddParams) {
  console.log(data);
  return request<Api.Metric.MetricData, 'json'>({
    url: '/metric/create',
    method: 'post',
    data
  });
}

// 更新指标
export function fetchUpdateMetric(data?: Api.Metric.MetricUpdateParams) {
  return request<Api.Metric.MetricData, 'json'>({
    url: `/metric/${data?.id}`,
    method: 'patch',
    data
  });
}

// 删除指标
export function fetchDeleteMetric(data?: Api.Common.CommonDeleteParams) {
  return request<Api.Metric.MetricData, 'json'>({
    url: `/metric/${data?.id}`,
    method: 'delete',
    data
  });
}
