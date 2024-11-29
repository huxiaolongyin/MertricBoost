<template>
    <div>
        <NForm ref="form" :model="formModel" :rules="rules" label-width="80" class="" labelAlign="left">
            <div v-for="(form, key)  in formFields">
                <div class=" text-dark dark:text-white font-sans text-lg font-semibold mb-6">{{
                    $t(`page.metric.formTile.${key}`)
                    }}
                </div>
                <NGrid cols="s:1 m:2 l:3" responsive="screen" :x-gap="16" :y-gap="16" class="">
                    <NGi v-for="field in form">
                        <NFormItem :key="field.key" :label="field.label" :path="field.key">
                            <component :is="field.component" v-model:value="formModel[field.key]" v-bind="field.props"
                                :placeholder="field.placeholder" class="w-full" />
                        </NFormItem>
                    </NGi>
                </NGrid>
            </div>

        </NForm>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, markRaw, onMounted } from 'vue';
import { NForm, NFormItem, NInput, NSelect, NInputNumber } from 'naive-ui';
import { $t } from '@/locales';
import { fetchDataModelList } from '@/service/api'
import type { SelectOption, FormRules } from 'naive-ui';
import { useLoadOptions } from '@/hooks/common/option'


// 定义表单模型
const formModel = defineModel<Api.Metric.MetricUpdateParams>("metricData", { required: true })

// 加载非禁用的模型列表
const {
    options: dataModelOptions,
    loading: dataModelLoading,
    fetchOptions: fetchDataModelOptions
} = useLoadOptions(
    () => fetchDataModelList({ status: "1" }),
    'dataModelName',
    'id')

// 加载数据
// fetchDataModelOptions()

const sensitivityOptions: SelectOption[] = [
    { label: '普通', value: '1' },
    { label: '重要', value: '2' },
    { label: '核心', value: '3' }
]
const statisticalPeriodOptions: SelectOption[] = [
    { label: '日', value: 'day' },
    { label: '周', value: 'week' },
    { label: '月', value: 'month' },
    // { label: '季度', value: 'quarter' },
    { label: '年', value: 'year' }
]
const chartTypeOptions: SelectOption[] = [
    { label: '折线图', value: 'line' },
    { label: '柱状图', value: 'bar' },
]

// 定义表单的字段
const formFields = ref<Api.Metric.MetricFormFields>({
    modelForm: [
        {
            key: 'dataModel',
            label: '选用模型',
            component: markRaw(NSelect),
            props: {
                options: computed(() => dataModelOptions.value)
            },
            placeholder: '请选择模型'
        },
        {
            key: 'businessScope',
            label: '业务口径',
            component: markRaw(NInput),
            placeholder: '用于描述流程, 统一业务口径'
        }
    ],
    metricForm: [
        {
            key: 'chineseName',
            label: '中文名',
            component: markRaw(NInput),
            placeholder: '指标的中文名'
        },
        {
            key: 'englishName',
            label: '英文名',
            component: markRaw(NInput),
            placeholder: '指标的英文名'
        },
        {
            key: 'alias',
            label: '别名',
            component: markRaw(NInput),
            placeholder: '指标的别名'
        },
    ],
    sensitivityForm: [
        {
            key: 'sensitivity',
            label: '敏感度',
            component: markRaw(NSelect),
            props: {
                options: sensitivityOptions
            },
            placeholder: '请选择敏感度'
        }],
    staticForm: [
        {
            key: 'statisticalPeriod',
            label: '统计周期',
            component: markRaw(NSelect),
            props: {
                options: statisticalPeriodOptions
            },
            placeholder: '选择需要统计周期'
        },
        {
            key: 'chartDisplayDate',
            label: '展示周期',
            component: markRaw(NInputNumber),
            placeholder: '选择需要展示的周期'
        }
    ],
    chartForm: [
        {
            key: 'chartType',
            label: '选用图表',
            component: markRaw(NSelect),
            props: {
                options: chartTypeOptions
            },
            placeholder: '选择展示的图表'
        },

    ],
    publishForm: [
        {
            key: 'publishStatus',
            label: '发布状态',
            component: markRaw(NSelect),
            props: {
                options: [
                    { label: '已发布', value: '1' },
                    { label: '未发布', value: '2' }
                ]
            },
            placeholder: '选择发布状态'
        }
    ]
})

// 定义表单的校验规则
const rules: FormRules = {
    chineseName: { required: true, message: '中文名是必填项', trigger: 'blur' },
    englishName: { required: true, message: '英文名是必填项', trigger: 'blur' },
    alias: { required: false, message: '别名是必填项', trigger: 'blur' },
    sensitivity: { required: true, message: '敏感度是必填项', trigger: 'blur' },
    dataModel: { required: true, message: '选用模型是必填项' },
    businessScope: { required: true, message: '业务口径是必填项', trigger: 'blur' }
};

onMounted(async () =>
    // 加载数据 
    await fetchDataModelOptions()
)
</script>