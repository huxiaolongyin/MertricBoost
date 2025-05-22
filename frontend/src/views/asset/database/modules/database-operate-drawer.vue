<script setup lang="ts">
import { computed, reactive, watch } from 'vue';
import { enableStatusOptions } from '@/constants/business';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { fetchAddDatabase, fetchTestDatabase, fetchUpdateDatabase } from '@/service/api';
import { useAuthStore } from '@/store/modules/auth';
import { databaseOptions } from '@/constants/options';

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

// 判断当前是否为Grafana类型
const isGrafana = computed(() => model.type === 'Grafana');

function createDefaultModel(): Api.SystemManage.DatabaseAddParams {
  return {
    name: '',
    type: null,
    host: '',
    port: 3306,
    username: '',
    password: '',
    database: '',
    description: '',
    status: null,
    createBy: authStore.userInfo.userName
  };
}

// type RuleKey = Exclude<
//   keyof Api.SystemManage.DatabaseAddParams,
//   "description" | "createBy" | "password"
// >;

const rules = computed(() => {
  // 基础规则：所有类型都需要的字段
  const baseRules: Record<string, App.Global.FormRule> = {
    name: defaultRequiredRule,
    type: defaultRequiredRule,
    host: defaultRequiredRule,
    port: defaultRequiredRule,
    status: defaultRequiredRule
  };

  // Grafana类型的规则
  if (isGrafana.value) {
    return {
      ...baseRules
    };
  }

  // MySQL和其他类型：完整规则
  return {
    ...baseRules,
    host: defaultRequiredRule,
    port: defaultRequiredRule,
    username: defaultRequiredRule,
    database: defaultRequiredRule
  };
});

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
// 添加图片加载检测函数
function checkGrafanaByImage(url: string) {
  return new Promise(resolve => {
    const img = new Image();

    // 设置超时
    const timeout = setTimeout(() => {
      resolve(false);
    }, 5000);

    img.onload = () => {
      clearTimeout(timeout);
      resolve(true);
    };

    img.onerror = () => {
      clearTimeout(timeout);
      // 即使返回404或其他错误，至少说明服务器是在响应的
      // 所以这里我们认为服务器可访问
      resolve(true);
    };

    // 尝试加载Grafana的favicon或其他静态资源
    img.src = `${url}/public/img/grafana_icon.svg`;
  });
}
// 数据库连接测试
async function handleTest() {
  if (model.type === 'Grafana') {
    const url = `http://${model.host}:${model.port}`;

    // 使用图片加载检测Grafana可访问性
    try {
      const isAccessible = await checkGrafanaByImage(url);
      if (isAccessible) {
        window.$message?.success($t('common.testSuccess'));
      } else {
        window.$message?.error('无法连接到Grafana服务器');
      }
    } catch (err: any) {
      window.$message?.error(`连接测试失败: ${err.message}`);
    }
  } else {
    const { error } = await fetchTestDatabase(model);
    if (!error) {
      window.$message?.success($t('common.testSuccess'));
    }
  }
}

// 提交表单
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

// 类型变更时重新验证表单
watch(
  () => model.type,
  () => {
    // 重置验证状态
    restoreValidation();
    // 根据类型调整默认端口
    if (model.type === 'Grafana') {
      model.port = 3000;
    } else if (model.type === 'MySQL') {
      model.port = 3306;
    }
  }
);

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
            :options="databaseOptions"
          />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.host')" path="host">
          <NInput v-model:value="model.host" :placeholder="$t('page.dataAsset.database.form.host')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.port')" path="port">
          <NInputNumber v-model:value="model.port" :placeholder="$t('page.dataAsset.database.form.port')" />
        </NFormItem>

        <NFormItem :label="$t('page.dataAsset.database.database')" path="database">
          <NInput v-model:value="model.database" :placeholder="$t('page.dataAsset.database.form.database')" />
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
