import { request } from '../request';

/** 获得固定的路由 */
export function fetchGetConstantRoutes() {
  return request<Api.Route.MenuRoute[]>({ url: '/route/getConstantRoutes' });
}

/** 获取用户路由 */
export function fetchGetUserRoutes() {
  return request<Api.Route.UserRoute>({ url: '/route/getUserRoutes' });
}

/**
 * 确认路由是否存在
 *
 * @param routeName 路线名称
 */
export function fetchIsRouteExist(routeName: string) {
  return request<boolean>({ url: '/route/isRouteExist', params: { routeName } });
}
