<script setup lang="tsx">
import { computed, ref, watch } from 'vue';
import { Icon } from '@iconify/vue';
import { NButton, NPopconfirm } from 'naive-ui';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import {
  fetchAddServiceApi,
  fetchDeleteServiceApi,
  fetchServiceApiDetail,
  fetchServiceAppList,
  fetchUpdateServiceApi
} from '@/service/api';

import ServiceApiParamAdd from './service-api-param-add.vue';

defineOptions({
  name: 'ServiceApiOperateDrawer'
});

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.DataService.ServiceApi | null;
}

const props = defineProps<Props>();

interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
  default: false
});

const modalVisible = ref<boolean>(false);

const paramId = ref<number>();

const paramOperatype = ref<NaiveUI.TableOperateType>('add');

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.service.serviceApi.addApi'),
    edit: $t('page.service.serviceApi.editApi')
  };
  return titles[props.operateType];
});

const createDefaultModel = (): Api.DataService.ServiceApiUpdateParams => ({
  metricName: '',
  apiName: '',
  apiDesc: '',
  apiPath: '',
  status: '1',
  appName: null,
  apiMethod: 'get' as Api.DataService.Method,
  params: [] as Api.DataService.ServiceApiParams[]
});

const model = ref<Api.DataService.ServiceApiUpdateParams>(createDefaultModel());

type RuleKey = Extract<keyof Api.DataService.ServiceApiUpdateParams, 'apiName' | 'apiPath' | 'apiDesc' | 'appName'>;

const rules = ref<Record<RuleKey, App.Global.FormRule>>({
  apiName: defaultRequiredRule,
  apiPath: defaultRequiredRule,
  apiDesc: defaultRequiredRule,
  appName: defaultRequiredRule
});

/** the enabled role options */
const appOptions = ref<CommonType.Option<string>[]>([]);

const handleEdit = (row: any) => {
  paramOperatype.value = 'edit';
  modalVisible.value = true;
  paramId.value = row.id;
};
const handleDelete = (row: any) => {
  fetchDeleteServiceApi({ id: row.id });
};

const columns = [
  {
    key: 'paramName',
    title: '参数名称',
    minWidth: 80
  },
  {
    key: 'paramLoc',
    title: '参数位置',
    minWidth: 100
  },
  {
    key: 'paramType',
    title: '参数类型',
    minWidth: 100
  },
  {
    key: 'isRequired',
    title: '是否必填',
    width: 100,
    render: (row: any) => {
      return <div>{row.isRequired ? '是' : '否'}</div>;
    }
  },
  {
    key: 'example',
    title: '示例值',
    minWidth: 120
  },
  {
    key: 'paramDesc',
    title: '描述',
    minWidth: 120
  },
  {
    key: 'operate',
    title: '操作',
    width: 130,
    render: (row: any) => (
      <div class="flex-center gap-8px">
        <NButton type="primary" ghost size="small" onClick={() => handleEdit(row)}>
          {$t('common.edit')}
        </NButton>
        <NPopconfirm onPositiveClick={() => handleDelete(row)}>
          {{
            default: () => $t('common.confirmDelete'),
            trigger: () => (
              <NButton type="error" ghost size="small">
                {$t('common.delete')}
              </NButton>
            )
          }}
        </NPopconfirm>
      </div>
    )
  }
];

const getAppOptions = async () => {
  const { error, data } = await fetchServiceAppList({
    page: 1,
    pageSize: 9999,
    status: '1'
  });

  if (!error) {
    const options = data.records.map(item => ({
      label: item.appName,
      value: item.appName
    }));
    appOptions.value = options;
  }
};

const handleInitModel = async () => {
  Object.assign(model.value, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    const response = await fetchServiceApiDetail({ id: props.rowData.id });
    Object.assign(model.value, response.data?.records);
  }
};

const handleMethodChange = () => {};

const handleParamAdd = () => {
  modalVisible.value = true;
};

const closeDrawer = () => {
  visible.value = false;
};

const handleSubmit = async () => {
  await validate();
  // request

  if (props.operateType === 'add') {
    const { error } = await fetchAddServiceApi(model.value);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateServiceApi(model.value);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
};

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
    getAppOptions();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" display-directive="show" :width="1000">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules">
        <NFlex align="center" class="mb-5">
          <Icon icon="mdi:numeric-1-circle" width="36" height="36" class="text-blue-700" />
          <div class="text-xl font-semibold">
            {{ $t('page.service.serviceApi.form.baseInfo') }}
          </div>
        </NFlex>
        <NFormItem
          :label="$t('page.service.serviceApi.metricName')"
          label-placement="left"
          :label-width="80"
          path="metricName"
        >
          <NInput v-model:value="model.metricName" disabled />
        </NFormItem>
        <NFormItem
          :label="$t('page.service.serviceApi.apiName')"
          label-placement="left"
          :label-width="80"
          path="apiName"
        >
          <NInput v-model:value="model.apiName" :placeholder="$t('page.service.serviceApi.form.apiName')" />
        </NFormItem>
        <NFormItem
          :label="$t('page.service.serviceApi.apiPath')"
          label-placement="left"
          :label-width="80"
          path="apiPath"
        >
          <NInput v-model:value="model.apiPath" :placeholder="$t('page.service.serviceApi.form.apiPath')" />
        </NFormItem>
        <NFormItem
          :label="$t('page.service.serviceApi.apiDesc')"
          label-placement="left"
          :label-width="80"
          path="apiDesc"
        >
          <NInput
            v-model:value="model.apiDesc"
            :placeholder="$t('page.service.serviceApi.form.apiDesc')"
            type="textarea"
          />
        </NFormItem>
        <NFormItem :label="$t('page.service.serviceApi.apiMethod')" label-placement="left" :label-width="80">
          <NRadioGroup v-model:value="model.apiMethod" @update:value="handleMethodChange">
            <NRadio key="get" value="get">GET</NRadio>
            <NRadio key="post" value="post">POST</NRadio>
          </NRadioGroup>
        </NFormItem>
        <NFormItem
          :label="$t('page.service.serviceApi.appName')"
          label-placement="left"
          :label-width="80"
          path="appName"
        >
          <NSelect v-model:value="model.appName" :options="appOptions" />
        </NFormItem>
        <NFormItem :label="$t('page.service.serviceApi.status')" label-placement="left" :label-width="80">
          <NSwitch v-model:value="model.status" checked-value="1" unchecked-value="2" />
        </NFormItem>
      </NForm>
      <NFlex align="center" class="mb-5">
        <Icon icon="mdi:numeric-2-circle" width="36" height="36" class="text-blue-700" />
        <div class="text-xl font-semibold">
          {{ $t('page.service.serviceApi.form.paramSetting') }}
        </div>
      </NFlex>
      <NButton type="info" class="mb-5 w-20" @click="handleParamAdd">{{ $t('common.append') }}</NButton>
      <NDataTable :columns="columns" :data="model.params" />
      <ServiceApiParamAdd
        v-model:modal-visible="modalVisible"
        v-model:param-list="model.params"
        :operate-type="paramOperatype"
        :method="model.apiMethod ?? 'get'"
        :param-id="paramId"
        @submitted="handleParamAdd"
      />
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
          <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
