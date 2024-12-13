import { request } from '../request';

// api
export function fetchServiceApiList(params?: Api.DataService.ServiceApiSearchParams) {
  return request<Api.DataService.ServiceApiList>({
    url: '/service/apis',
    method: 'get',
    params
  });
}

export function fetchServiceApiDetail(params: Api.Common.CommonIdParams) {
  return request<Api.DataService.ServiceApiDetail>({
    url: `/service/apis/${params.id}`,
    method: 'get',
    params
  });
}

export function fetchAddServiceApi(data: Api.DataService.ServiceApiAddParams) {
  return request<Api.DataService.ServiceApiList, 'json'>({
    url: '/service/apis',
    method: 'post',
    data
  });
}

export function fetchUpdateServiceApi(data: Api.DataService.ServiceApiUpdateParams) {
  console.log(data);
  return request<Api.DataService.ServiceApiList, 'json'>({
    url: `/service/apis/${data.id}`,
    method: 'patch',
    data
  });
}

export function fetchDeleteServiceApi(params: Api.Common.CommonDeleteParams) {
  return request<Api.Common.CommonDeleteParams>({
    url: '/service/apis',
    method: 'delete',
    params
  });
}

export function fetchBatchDeleteServiceApi(data?: Api.Common.CommonBatchDeleteParams) {
  return request<Api.Common.CommonDeleteParams>({
    url: '/service/apis',
    method: 'delete',
    params: { ids: data?.ids.join(',') }
  });
}

// 应用
export function fetchServiceAppList(params?: Api.DataService.ServiceAppSearchParams) {
  return request<Api.DataService.ServiceAppList>({
    url: '/service/apps',
    method: 'get',
    params
  });
}

export function fetchServiceAppDetail(params: Api.Common.CommonIdParams) {
  return request<Api.DataService.ServiceAppDetail>({
    url: `/service/apps/${params.id}`,
    method: 'get'
  });
}

export function fetchAddServiceApp(data: Api.DataService.ServiceAppAddParams) {
  return request<Api.DataService.ServiceAppList, 'json'>({
    url: '/service/apps',
    method: 'post',
    data
  });
}

export function fetchUpdateServiceApp(data: Api.DataService.ServiceAppUpdateParams) {
  return request<Api.DataService.ServiceAppList, 'json'>({
    url: `/service/apps/${data.id}`,
    method: 'patch',
    data
  });
}

export function fetchDeleteServiceApp(params: Api.Common.CommonDeleteParams) {
  return request<Api.Common.CommonDeleteParams>({
    url: `/service/apps/${params.id}`,
    method: 'delete'
  });
}
