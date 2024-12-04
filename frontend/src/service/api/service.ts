import { request } from '../request';

// api
export function fetchServiceApiList(params?: Api.DataService.ServiceApiSearchParams) {
  return request<Api.DataService.ServiceApiList>({
    url: '/service/api',
    method: 'get',
    params
  });
}

export function fetchServiceApiDetail(params: Api.Common.CommonIdParams) {
  return request<Api.DataService.ServiceApiDetail>({
    url: `/service/api/${params.id}`,
    method: 'get',
    params
  });
}

export function fetchAddServiceApi(data: Api.DataService.ServiceApiAddParams) {
  return request<Api.DataService.ServiceApiList, 'json'>({
    url: '/service/api',
    method: 'post',
    data
  });
}

export function fetchUpdateServiceApi(data: Api.DataService.ServiceApiUpdateParams) {
  return request<Api.DataService.ServiceApiList, 'json'>({
    url: '/service/api',
    method: 'patch',
    data
  });
}

export function fetchDeleteServiceApi(params: Api.Common.CommonDeleteParams) {
  return request<Api.Common.CommonDeleteParams>({
    url: '/service/api',
    method: 'delete',
    params
  });
}

// 应用
export function fetchServiceAppList(params?: Api.DataService.ServiceAppSearchParams) {
  return request<Api.DataService.ServiceAppList>({
    url: '/service/app',
    method: 'get',
    params
  });
}
