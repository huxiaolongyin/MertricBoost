<script setup lang="ts">
import { NForm, NFormItem, NInput, NInputNumber, NSelect } from 'naive-ui';
import { computed, markRaw, onMounted, reactive, ref, watch } from 'vue';
import { useLoadOptions } from '@/hooks/common/option';
import { $t } from '@/locales';
import { fetchAddMetric, fetchDataModelList, fetchUpdateMetric } from '@/service/api';
import { chartTypeOptions, sensitiveOptions, statisticalPeriodOptions } from '@/constants/options';

defineOptions({
  name: 'MetricOperateDrawer'
});

// 从父组件传入数据
interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.Metric.MetricUpdateParams | null;
}

const props = defineProps<Props>();

// 定义上传
interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();

// 定义抽屉是否显示
const visible = defineModel<boolean>('visible', {
  default: false
});

// 定义抽屉标题
const drawerTitle = computed(() => {
  return props.operateType === 'add' ? '新增指标' : '编辑指标';
});

// 定义新增指标表单
const createDefaultModel = (): Api.Metric.MetricUpdateParams => {
  return {
    id: null,
    metricName: '',
    metricDesc: '',
    dataModelId: null,
    statisticalPeriod: null,
    statisticScope: null,
    chartType: null,
    sensitivity: null
    // domainIds: [],
  };
};
const model = reactive<Api.Metric.MetricUpdateParams>(createDefaultModel());

// 加载非禁用的模型列表
const {
  options: dataModelOptions,
  // loading: dataModelLoading,
  fetchOptions: fetchDataModelOptions
} = useLoadOptions(() => fetchDataModelList({ status: '1' }), {
  labelKey: 'name',
  valueKey: 'id'
});
// 加载过滤掉不限选项
const filteredSensitiveOptions = sensitiveOptions.filter(option => !(option.value === '' && option.label === '不限'));

// 加载禁用
const disableFields = ref(false);

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
const rules = computed(() => {
  return {
    metricName: { required: true, message: '指标名称是必填项', trigger: 'blur' },
    metricDesc: { required: true, message: '指标描述是必填项', trigger: 'blur' },
    sensitivity: { required: true, message: '敏感等级是必填项', trigger: 'blur' },
    statisticalPeriod: { required: true, message: '统计周期是必填项', trigger: 'blur' },
    dataModelId: { required: true, message: '选用模型是必填项', trigger: 'blur' },
    statisticScope: {
      required: !disableFields.value,
      message: '统计范围是必填项',
      trigger: 'blur'
    },
    chartType: {
      required: !disableFields.value,
      message: '选用图表是必填项',
      trigger: 'blur'
    }
  };
});

function handleInitModel() {
  Object.assign(model, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    Object.assign(model, props.rowData);
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  //   await validate();
  // request
  if (props.operateType === 'add') {
    const { error } = await fetchAddMetric(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateMetric(model);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
}

onMounted(
  async () =>
    // 加载数据
    await fetchDataModelOptions()
);
watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    // restoreValidation();
  }
});

watch(
  () => model.statisticalPeriod,
  newVal => {
    // Set disableFields to true when statisticalPeriod is 'cumulative'
    if ((disableFields.value = newVal === 'cumulative')) {
      disableFields.value = true;
      model.statisticScope = null;
      model.chartType = null;
    } else {
      disableFields.value = false;
    }
  }
);
</script>

<template>
  <NDrawer v-model:show="visible" :width="800">
    <NDrawerContent>
      <template #header>{{ drawerTitle }}</template>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
          <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
        </NSpace>
      </template>
      <NForm :model="model" :rules="rules" label-width="80" class="" label-align="left">
        <div v-for="(form, key) in formFields" :key="key">
          <div class="mb-6 text-lg text-dark font-semibold font-sans dark:text-white">
            {{ $t(`page.metric.formTile.${key}`) }}
          </div>
          <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16" class="">
            <NGi v-for="field in form" :key="field.key">
              <NFormItem :key="field.key" :label="field.label" :path="field.key">
                <component
                  :is="field.component"
                  v-model:value="model[field.key]"
                  v-bind="field.props"
                  :placeholder="field.placeholder"
                  class="w-full"
                />
              </NFormItem>
            </NGi>
          </NGrid>
        </div>
      </NForm>
    </NDrawerContent>
  </NDrawer>
</template>
