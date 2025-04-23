<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';

// 定义双向模型
const modalVisible = defineModel<boolean>('modalVisible', {
  default: false
});

const paramList = defineModel<Api.DataService.ServiceApiParams[]>('paramList', {
  required: true
});

// 定义传入参数
type Props = {
  method: Api.DataService.Method;
  operateType: NaiveUI.TableOperateType;
  paramId?: number | null;
};
const props = defineProps<Props>();

const { formRef, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.service.serviceApi.form.paramAddTitle'),
    edit: $t('page.service.serviceApi.form.paramEditTitle')
  };
  return titles[props.operateType];
});

type RuleKey = Extract<
  keyof Api.DataService.ServiceApiParams,
  'paramName' | 'paramType' | 'paramDesc' | 'default' | 'example'
>;

const rules = ref<Record<RuleKey, App.Global.FormRule>>({
  paramName: defaultRequiredRule,
  paramType: defaultRequiredRule,
  paramDesc: defaultRequiredRule,
  default: defaultRequiredRule,
  example: defaultRequiredRule
});

// 如果是 GET 则使用 query，如果是POST 则使用 body
const methodKey = {
  get: {
    content: 'QUERY',
    desc: 'query参数'
  },
  post: {
    content: 'BODY',
    desc: '请求方式为POST，参数位置为 BODY'
  }
};

const paramOptions = [
  {
    label: '整型(long)',
    value: 'long'
  },
  {
    label: '浮点型(double)',
    value: 'double'
  },
  {
    label: '字符串(string)',
    value: 'string'
  },
  {
    label: '布尔型(boolean)',
    value: 'boolean'
  }
];

// 设置表单初始值
const createDefaultModel = () => ({
  id: 1,
  paramName: null,
  paramLoc: methodKey[props.method].content,
  paramType: 'string',
  isRequired: 1,
  example: null,
  default: null,
  paramDesc: null
});

const model = ref<Api.DataService.ServiceApiParamsUpdateParams>(createDefaultModel());
const handleInitModel = async () => {
  if (props.operateType === 'edit') {
    const param = paramList.value.find(item => item.id === props.paramId);
    if (param) {
      model.value = param;
    }
  } else {
    model.value = createDefaultModel();
  }
};

const computedIsRequired = computed({
  get: () => model.value.isRequired ?? 1,
  set: val => (model.value.isRequired = val)
});

const closeModal = () => {
  modalVisible.value = false;
};

const handleSubmit = () => {
  closeModal();
};

watch(modalVisible, () => {
  if (modalVisible.value) {
    handleInitModel();
    restoreValidation();
  }
});
</script>

<template>
  <NModal
    v-model:show="modalVisible"
    preset="card"
    :title="title"
    :bordered="false"
    size="huge"
    role="dialog"
    aria-modal="true"
    class="param-modal"
  >
    <NDivider class="modal-divider" />
    <NForm ref="formRef" :model="model" :rules="rules">
      <NFormItem label="参数名" label-placement="left" :label-width="80" path="paramName">
        <NInput v-model:value="model.paramName" placeholder="请输入参数名称" />
      </NFormItem>
      <NFormItem label="参数位置" label-placement="left" :label-width="80" path="paramType">
        <span>{{ methodKey[props.method].content }}</span>
        <span class="ml-4 text-xs text-slate-400">{{ methodKey[props.method].desc }}</span>
      </NFormItem>
      <NFormItem label="参数类型" label-placement="left" :label-width="80" path="paramType">
        <NSelect v-model:value="model.paramType" :options="paramOptions" />
      </NFormItem>
      <NFormItem label="是否必填" label-placement="left" :label-width="80">
        <NSwitch v-model:value="computedIsRequired" :checked-value="1" :unchecked-value="2" />
      </NFormItem>
      <NFormItem label="示例值" label-placement="left" :label-width="80" path="example">
        <NInput v-model:value="model.example" placeholder="将API提供给别人时的参考值" />
      </NFormItem>
      <NFormItem label="默认值" label-placement="left" :label-width="80" path="example">
        <NInput v-model:value="model.default" placeholder="未提供参数时的默认值" />
      </NFormItem>
      <NFormItem label="描述" label-placement="left" :label-width="80" path="paramDesc">
        <NInput v-model:value="model.paramDesc" placeholder="请输入入参描述" type="textarea" />
      </NFormItem>
    </NForm>
    <!-- <template #footer> 尾部 </template> -->
    <template #footer>
      <NFlex justify="end">
        <NButton class="px-6" @click="closeModal">{{ $t('common.cancel') }}</NButton>
        <NButton class="px-6" type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
      </NFlex>
    </template>
  </NModal>
</template>

<style scoped>
.param-modal {
  width: 800px;
}

.modal-divider {
  margin: -16px 0 26px 0;
}
</style>
