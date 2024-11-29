import { request } from '../request';

// 获取标签列表
export function fetchTag(params?: Api.Tag.TagSearchParams) {
    return request<Api.Tag.TagList, 'json'>({
        url: `/data-asset/tag`,
        method: 'get',
        params
    });
}

// 创建标签
export function fetchAddTag(data?: Api.Tag.TagAddParams) {
    return request<Api.Tag.TagData, 'json'>({
        url: `/data-asset/tag`,
        method: 'post',
        data
    });
}

// 更新标签
export function fetchUpdateTag(data?: Api.Tag.TagUpdateParams) {
    return request<Api.Tag.TagData, 'json'>({
        url: `/data-asset/tag/${data?.id}`,
        method: 'patch',
        data
    });
}

// 删除标签
export function fetchDeleteTag(data?: Api.SystemManage.CommonDeleteParams) {
    return request<Api.Tag.TagData, 'json'>({
        url: `/data-asset/tag/${data?.id}`,
        method: 'delete',
    })
}

// 创建指标标签
export function fetchAddMetricTag(data?: Api.Tag.MetricTagAddParams) {
    return request<Api.Tag.TagData, 'json'>({
        url: `/data-asset/metric-tag`,
        method: 'post',
        data
    });
}

// 删除指标标签
export function fetchDeleteMetricTag(params?: Api.Tag.MetricTagDeleteParams) {
    return request<Api.Tag.TagData, 'json'>({
        url: `/data-asset/metric-tag`,
        method: 'delete',
        params
    })
}