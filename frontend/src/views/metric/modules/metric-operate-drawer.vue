<script setup lang="ts">
import { NForm, NFormItem, NInput, NInputNumber, NSelect } from 'naive-ui';
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useLoadOptions } from '@/hooks/common/option';
import { $t } from '@/locales';
import { fetchAddMetric, fetchDataModelList, fetchUpdateMetric } from '@/service/api';
import { chartTypeOptions, filteredSensitiveOptions, statisticalPeriodOptions } from '@/constants/options';

defineOptions({
  name: 'MetricOperateDrawer'
});

// 从父组件传入操作类型和行数据
interface Props {
  operateType: NaiveUI.TableOperateType;
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
  };
};
const model = reactive<Api.Metric.MetricUpdateParams>({});

// 加载非禁用的模型列表
const {
  options: dataModelOptions,
  // loading: dataModelLoading,
  fetchOptions: fetchDataModelOptions
} = useLoadOptions(() => fetchDataModelList({ status: '1' }), {
  labelKey: 'name',
  valueKey: 'id'
});

// 加载禁用
const disableFields = ref(false);

// 定义表单的校验规则
const rules = computed(() => {
  return {
    dataModelId: {
      required: true,
      validator: (value: any) => {
        return value !== null && value !== undefined;
      },
      message: '选用模型是必填项',
      trigger: ['blur', 'change']
    },
    metricName: { required: true, message: '指标名称是必填项', trigger: ['blur'] },
    metricDesc: { required: true, message: '指标描述是必填项', trigger: 'blur' },
    sensitivity: { required: true, message: '敏感等级是必填项', trigger: 'blur' },
    statisticalPeriod: { required: true, message: '统计周期是必填项', trigger: 'blur' },
    statisticScope: {
      required: !disableFields.value,
      validator: (value: any) => {
        return value !== null && value !== undefined;
      },
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

onMounted(async () => {
  await fetchDataModelOptions();
});

watch(
  () => visible.value,
  newVal => {
    if (newVal) {
      handleInitModel();
    }
  },
  { immediate: true }
);

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
      <NForm :model="model" :rules="rules" label-width="80" label-align="left">
        <div class="mb-6 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.metric.formTile.modelForm`) }}
        </div>
        <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16" class="">
          <NGi key="dataModelId">
            <NFormItem label="选用模型" path="dataModelId">
              <NSelect
                v-model:value="model.dataModelId"
                placeholder="选用模型"
                :options="dataModelOptions"
                filterable
              />
            </NFormItem>
          </NGi>
        </NGrid>
        <div class="mb-6 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.metric.formTile.metricForm`) }}
        </div>
        <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16" class="">
          <NGi key="metricName">
            <NFormItem label="指标名称" path="metricName">
              <NInput v-model:value="model.metricName" placeholder="请输入指标名称" />
            </NFormItem>
          </NGi>
          <NGi key="metricDesc">
            <NFormItem label="指标描述" path="metricDesc">
              <NInput v-model:value="model.metricDesc" placeholder="请输入指标描述" />
            </NFormItem>
          </NGi>
        </NGrid>
        <div class="mb-6 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.metric.formTile.sensitivityForm`) }}
        </div>

        <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16">
          <NGi key="sensitivity">
            <NFormItem label="敏感等级" path="sensitivity">
              <NSelect
                v-model:value="model.sensitivity"
                placeholder="请选择敏感等级"
                :options="filteredSensitiveOptions"
              />
            </NFormItem>
          </NGi>
        </NGrid>

        <div class="mb-6 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.metric.formTile.staticForm`) }}
        </div>
        <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16">
          <NGi key="statisticalPeriod">
            <NFormItem label="统计周期" path="statisticalPeriod">
              <NSelect
                v-model:value="model.statisticalPeriod"
                placeholder="统计周期"
                :options="statisticalPeriodOptions"
              />
            </NFormItem>
          </NGi>
          <NGi key="statisticScope">
            <NFormItem label="统计范围" path="statisticScope">
              <NInputNumber v-model:value="model.statisticScope" placeholder="统计范围" />
            </NFormItem>
          </NGi>
        </NGrid>

        <div class="mb-6 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.metric.formTile.chartForm`) }}
        </div>
        <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16">
          <NGi key="chartType">
            <NFormItem label="图表类型" path="chartType">
              <NSelect v-model:value="model.chartType" placeholder="图表类型" :options="chartTypeOptions" />
            </NFormItem>
          </NGi>
        </NGrid>
      </NForm>
    </NDrawerContent>
  </NDrawer>
</template>
