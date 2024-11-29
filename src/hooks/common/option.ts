import { ref } from 'vue'
import type { SelectOption } from 'naive-ui';
// // 通用类型定义
// export interface SelectOption {
//     label: string;
//     value: string | number;
// }


// 通用加载选项hook
export function useLoadOptions<T extends Record<string, any>>(
    fetchFunction: (params?: any) => Promise<NaiveUI.FlatResponseData<T>>,
    labelKey: string,
    valueKey: string
) {
    const options = ref<SelectOption[]>([])
    const loading = ref(false)

    // 可以在label上加上注释
    const parseLabelKey = (key: string, item: any) => {
        const match = key.match(/(\w+)\((\w+)\)/)
        if (match) {
            const [, mainKey, descKey] = match
            return `${item[mainKey]}(${item[descKey]})`
        }
        return item[key]
    }
    const fetchOptions = async () => {
        loading.value = true
        try {
            const response = await fetchFunction()
            options.value = response.data?.records?.map((item: T) => ({
                label: parseLabelKey(labelKey, item),
                value: item[valueKey]
            }))
        } catch (error) {
            console.error('Failed to fetch options:', error)
            options.value = []
        } finally {
            loading.value = false
        }
    }

    return {
        options,
        loading,
        fetchOptions
    }
}