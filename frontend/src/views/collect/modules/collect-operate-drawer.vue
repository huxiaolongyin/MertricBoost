<script setup lang="ts">
import { computed, reactive, watch } from 'vue';
import type { SelectOption } from 'naive-ui';
import { NForm, NFormItem, NInput, NSelect } from 'naive-ui';
import { enableStatusOptions } from '@/constants/business';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { fetchAddCollect, fetchDatabaseList, fetchUpdateCollect } from '@/service/api';
import { collectOptions } from '@/constants/options';
import { useLoadOptions } from '@/hooks/common/option';

defineOptions({
  name: 'CollectOperateDrawer'
});

interface Props {
  operateType: NaiveUI.TableOperateType; // 操作类型
  rowData?: Api.Collect.Collect | null; // 编辑行数据
}

const props = defineProps<Props>();

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
  return props.operateType === 'add' ? $t('page.collect.addCollect') : $t('page.collect.editCollect');
});

const { validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const model: Api.Collect.CollectAddParams = reactive(createDefaultModel());

function createDefaultModel(): Api.Collect.CollectAddParams {
  return {
    name: '',
    type: null,
    schedule: null,
    originDatabaseId: null,
    originTable: null,
    targetDatabaseId: null,
    targetTable: null
  };
}

type RuleKey = Exclude<keyof Api.Collect.CollectAddParams, 'id'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  name: defaultRequiredRule,
  type: defaultRequiredRule,
  schedule: defaultRequiredRule,
  originDatabaseId: defaultRequiredRule,
  originTable: defaultRequiredRule,
  targetDatabaseId: defaultRequiredRule,
  targetTable: defaultRequiredRule,
  status: defaultRequiredRule
};

function handleInitModel() {
  Object.assign(model, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    Object.assign(model, props.rowData);
  }
}

const databaseTypeOptions: SelectOption[] = [
  {
    label: 'MySQL',
    value: 'mysql'
  }
];

const { options: databaseOptions, fetchOptions: fetchdatabaseOptions } = useLoadOptions(
  () => fetchDatabaseList({ status: '1' }),
  {
    labelKey: 'name',
    valueKey: 'id'
  }
);

fetchdatabaseOptions();

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  // request
  if (props.operateType === 'add') {
    const { error } = await fetchAddCollect(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateCollect(model);
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
  <NDrawer v-model:show="visible" :width="1000">
    <NDrawerContent>
      <template #header>{{ drawerTitle }}</template>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
          <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
        </NSpace>
      </template>
      <NForm :model="model" :rules="rules" class="" label-align="left" label-placement="left">
        <div class="mb-2 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.collect.formTile.baseInfo`) }}
        </div>
        <NGrid cols="s:1 m:2 l:3" responsive="screen" :x-gap="16" :y-gap="16" class="">
          <NGi>
            <NFormItem key="collectName" path="name" label="名称">
              <NInput v-model:value="model.name" placeholder="请输入名称" />
            </NFormItem>
          </NGi>
          <NGi>
            <NFormItem key="collectType" path="type" label="同步类型">
              <NSelect v-model:value="model.type" placeholder="请选择同步类型" :options="collectOptions" clearable />
            </NFormItem>
          </NGi>
          <NGi v-if="model.type === '离线'">
            <NFormItem key="batchSchedule" path="schedule" label="同步时间">
              <NInput v-model:value="model.schedule" placeholder="请输入同步时间" />
            </NFormItem>
          </NGi>
        </NGrid>
        <div class="mb-2 mt-2 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.collect.formTile.collectForm`) }}
        </div>
        <NGrid cols="s:1 m:2 l:2" responsive="screen" :x-gap="16" :y-gap="16" class="">
          <NGi>
            <NCard title="数据来源" class="shadow-sm transition-shadow duration-300 hover:shadow-md">
              <div class="section-title mb-2 flex items-center text-base">数据源</div>
              <NGrid cols="3">
                <NGi span="1">
                  <NSelect placeholder="类型" clearable :options="databaseTypeOptions" />
                </NGi>
                <NGi span="2">
                  <NFormItem key="originDatabaseId" path="originDatabaseId">
                    <NSelect
                      v-model:value="model.originDatabaseId"
                      placeholder="请选择数据源名称"
                      :options="databaseOptions"
                      clearable
                    />
                  </NFormItem>
                </NGi>
              </NGrid>
              <div class="section-title mb-2 flex items-center text-base">数据表</div>
              <NFormItem key="targetTable" path="targetTable">
                <NSelect v-model:value="model.targetTable" placeholder="请选择数据表名称" clearable />
              </NFormItem>
            </NCard>
          </NGi>
          <NGi>
            <NCard title="数据去向" class="shadow-sm transition-shadow duration-300 hover:shadow-md">
              <div class="section-title mb-2 flex items-center text-base">数据源</div>
              <NGrid cols="3">
                <NGi span="1">
                  <NSelect placeholder="类型" clearable :options="databaseTypeOptions" />
                </NGi>
                <NGi span="2">
                  <NFormItem key="targetDatabaseId" path="targetDatabaseId">
                    <NSelect v-model:value="model.targetDatabaseId" placeholder="请选择数据源名称" clearable />
                  </NFormItem>
                </NGi>
              </NGrid>
              <div class="section-title mb-2 flex items-center text-base">数据表</div>
              <NFormItem key="orginTable" path="orginTable">
                <NSelect v-model:value="model.originTable" placeholder="请选择数据表名称" clearable />
              </NFormItem>
            </NCard>
          </NGi>
        </NGrid>
        <div class="mb-2 mt-8 text-lg text-dark font-semibold font-sans dark:text-white">
          {{ $t(`page.collect.formTile.status`) }}
        </div>
        <NFormItem>
          <NRadioGroup v-model:value="model.status">
            <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="$t(item.label)" />
          </NRadioGroup>
        </NFormItem>
      </NForm>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
