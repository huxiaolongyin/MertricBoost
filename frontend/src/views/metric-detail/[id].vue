<template>
  <div>
    <div v-if="operateType === 'edit'" class="flex justify-end space-x-2 mb-4">
      <NButton class="bg-red-500 text-white" @click="handleDelete">删除</NButton>
      <NButton class="bg-blue-500 text-white" @click="handleEdit">{{ isEditing ? '取消编辑' : '编辑' }}</NButton>
    </div>
    <NCard :bordered="true" class="bg-white dark:bg-slate-700">
      <NForm ref="form" :model="formModel" :rules="rules" label-width="80" class="" labelAlign="left"
        :disabled="!isEditing">
        <div v-for="(form, key)  in formFields">
          <div class=" text-dark dark:text-white font-sans text-lg font-semibold mb-6">{{
            $t(`page.metric.formTile.${key}`)
          }}
          </div>
          <NGrid cols="s:1 m:2 l:4" responsive="screen" :x-gap="16" :y-gap="16" class="">
            <NGi v-for="field in form">
              <NFormItem :key="field.key" :label="field.label" :path="field.key">
                <component :is="field.component" v-model:value="formModel[field.key]" v-bind="field.props"
                  :placeholder="field.placeholder" class="w-full" />
              </NFormItem>
            </NGi>
          </NGrid>
        </div>
        <NFormItem class="flex justify-center">
          <NButton v-if="isEditing" @click="handleSubmit" class="px-6" type="primary">提交</NButton>
        </NFormItem>
      </NForm>
    </NCard>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, markRaw } from 'vue';
import { NForm, NFormItem, NInput, NSelect, NButton, NInputNumber } from 'naive-ui';
import { $t } from '@/locales';
import { useMessage } from 'naive-ui'
import { useRoute } from 'vue-router';
import { fetchAddMetric, fetchUpdateMetric, fetchDataModelList } from '@/service/api'
import type { SelectOption, FormRules } from 'naive-ui';
import { useLoadOptions } from '@/hooks/common/option'
import { useAuthStore } from '@/store/modules/auth';

// 定义表单的一些选项
// const dataModelOptions = ref<SelectOption[]>([])

// 加载非禁用的模型列表
const {
  options: dataModelOptions,
  loading: dataModelLoading,
  fetchOptions: fetchDataModelOptions
} = useLoadOptions(
  () => fetchDataModelList({ status: "1" }),
  'dataModelName',
  'id')

fetchDataModelOptions()

const sensitivityOptions: SelectOption[] = [
  { label: '普通', value: '1' },
  { label: '低敏感', value: '2' },
  { label: '高敏感', value: '3' }
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
const chartDisplayDateOptions: SelectOption[] = [
  { label: '7日 ', value: 7 },
  { label: '15日', value: 15 },
  { label: '30日', value: 30 },
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

// 定义表单的初始值
// 获取用户的信息
const authStore = useAuthStore();
const formModel = ref<Api.Metric.MetricUpdateParams>({
  id: null,
  dataModel: null,
  businessScope: null,
  chineseName: null,
  englishName: null,
  alias: null,
  sensitivity: null,
  statisticalPeriod: null,
  chartType: null,
  chartDisplayDate: null,
  publishStatus: '2',
  createBy: authStore.userInfo.userName
});

// 设置表单默认不能编辑
const isEditing = ref(false)

// 获取路由
const route = useRoute();

// 获取传入的id
const id = route.params.id;

const operateType = ref<'add' | 'edit'>('add');

if (id === 'add') {
  operateType.value = 'add';
  isEditing.value = !isEditing.value
}
else {
  operateType.value = 'edit';
  const item = JSON.parse(route.query.item as string);
  formModel.value = item;
}

// 定义表单的校验规则
const rules: FormRules = {
  chineseName: { required: true, message: '中文名是必填项', trigger: 'blur' },
  englishName: { required: true, message: '英文名是必填项', trigger: 'blur' },
  alias: { required: false, message: '别名是必填项', trigger: 'blur' },
  sensitivity: { required: true, message: '敏感度是必填项', trigger: 'blur' },
  dataModel: { required: true, message: '选用模型是必填项' },
  businessScope: { required: true, message: '业务口径是必填项', trigger: 'blur' }
};

const message = useMessage()

const handleDelete = () => {
  message.info('删除成功')
}

// 处理编辑
const handleEdit = () => {
  isEditing.value = !isEditing.value
}

const handleSubmit = async () => {
  if (operateType.value === 'add') {

    const { error } = await fetchAddMetric(formModel.value);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (operateType.value === 'edit') {
    const { error } = await fetchUpdateMetric(formModel.value);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }
}

onMounted(async () => {
  // 加载模型的选项数据
  // await fetchDataModelOptions()
  // console.log(dataModelOptions.value)
}
)
</script>
