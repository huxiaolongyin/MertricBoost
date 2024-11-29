<template>
    <NDataTable :columns="columns" :data="metricData?.data" size="small" :loading="isDataLoading" class="sm:h-full"
        :pagination="pagination" scroll-y="700" :max-height="320" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { DataTableColumns } from "naive-ui";
import { watch } from 'vue';

// 定义组件名
defineOptions({
    name: 'MetricDetail'
})

// 双向绑定数据
const metricData = defineModel<Api.Metric.MetricData>("metricData", { required: false })
const isDataLoading = defineModel<boolean>("isDataLoading", { required: true })
const metricSearchParams = defineModel<Api.Metric.MetricSearchParams>("searchParams", { required: true })

// 设置字段
const columns = ref<DataTableColumns>([
    {
        key: 'date',
        title: "日期",
        sorter: 'default',
        align: 'center',
    },
    {
        key: 'value',
        title: "数据",
        sorter: 'default',
        align: 'center',
    }
])

const pagination = ref({
    page: 1,
    pageSize: 10,
    showSizePicker: true,
    pageSizes: [10, 20, 30, 50],
    onChange: (page: number) => {
        pagination.value.page = page
        // handlePreview()
    },
    onUpdatePageSize: (pageSize: number) => {
        pagination.value.pageSize = pageSize
        pagination.value.page = 1
        // handlePreview()
    }
}
);

watch(() => metricSearchParams.value.dimensionDrillDown, async (newDimension) => {
    // 重置columns为基础列
    columns.value = [
        {
            key: 'date',
            title: "日期",
            sorter: 'default',
            align: 'center',
        },
        {
            key: 'value',
            title: "数据",
            sorter: 'default',
            align: 'center',
        }
    ]
    // 添加新的维度列
    if (newDimension) {
        columns.value.splice(1, 0, {
            key: newDimension,
            title: metricData.value?.dimensions.find(item => item.value === newDimension)?.label,
            sorter: 'default',
            align: 'center'
        })
    }
},
    { immediate: true })
</script>
