import type { SelectOption } from 'naive-ui';
import { ref } from 'vue';

// Type for the options configuration
interface OptionsConfig {
  labelKey: string;
  valueKey: string;
  disabledKey?: string;
}

// 通用加载选项hook
export function useLoadOptions<T extends Record<string, any>>(
  fetchFunction: (params?: any) => Promise<NaiveUI.FlatResponseData<T>>,
  config: OptionsConfig
) {
  const options = ref<SelectOption[]>([]);
  const loading = ref(false);
  const { labelKey, valueKey, disabledKey = labelKey } = config;

  // 可以在label上加上注释
  const parseLabelKey = (key: string, item: any) => {
    const match = key.match(/(\w+)\((\w+)\)/);
    if (match) {
      const [, mainKey, descKey] = match;
      return `${item[mainKey]}(${item[descKey]})`;
    }
    return item[key];
  };

  const fetchOptions = async () => {
    loading.value = true;
    try {
      const response = await fetchFunction();
      options.value = response.data?.records?.map((item: T) => ({
        label: parseLabelKey(labelKey, item),
        value: item[valueKey],
        disabled: disabledKey ? item[disabledKey] === '1' : false
      }));
    } catch (error) {
      // Replace console statement with proper error handling
      options.value = [];
      // Optionally add proper error handling mechanism
      // errorHandler.captureError('Failed to fetch options:', error);
      console.log('Failed to fetch options:', error);
    } finally {
      loading.value = false;
    }
  };

  return {
    options,
    loading,
    fetchOptions
  };
}
