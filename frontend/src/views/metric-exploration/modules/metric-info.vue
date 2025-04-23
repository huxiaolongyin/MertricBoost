<script setup lang="ts">
import type { FormRules } from 'naive-ui';
import { NForm, NFormItem, NInput, NInputNumber, NSelect } from 'naive-ui';
import { markRaw, onMounted, ref, watch } from 'vue';
import { useLoadOptions } from '@/hooks/common/option';
import { $t } from '@/locales';
import { fetchDataModelList } from '@/service/api';
import { chartTypeOptions, sensitiveOptions, statisticalPeriodOptions } from '@/constants/options';
// 定义表单模型
const formModel = defineModel<Api.Metric.MetricUpdateParams>('metricData', {
  required: true
});

// 添加响应式状态跟踪是否禁用这些字段
const disableFields = ref(false);

// 加载非禁用的模型列表
const {
  options: dataModelOptions,
  // loading: dataModelLoading,
  fetchOptions: fetchDataModelOptions
} = useLoadOptions(() => fetchDataModelList({ status: '1' }), {
  labelKey: 'name',
  valueKey: 'id'
});

// Filter out the "不限" option
const filteredSensitiveOptions = sensitiveOptions.filter(option => !(option.value === '' && option.label === '不限'));
// 加载数据
// fetchDataModelOptions()

// 定义表单的字段
const formFields = ref<Api.Metric.MetricFormFields>({
  modelForm: [
    {
      key: 'dataModelId',
      label: '选用模型',
      component: markRaw(NSelect),
      props: {
        options: dataModelOptions,
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
        options: filteredSensitiveOptions
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
      props: {
        disabled: disableFields
      },
      placeholder: '请输入统计范围'
    }
  ],
  chartForm: [
    {
      key: 'chartType',
      label: '选用图表',
      component: markRaw(NSelect),
      props: {
        options: chartTypeOptions,
        disabled: disableFields
      },
      placeholder: '选择展示的图表'
    }
  ]
});

// 定义表单的校验规则
const rules: FormRules = {
  metricName: { required: true, message: '指标名称是必填项', trigger: 'blur' },
  metricDesc: { required: true, message: '指标描述是必填项', trigger: 'blur' },
  sensitivity: { required: true, message: '敏感等级是必填项', trigger: 'blur' },
  statisticalPeriod: { required: true, message: '统计周期是必填项', trigger: 'blur' },
  dataModelId: { required: true, message: '选用模型是必填项' }
};

onMounted(
  async () =>
    // 加载数据
    await fetchDataModelOptions()
);

// 监听统计周期的变化
watch(
  () => formModel.value.statisticalPeriod,
  newValue => {
    // 当统计周期为 'cumulative' 时禁用相关字段
    disableFields.value = newValue === 'cumulative';

    // 如果禁用了且已有值，可以选择是否清空这些值
    if (disableFields.value) {
      // 可选：清空选用图表值
      // formModel.value.chartType = null;
    }
  },
  { immediate: true }
);
</script>

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
