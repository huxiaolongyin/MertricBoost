<script setup lang="tsx">
import { Icon } from '@iconify/vue';
import { NButton } from 'naive-ui';
import { computed, ref, watch } from 'vue';
import { useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { fetchAddDecision, fetchDecisionDetail, fetchUpdateDecision } from '@/service/api';
import { useAuthStore } from '@/store/modules/auth';

const authStore = useAuthStore();
// 定义传参
interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.Decision.DecisionData | null;
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
const createDefaultModel = (): Api.Decision.DecisionUpdateParams => ({
  decisionName: '',
  decisionDesc: '',
  createBy: authStore.userInfo.userName
});

const model = ref<Api.Decision.DecisionUpdateParams>(createDefaultModel());

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: '新增决策',
    edit: '编辑决策'
  };
  return titles[props.operateType];
});

const handleInitModel = async () => {
  Object.assign(model.value, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    const response = await fetchDecisionDetail({ id: props.rowData.id });
    Object.assign(model.value, response.data?.records);
  }
};

// 定义表单的必填项
// type RuleKey = Extract<keyof Api.Decision.DecisionUpdateParams, 'appName' | 'appDesc'>;
const { validate, restoreValidation } = useNaiveForm();
// const { defaultRequiredRule } = useFormRules();
// const rules = ref<Record<RuleKey, App.Global.FormRule>>({
//   appName: defaultRequiredRule,
//   appDesc: defaultRequiredRule
// });

// 关闭表单
const closeDrawer = () => {
  visible.value = false;
};

const handleSubmit = async () => {
  await validate();
  // request

  if (props.operateType === 'add') {
    const { error } = await fetchAddDecision(model.value);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateDecision(model.value);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
};

// const showModal = ref(false);
// const handleParamAdd = () => {
//   showModal.value = !showModal.value;
// };

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" :width="1080">
    <NDrawerContent :title="title">
      <template #footer>
        <NButton class="px-6" type="primary" @click="handleSubmit">保存</NButton>
      </template>
      <NForm class="ml-5 mt-5">
        <NFlex align="center" class="mb-5">
          <Icon icon="mdi:numeric-1-circle" width="40" height="40" class="text-blue-700" />
          <div class="text-xl font-semibold">决策事件基本信息</div>
        </NFlex>
        <div class="ml-20">
          <NFormItem label="事件名称" label-placement="left" class="w-11/12">
            <NInput placeholder="请输入事件名称" />
          </NFormItem>
          <NFormItem label="事件描述" label-placement="left" class="w-11/12">
            <NInput placeholder="请输入事件描述" type="textarea" />
          </NFormItem>
          <NFormItem label="事件状态" label-placement="left" class="w-11/12">
            <NSwitch />
          </NFormItem>
          <NFormItem label="执行频率：" label-placement="left" class="w-11/12">
            <NFlex align="center" class="w-11/12">
              <div>每隔</div>
              <NInputNumber class="w-2/12" />
              <NSelect class="w-2/12" />
              <div>检查一次</div>
            </NFlex>
          </NFormItem>
        </div>
        <NFlex align="center" class="mb-5">
          <Icon icon="mdi:numeric-2-circle" width="40" height="40" class="text-blue-700" />
          <div class="text-xl font-semibold">配置决策</div>
        </NFlex>
        <NFormItem>
          <NFlex align="center" class="ml-15 w-10/12 bg-slate-100 px-5 py-2">
            <div>如果</div>
            <NSelect placeholder="生产效率" class="w-3/12" />
            <NSelect placeholder="低于" class="w-2/12" />
            <div class="w-2/12">
              <NInput placeholder="80%" />
            </div>
            <div>那么</div>
            <NSelect placeholder="发送通知邮件" class="w-3/12" />
          </NFlex>
        </NFormItem>
        <div class="add-branch ml-15 text-blue-700 hover:text-blue-900">添加分支+</div>
      </NForm>
    </NDrawerContent>
  </NDrawer>
</template>
