<script setup lang="ts">
import { computed, reactive, watch } from 'vue';
import { enableStatusOptions } from '@/constants/business';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { fetchAddDatabase, fetchTestDatabase, fetchUpdateDatabase } from '@/service/api';
import { useAuthStore } from '@/store/modules/auth';

// 用户状态，用于获取用户名
const authStore = useAuthStore();

defineOptions({
  name: 'DatabaseOperateDrawer'
});

interface Props {
  operateType: NaiveUI.TableOperateType; // 操作类型
  rowData?: Api.SystemManage.Database | null; // 编辑行数据
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
    add: $t('page.dataAsset.database.addDatabase'),
    edit: $t('page.dataAsset.database.editDatabase')
  };
  return titles[props.operateType];
});

const model: Api.SystemManage.DatabaseUpdateParams = reactive(createDefaultModel());

function createDefaultModel(): Api.SystemManage.DatabaseAddParams {
  return {
    name: '',
    type: null,
    host: '',
    port: 3306,
    username: '',
    password: '',
    databaseId: '',
    description: '',
    status: null,
    createBy: authStore.userInfo.userName
  };
}

//  数据库类型
const typeOptions = computed(() => {
  return [
    {
      label: 'MySQL',
      value: 'MySQL'
    },
    {
      label: 'Oracle',
      value: 'Oracle'
    },
    {
      label: 'SQL Server',
      value: 'SQL Server'
    },
    {
      label: 'PostgreSQL',
      value: 'PostgreSQL'
    },
    {
      label: 'MongoDB',
      value: 'MongoDB'
    },
    {
      label: 'Redis',
      value: 'Redis'
    },
    {
      label: 'ClickHouse',
      value: 'ClickHouse'
    },
    {
      label: 'HBase',
      value: 'HBase'
    },
    {
      label: 'Hive',
      value: 'Hive'
    },
    {
      label: 'Elasticsearch',
      value: 'Elasticsearch'
    },
    {
      label: 'Kafka',
      value: 'Kafka'
    },
    {
      label: 'RabbitMQ',
      value: 'RabbitMQ'
    }
  ];
  // return enableStatusOptions;
});

type RuleKey = Exclude<keyof Api.SystemManage.DatabaseAddParams, 'description' | 'createBy' | 'password'>;

const rules: Record<RuleKey, App.Global.FormRule> = {
  name: defaultRequiredRule,
  type: defaultRequiredRule,
  host: defaultRequiredRule,
  port: defaultRequiredRule,
  username: defaultRequiredRule,
  // password: defaultRequiredRule,
  databaseId: defaultRequiredRule,
  status: defaultRequiredRule
};

// const databaseId = computed(() => props.rowData?.id || -1);

// const isEdit = computed(() => props.operateType === 'edit');

function handleInitModel() {
  Object.assign(model, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    Object.assign(model, props.rowData);
  }
}

function closeDrawer() {
  visible.value = false;
}

// 数据库连接测试
async function handleTest() {
  const { error } = await fetchTestDatabase(model);

  if (!error) {
    window.$message?.success($t('common.testSuccess'));
  }
}
async function handleSubmit() {
  await validate();
  // request
  if (props.operateType === 'add') {
    const { error } = await fetchAddDatabase(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateDatabase(model);
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
        <NFormItem :label="$t('page.dataAsset.database.name')" path="name">
          <NInput v-model:value="model.name" :placeholder="$t('page.dataAsset.database.form.name')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.type')" path="type">
          <NSelect
            v-model:value="model.type"
            :placeholder="$t('page.dataAsset.database.form.type')"
            :options="typeOptions"
          />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.host')" path="host">
          <NInput v-model:value="model.host" :placeholder="$t('page.dataAsset.database.form.host')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.port')" path="port">
          <NInputNumber v-model:value="model.port" :placeholder="$t('page.dataAsset.database.form.port')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.database')" path="database">
          <NInput v-model:value="model.databaseId" :placeholder="$t('page.dataAsset.database.form.database')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.username')" path="username">
          <NInput v-model:value="model.username" :placeholder="$t('page.dataAsset.database.form.username')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.password')" path="password">
          <NInput
            v-model:value="model.password"
            :placeholder="$t('page.dataAsset.database.form.password')"
            type="password"
          />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.status')" path="status">
          <NRadioGroup v-model:value="model.status">
            <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="$t(item.label)" />
          </NRadioGroup>
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.description')" path="description">
          <NInput v-model:value="model.description" :placeholder="$t('page.dataAsset.database.form.description')" />
        </NFormItem>
      </NForm>

      <template #footer>
        <NSpace :size="16">
          <NButton @click="handleTest">{{ $t('common.test') }}</NButton>
          <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
          <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
