<template>
    <div class="px-6 mt-2">
        <NCard class="bg-white dark:bg-slate-700 rounded-xl">
            <NForm class="mt-3">
                <NFlex>
                    <NFormItem label="日期区间：" label-placement="left" class="w-3/12">
                        <NDatePicker v-model:value="formData.dateRange" type="daterange" clearable />
                    </NFormItem>
                    <NFormItem label="统计周期：" label-placement="left" class="w-2/12 ml-5">
                        <NSelect v-model:value="formData.statisticalPeriod" :options="StatisticalPeriodOptions"
                            clearable />
                    </NFormItem>
                </NFlex>
                <NFormItem label="维度下钻：" label-placement="left" class="w-full">
                    <NSelect class="w-3/12" v-model:value="formData.dimensionDrillDown"
                        :options="metricData?.dimensions" clearable />
                    <NSelect class="w-1/12 ml-2" v-model:value="formData.sort" :options="sortOptions"
                        placeholder="排名升降序" clearable />
                    <div class="w-full ml-5 text-orange-600">（图表最多显示排名前30行数据）</div>
                </NFormItem>
                <NFormItem label="维度筛选：" label-placement="left">
                    <NFlex :size="5" class="w-full">
                        <NSelect v-model:value="formData.dimensionFilter" class="w-2/12" clearable
                            @update:value="handleUpdate" :options="metricData?.dimensions" />
                        <NSelect v-model:value="formData.comparisonOperators" class="w-1/12" clearable
                            :options="FilterOptions" />
                        <NSelect v-model:value="formData.conditions" class="w-2/12" filterable clearable
                            :multiple="formData.comparisonOperators === 'in' || formData.comparisonOperators === 'not in'"
                            :options="conditionOptions" />
                        <!-- <NButton @click="handleAddGroup">
                            <Icon icon="material-symbols:add" />
                        </NButton> -->
                        <NButton class="bg-sky-700 text-white" @click="handleClick">
                            <Icon icon="material-symbols:search" class="mr-2" />查询
                        </NButton>
                    </NFlex>
                </NFormItem>
            </NForm>
        </NCard>
    </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { SelectOption } from 'naive-ui';
import { watch, ref } from 'vue';

// 定义组件的名称
defineOptions({
    name: 'MetricFilter'
})

// 双向绑定数据
const metricData = defineModel<Api.Metric.MetricData>("metricData", { required: true })
const formData = defineModel<Api.Metric.MetricSearchParams>("searchParams", { required: true })

// 添加维度筛选options
const FilterOptions: SelectOption[] = ([
    { label: "=", value: "=" },
    { label: "!=", value: "!=" },
    { label: "IN", value: "in" },
    { label: "NOT IN", value: "not in" }
]
)

// 添加统计周期筛选options
const StatisticalPeriodOptions: SelectOption[] = ([
    { label: "日", value: "day" },
    { label: "周", value: "week" },
    // { label: "季度", value: "quarter" },
    { label: "月", value: "month" },
    { label: "年", value: "year" }]
)

// 升序或者降序
const sortOptions: SelectOption[] = ([
    { label: "升序", value: "asc" },
    { label: "降序", value: "desc" },
])


// 添加维度筛选框
const conditionOptions = ref<SelectOption[]>([])

// 设置上传提交事件
const emit = defineEmits<{ (e: "submit"): void, (e: "update"): void }>();

const handleClick = () => {
    emit("submit");
}

const handleUpdate = () => {
    emit("update");
}

// 增加维度选项组，todo
const handleAddGroup = () => {

}

watch(() => formData.value.dimensionFilter, () => {
    // 如果维度筛选框有值，则设置条件选项，没有值，则清空条件选项
    if (formData.value.dimensionFilter) {
        conditionOptions.value = metricData.value?.dimensions.filter(item => item.value === formData.value.dimensionFilter)[0].options
    }
    else {
        conditionOptions.value = []
        formData.value.conditions = null
    }
})
</script>