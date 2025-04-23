<script setup lang="tsx">
import { computed, ref, watch } from 'vue';
import { NButton } from 'naive-ui';
import { nanoid } from 'nanoid';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { useAuthStore } from '@/store/modules/auth';
import { fetchAddServiceApp, fetchServiceAppDetail, fetchUpdateServiceApp } from '@/service/api';
import { enableStatusOptions } from '@/constants/business';

const authStore = useAuthStore();
// 定义传参
interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.DataService.ServiceApi | null;
}
const props = defineProps<Props>();

// 上传事件
interface Emits {
  (e: 'submitted'): void;
}
const emit = defineEmits<Emits>();

// 双向模型绑定父子组件的数据
const visible = defineModel<boolean>('visible', {
  default: false
});

// 定义表单模型
// 初始化模型
const createDefaultModel = (): Api.DataService.ServiceAppUpdateParams => ({
  appName: '',
  appDesc: '',
  status: '1',
  appKey: '',
  appSecret: '',
  createBy: authStore.userInfo.userName
});

const model = ref<Api.DataService.ServiceAppUpdateParams>(createDefaultModel());

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: '新增应用',
    edit: '编辑应用'
  };
  return titles[props.operateType];
});

const handleInitModel = async () => {
  Object.assign(model.value, createDefaultModel());
  if (props.operateType === 'add') {
    model.value.appKey = nanoid(32);
    model.value.appSecret = nanoid(32);
  }
  if (props.operateType === 'edit' && props.rowData) {
    const response = await fetchServiceAppDetail({ id: props.rowData.id });
    Object.assign(model.value, response.data?.records);
  }
};

// 定义表单的必填项
type RuleKey = Extract<keyof Api.DataService.ServiceAppUpdateParams, 'appName' | 'appDesc'>;
const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();
const rules = ref<Record<RuleKey, App.Global.FormRule>>({
  appName: defaultRequiredRule,
  appDesc: defaultRequiredRule
});

// 关闭表单
const closeDrawer = () => {
  visible.value = false;
};

const handleSubmit = async () => {
  await validate();
  // request

  if (props.operateType === 'add') {
    const { error } = await fetchAddServiceApp(model.value);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateServiceApp(model.value);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
};

const showModal = ref(false);
const handleParamAdd = () => {
  showModal.value = !showModal.value;
};

const copyAppSecret = () => {
  navigator.clipboard
    .writeText(model.value.appSecret || '')
    .then(() => {
      window.$message?.success('appSecret 已复制到剪贴板');
    })
    .catch(() => {
      window.$message?.error('复制失败');
    });
};

const copyAppKey = () => {
  navigator.clipboard
    .writeText(model.value.appKey || '')
    .then(() => {
      window.$message?.success('appKey 已复制到剪贴板');
    })
    .catch(() => {
      window.$message?.error('复制失败');
    });
};

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" :width="360">
    <NDrawerContent :title="title">
      <template #footer>
        <NButton class="px-6" type="primary" @click="handleSubmit">保存</NButton>
      </template>
      <NForm ref="formRef" :rules="rules" :model="model">
        <NFormItem label="应用名称" path="appName">
          <NInput v-model:value="model.appName" />
        </NFormItem>
        <NFormItem label="应用描述" path="appDesc">
          <NInput v-model:value="model.appDesc" type="textarea" :autosize="{ minRows: 2 }" />
        </NFormItem>
        <NFormItem label="状态" path="status">
          <NRadioGroup v-model:value="model.status">
            <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="$t(item.label)" />
          </NRadioGroup>
        </NFormItem>
        <NFormItem label="appKey" path="appKey">
          <NInput v-model:value="model.appKey" disabled>
            <template #suffix>
              <NButton size="small" @click="copyAppKey">复制</NButton>
            </template>
          </NInput>
        </NFormItem>
        <NFormItem label="appSecret" path="appSecret">
          <NInput v-model:value="model.appSecret" disabled>
            <template #suffix>
              <NButton size="small" @click="copyAppSecret">复制</NButton>
            </template>
          </NInput>
        </NFormItem>
      </NForm>
      <div class="text-xl font-semibold">关联API</div>
      <NButton type="info" class="mb-5 w-20" @click="handleParamAdd">{{ $t('common.append') }}</NButton>
    </NDrawerContent>
  </NDrawer>
</template>
