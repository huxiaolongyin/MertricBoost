// 用于获取表格数据
import { computed, reactive, ref } from 'vue';
import type { Ref } from 'vue';
import { jsonClone } from '@sa/utils';
import useBoolean from './use-boolean';
import useLoading from './use-loading';

export type MaybePromise<T> = T | Promise<T>;

export type ApiFn = (args: any) => Promise<unknown>;

export type TableColumnCheck = {
  key: string;
  title: string;
  checked: boolean;
};

export type TableDataWithIndex<T> = T & { index: number };

export type TransformedData<T> = {
  data: TableDataWithIndex<T>[];
  pageNum: number;
  pageSize: number;
  total: number;
};

export type Transformer<T, Response> = (response: Response) => TransformedData<T>;

// 这个类型定义了传递给 useHookTable 的配置项，包括 API 函数、参数、转换器、列定义等。
export type TableConfig<A extends ApiFn, T, C> = {
  apiFn: A; // API 函数
  apiParams?: Parameters<A>[0]; // API 参数
  transformer: Transformer<T, Awaited<ReturnType<A>>>; // 转换 API 响应为表格数据
  columns: () => C[]; // 列工厂函数
  getColumnChecks: (columns: C[]) => TableColumnCheck[]; // 获取列检查配置
  getColumns: (columns: C[], checks: TableColumnCheck[]) => C[]; // 获取过滤后的列
  onFetched?: (transformed: TransformedData<T>) => MaybePromise<void>; // 获取数据后的回调
  immediate?: boolean; // 是否立即获取数据
};

export default function useHookTable<A extends ApiFn, T, C>(config: TableConfig<A, T, C>) {
  const { loading, startLoading, endLoading } = useLoading();
  const { bool: empty, setBool: setEmpty } = useBoolean();
  const { apiFn, apiParams, transformer, immediate = true, getColumnChecks, getColumns } = config;
  const searchParams: NonNullable<Parameters<A>[0]> = reactive(jsonClone({ ...apiParams }));
  const allColumns = ref(config.columns()) as Ref<C[]>;
  const data: Ref<TableDataWithIndex<T>[]> = ref([]);
  const columnChecks: Ref<TableColumnCheck[]> = ref(getColumnChecks(config.columns()));
  const columns = computed(() => getColumns(allColumns.value, columnChecks.value));

  // Hook 初始化了加载状态、空状态，并从配置中解构出必要的属性
  function reloadColumns() {
    allColumns.value = config.columns();
    const checkMap = new Map(columnChecks.value.map(col => [col.key, col.checked]));
    const defaultChecks = getColumnChecks(allColumns.value);
    columnChecks.value = defaultChecks.map(col => ({
      ...col,
      checked: checkMap.get(col.key) ?? col.checked
    }));
  }

  // 负责调用 API 获取数据，并通过转换器处理响应数据
  async function getData() {
    startLoading();
    const formattedParams = formatSearchParams(searchParams);
    const response = await apiFn(formattedParams);
    const transformed = transformer(response as Awaited<ReturnType<A>>);
    data.value = transformed.data;
    setEmpty(transformed.data.length === 0);
    await config.onFetched?.(transformed);
    endLoading();
  }

  function formatSearchParams(params: Record<string, unknown>) {
    const formattedParams: Record<string, unknown> = {};
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        formattedParams[key] = value;
      }
    });

    return formattedParams;
  }

  // 更新搜索参数
  function updateSearchParams(params: Partial<Parameters<A>[0]>) {
    Object.assign(searchParams, params);
  }

  // 重置搜索参数
  function resetSearchParams() {
    Object.assign(searchParams, jsonClone(apiParams));
  }

  // 如果配置了立即获取数据，则立即调用 getData 获取数据
  if (immediate) {
    getData();
  }

  return {
    loading,
    empty,
    data,
    columns,
    columnChecks,
    reloadColumns,
    getData,
    searchParams,
    updateSearchParams,
    resetSearchParams
  };
}
