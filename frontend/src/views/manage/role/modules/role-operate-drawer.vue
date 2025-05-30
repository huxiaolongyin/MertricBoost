<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useBoolean } from '@sa/hooks';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { fetchAddRole, fetchGetDomainTree, fetchUpdateRole } from '@/service/api';
import { $t } from '@/locales';
import { enableStatusOptions } from '@/constants/business';
import { filteredSensitiveOptions } from '@/constants/options';
import MenuAuthModal from './menu-auth-modal.vue';
import ButtonAuthModal from './button-auth-modal.vue';
import ApiAuthModal from './/api-auth-modal.vue';

defineOptions({
  name: 'RoleOperateDrawer'
});

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.SystemManage.Role | null;
}

const props = defineProps<Props>();

interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
  default: false
});

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();
const { bool: menuAuthVisible, setTrue: openMenuAuthModal } = useBoolean();
const { bool: buttonAuthVisible, setTrue: openButtonAuthModal } = useBoolean();
const { bool: apiAuthVisible, setTrue: openApiAuthModal } = useBoolean();

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.manage.role.addRole'),
    edit: $t('page.manage.role.editRole')
  };
  return titles[props.operateType];
});

const model: Api.SystemManage.RoleUpdateParams = reactive(createDefaultModel());

function createDefaultModel(): Api.SystemManage.RoleAddParams {
  return {
    roleName: '',
    roleCode: '',
    roleDesc: '',
    roleHome: '',
    sensitivity: '',
    domainIds: [],
    status: '0'
  };
}

type RuleKey = Exclude<keyof Api.SystemManage.RoleAddParams, 'roleDesc' | 'roleHome' | 'domainIds'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  roleName: defaultRequiredRule,
  roleCode: defaultRequiredRule,
  status: defaultRequiredRule,
  sensitivity: defaultRequiredRule
};

const roleId = computed(() => props.rowData?.id || -1);

const isEdit = computed(() => props.operateType === 'edit');

// 获取主题域列表
const domainOptions = ref<Api.SystemManage.DomainTree[]>([]);

// 创建一个函数来获取领域树数据
async function fetchDomainTreeOptions() {
  const { error, data } = await fetchGetDomainTree();
  if (!error && data) {
    domainOptions.value = data;
  }
}

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
  await validate();
  // request
  if (props.operateType === 'add') {
    const { error } = await fetchAddRole(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateRole(model);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
}

// 在组件挂载时获取数据
onMounted(() => {
  fetchDomainTreeOptions();
});

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" display-directive="show" :width="360">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules">
        <NFormItem :label="$t('page.manage.role.roleName')" path="roleName">
          <NInput v-model:value="model.roleName" :placeholder="$t('page.manage.role.form.roleName')" />
        </NFormItem>
        <NFormItem :label="$t('page.manage.role.roleCode')" path="roleCode">
          <NInput v-model:value="model.roleCode" :placeholder="$t('page.manage.role.form.roleCode')" />
        </NFormItem>
        <NFormItem :label="$t('page.manage.role.sensitivity')" path="sensitivity">
          <NSelect
            v-model:value="model.sensitivity"
            :placeholder="$t('page.manage.role.form.sensitivity')"
            :options="filteredSensitiveOptions"
          />
        </NFormItem>
        <NFormItem :label="$t('page.manage.role.domains')" path="domains">
          <NTreeSelect
            v-model:value="model.domainIds"
            multiple
            cascade
            checkable
            :placeholder="$t('page.manage.role.form.domains')"
            :options="domainOptions"
          />
        </NFormItem>
        <NFormItem :label="$t('page.manage.role.roleStatus')" path="status">
          <NRadioGroup v-model:value="model.status">
            <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="$t(item.label)" />
          </NRadioGroup>
        </NFormItem>
        <NFormItem :label="$t('page.manage.role.roleDesc')" path="roleDesc">
          <NInput v-model:value="model.roleDesc" :placeholder="$t('page.manage.role.form.roleDesc')" />
        </NFormItem>
      </NForm>
      <NSpace v-if="isEdit">
        <NButton @click="openMenuAuthModal">{{ $t('page.manage.role.menuAuth') }}</NButton>
        <MenuAuthModal v-model:visible="menuAuthVisible" :role-id="roleId" :role-home="model.roleHome" />
        <NButton @click="openButtonAuthModal">{{ $t('page.manage.role.buttonAuth') }}</NButton>
        <ButtonAuthModal v-model:visible="buttonAuthVisible" :role-id="roleId" />
        <NButton @click="openApiAuthModal">{{ $t('page.manage.role.apiAuth') }}</NButton>
        <ApiAuthModal v-model:visible="apiAuthVisible" :role-id="roleId" />
      </NSpace>
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
