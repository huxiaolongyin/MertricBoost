import { request } from '../request';

export function fetchDecisionList(params?: Api.Decision.DecisionSearchParams) {
  return request<Api.Decision.DecisionList>({
    url: '/decisions',
    method: 'get',
    params
  });
}

export function fetchDecisionDetail(params: Api.Common.CommonIdParams) {
  return request<Api.Decision.DecisionDetail>({
    url: `/decisions/${params.id}`,
    method: 'get'
  });
}

export function fetchAddDecision(data: Api.Decision.DecisionAddParams) {
  return request<Api.Decision.DecisionList, 'json'>({
    url: '/decisions',
    method: 'post',
    data
  });
}

export function fetchUpdateDecision(data: Api.Decision.DecisionUpdateParams) {
  return request<Api.Decision.DecisionList, 'json'>({
    url: `/decisions/${data.id}`,
    method: 'patch',
    data
  });
}

export function fetchDeleteDecision(params: Api.Common.CommonDeleteParams) {
  return request<Api.Common.CommonDeleteParams>({
    url: `/decisions/${params.id}`,
    method: 'delete'
  });
}
