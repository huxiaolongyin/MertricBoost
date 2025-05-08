<script setup lang="ts">
import { computed, reactive, watch } from 'vue';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { fetchAddTag, fetchUpdateTag } from '@/service/api';
import { $t } from '@/locales';
import { useAuthStore } from '@/store/modules/auth';
import { tagTypeOptions } from '@/constants/options';
// 用户状态，用于获取用户名
const authStore = useAuthStore();

defineOptions({
  name: 'TagOperateDrawer'
});

interface Props {
  operateType: NaiveUI.TableOperateType; // 操作类型
  rowData?: Api.Asset.TagData | null; // 编辑行数据
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

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: '添加标签',
    edit: '编辑标签'
  };
  return titles[props.operateType];
});

const model: Api.Asset.TagUpdateParams = reactive(createDefaultModel());

function createDefaultModel(): Api.Asset.TagAddParams {
  return {
    tagName: '',
    tagType: null,
    tagDesc: '',
    createBy: authStore.userInfo.userName
  };
}

type RuleKey = Exclude<keyof Api.Asset.TagAddParams, 'createBy' | 'tagDesc'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  tagName: defaultRequiredRule,
  tagType: defaultRequiredRule
};

// const tagId = computed(() => props.rowData?.id || -1);

// const isEdit = computed(() => props.operateType === "edit");

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
    const { error } = await fetchAddTag(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateTag(model);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }
  closeDrawer();
  emit('submitted');
}

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
        <NFormItem :label="$t('page.dataAsset.tag.tagName')" path="tagName">
          <NInput v-model:value="model.tagName" :placeholder="$t('page.dataAsset.tag.form.tagType')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.tag.tagType')" path="tagType">
          <NSelect
            v-model:value="model.tagType"
            :placeholder="$t('page.dataAsset.tag.form.tagType')"
            :options="tagTypeOptions"
          />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.tag.tagDesc')" path="tagDesc">
          <NInput v-model:value="model.tagDesc" :placeholder="$t('page.dataAsset.tag.form.tagDesc')" />
        </NFormItem>
      </NForm>

      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
          <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>
