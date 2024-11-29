import { request } from '../request';

// 获取指标列表
export function fetchMetric(data?: Api.Metric.MetricSearchParams) {
    return request<Api.Metric.MetricList, 'json'>({
        url: `/metric/detail/${data?.id ?? ''}`,
        method: 'post',
        data
    });
}

// 添加指标
export function fetchAddMetric(data?: Api.Metric.MetricAddParams) {
    return request<Api.Metric.MetricData, 'json'>({
        url: '/metric/',
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
export function fetchDeleteMetric(data?: Api.SystemManage.CommonDeleteParams) {
    return request<Api.Metric.MetricData, 'json'>({
        url: `/metric/${data?.id}`,
        method: 'delete',
        data
    });
}
