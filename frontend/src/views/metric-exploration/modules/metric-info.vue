<script setup lang="ts">
import type { FormRules, SelectOption } from 'naive-ui';
import { NForm, NFormItem, NInput, NInputNumber, NSelect } from 'naive-ui';
import { markRaw, onMounted, ref } from 'vue';
import { useLoadOptions } from '@/hooks/common/option';
import { $t } from '@/locales';
import { fetchDataModelList } from '@/service/api';

// 定义表单模型
const formModel = defineModel<Api.Metric.MetricUpdateParams>('metricData', {
  required: true
});

// 加载非禁用的模型列表
const {
  options: dataModelOptions,
  // loading: dataModelLoading,
  fetchOptions: fetchDataModelOptions
} = useLoadOptions(() => fetchDataModelList({ status: '1' }), {
  labelKey: 'name',
  valueKey: 'id'
});

// 加载数据
// fetchDataModelOptions()

const sensitivityOptions: SelectOption[] = [
  { label: '普通', value: '1' },
  { label: '重要', value: '2' },
  { label: '核心', value: '3' }
];
const statisticalPeriodOptions: SelectOption[] = [
  { label: '日', value: 'daily' },
  { label: '周', value: 'weekly' },
  { label: '月', value: 'monthly' },
  { label: '年', value: 'yearly' }
];
const chartTypeOptions: SelectOption[] = [
  { label: '折线图', value: 'line' },
  { label: '柱状图', value: 'bar' }
];

// 定义表单的字段
const formFields = ref<Api.Metric.MetricFormFields>({
  modelForm: [
    {
      key: 'dataModelId',
      label: '选用模型',
      component: markRaw(NSelect),
      props: {
        options: dataModelOptions,
        // computed(() => dataModelOptions.value.map(item => ({ label: item.name, value: item.id })))
        filterable: true
      },
      placeholder: '请选择模型'
    }
  ],
  metricForm: [
    {
      key: 'metricName',
      label: '指标名称',
      component: markRaw(NInput),
      placeholder: '请输入指标名称'
    },
    {
      key: 'metricDesc',
      label: '指标描述',
      component: markRaw(NInput),
      placeholder: '请输入指标描述'
    }
  ],
  sensitivityForm: [
    {
      key: 'sensitivity',
      label: '敏感等级',
      component: markRaw(NSelect),
      props: {
        options: sensitivityOptions
      },
      placeholder: '请选择敏感等级'
    }
  ],
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
      key: 'statisticScope',
      label: '统计范围',
      component: markRaw(NInputNumber),
      placeholder: '请输入统计范围'
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
    }
  ]
});

// 定义表单的校验规则
const rules: FormRules = {
  metricName: { required: true, message: '指标名称是必填项', trigger: 'blur' },
  metricDesc: { required: true, message: '指标描述是必填项', trigger: 'blur' },
  sensitivity: { required: true, message: '敏感度是必填项', trigger: 'blur' },
  dataModelId: { required: true, message: '选用模型是必填项' },
  statisticScope: { required: true, message: '统计范围是必填项', trigger: 'blur' }
};

onMounted(
  async () =>
    // 加载数据
    await fetchDataModelOptions()
);
</script>

<!-- ref="formRef" -->
<template>
  <div>
    <NForm :model="formModel" :rules="rules" label-width="80" class="" label-align="left">
      <div v-for="(form, key) in formFields" :key="key">
        <div class="mb-6 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.metric.formTile.${key}`) }}
        </div>
        <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16" class="">
          <NGi v-for="field in form" :key="field.key">
            <NFormItem :key="field.key" :label="field.label" :path="field.key">
              <component
                :is="field.component"
                v-model:value="formModel[field.key]"
                v-bind="field.props"
                :placeholder="field.placeholder"
                class="w-full"
              />
            </NFormItem>
          </NGi>
        </NGrid>
      </div>
    </NForm>
  </div>
</template>
