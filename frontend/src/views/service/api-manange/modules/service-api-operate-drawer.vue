<template>
  <NDrawer v-model:show="visible" :width="1000">
    <NDrawerContent>
      <template #header>新增API</template>
      <template #footer>
        <NButton class="px-6" type="primary" @click="handleSubmit">保存</NButton>
      </template>
      <NForm ref="formRef" class="ml-2 mt-5" :rules="rules" :model="model">
        <NFlex align="center" class="mb-5">
          <Icon icon="mdi:numeric-1-circle" width="36" height="36" class="text-blue-700" />
          <div class="text-xl font-semibold">基础信息</div>
        </NFlex>
        <div class="ml-10">
          <NFormItem label="选用指标" label-placement="left" class="w-11/12" :label-width="80" path="metricId">
            <NInput v-model:value="model.metricName" disabled />
          </NFormItem>
          <NFormItem label="API 名称" label-placement="left" class="w-11/12" :label-width="80" path="apiName">
            <NInput v-model:value="model.apiName" placeholder="1~64个字符，需以中文、字母开头，仅支持中文、字母、数字、“-”、“_”" />
          </NFormItem>
          <NFormItem label="API Path" label-placement="left" class="w-11/12" :label-width="80" path="apiPath">
            <NInput v-model:value="model.apiPath" placeholder="1~64个字符，支持小写字母、数字和下划线，只能以小写字母和数字开头，比如users" />
          </NFormItem>
          <NFormItem label="API 描述" label-placement="left" class="w-11/12" :label-width="80" path="apiDesc">
            <NInput v-model:value="model.apiDesc" placeholder="请输入API描述" type="textarea" />
          </NFormItem>
          <NFormItem label="请求方式" label-placement="left" class="w-11/12" :label-width="80" path="method">
            <NRadioGroup v-model:value="model.apiMethod">
              <NRadio value="get" key="get">GET</NRadio>
              <NRadio value="post" key="post">POST</NRadio>
            </NRadioGroup>
          </NFormItem>
          <NFormItem label="应用" label-placement="left" class="w-11/12" :label-width="80" path="appId">
            <NSelect v-model:value="model.appId" :options="appOptions" :loading="appLoading" />
          </NFormItem>
        </div>
      </NForm>
      <NFlex align="center" class="mb-5">
        <Icon icon="mdi:numeric-2-circle" width="36" height="36" class="text-blue-700" />
        <div class="text-xl font-semibold">参数设置</div>
      </NFlex>
      <NButton type="info" class="mb-5 w-20" @click="handleParamAdd">添加</NButton>
      <NDataTable :columns="columns" :data="model.params" />
      <NModal v-model:show="showModal">
        <ApiAdd v-model:showModal="showModal" v-model:paramList="model.params" :method="model.apiMethod ?? 'get'" />
      </NModal>
    </NDrawerContent>
  </NDrawer>
</template>

<script setup lang="tsx">
import { onMounted, ref, watch } from "vue";
import { useFormRules, useNaiveForm } from "@/hooks/common/form";
import { $t } from "@/locales";
import { Icon } from "@iconify/vue";
import { NButton, NPopconfirm } from "naive-ui";
import ApiAdd from "./service-api-param-add.vue";
import { useAuthStore } from "@/store/modules/auth";
import {
  fetchAddServiceApi,
  fetchUpdateServiceApi,
  fetchServiceApiDetail,
  fetchServiceAppList,
} from "@/service/api";
import { useLoadOptions } from "@/hooks/common/option";

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
  (e: "submitted"): void;
}
const emit = defineEmits<Emits>();

// 双向模型绑定父子组件的数据
const visible = defineModel<boolean>("visible", {
  default: false,
});

// 定义表单模型
// 初始化模型
const createDefaultModel = (): Api.DataService.ServiceApiUpdateParams => ({
  metricName: "",
  apiName: "",
  apiDesc: "",
  apiPath: "",
  apiMethod: "get" as Api.DataService.Method,
  params: [] as Api.DataService.ServiceApiParams[],
  createBy: authStore.userInfo.userName,
});

const model = ref<Api.DataService.ServiceApiUpdateParams>(createDefaultModel());

const handleInitModel = async () => {
  Object.assign(model.value, createDefaultModel());
  if (props.operateType === "edit" && props.rowData) {
    const response = await fetchServiceApiDetail({ id: props.rowData.id });
    Object.assign(model.value, response.data?.records);
  }
};

// 定义表单的必填项
type RuleKey = Extract<
  keyof Api.DataService.ServiceApiUpdateParams,
  "apiName" | "apiPath" | "apiDesc" | "status" | "appId"
>;
const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();
const rules = ref<Record<RuleKey, App.Global.FormRule>>({
  apiName: defaultRequiredRule,
  apiPath: defaultRequiredRule,
  apiDesc: defaultRequiredRule,
  status: defaultRequiredRule,
  appId: defaultRequiredRule,
});

// 获取启用的应用列表
const {
  options: appOptions,
  loading: appLoading,
  fetchOptions: fetchAppOptions,
} = useLoadOptions(
  () =>
    fetchServiceAppList({
      current: 1,
      size: 9999,
      status: "1",
      userName: authStore.userInfo.userName,
    }),
  "appName",
  "id"
);

fetchAppOptions()

// 关闭表单
const closeDrawer = () => {
  visible.value = false;
};

const handleSubmit = async () => {
  await validate();
  // request

  if (props.operateType === "add") {
    const { error } = await fetchAddServiceApi(model.value);
    if (!error) {
      window.$message?.success($t("common.addSuccess"));
    }
  } else if (props.operateType === "edit") {
    const { error } = await fetchUpdateServiceApi(model.value);
    if (!error) {
      window.$message?.success($t("common.updateSuccess"));
    }
  }

  closeDrawer();
  emit("submitted");
};

const showModal = ref(false);
const handleParamAdd = () => {
  showModal.value = !showModal.value;
};

const columns = [
  {
    key: "paramName",
    title: "参数名称",
    minWidth: 80,
  },
  {
    key: "paramLoc",
    title: "参数位置",
    minWidth: 100,
  },
  {
    key: "paramType",
    title: "参数类型",
    minWidth: 100,
  },
  {
    key: "isRequired",
    title: "是否必填",
    width: 100,
    render: (row: any) => {
      return <div>{row.isRequired ? "是" : "否"}</div>;
    },
  },
  {
    key: "example",
    title: "示例值",
    minWidth: 120,
  },
  {
    key: "paramDesc",
    title: "描述",
    minWidth: 120,
  },
  {
    key: "operate",
    title: "操作",
    width: 130,
    render: (row: any) => (
      <div class="flex-center gap-8px">
        <NButton type="primary" ghost size="small" onClick={() => handleEdit(row.id)}>
          {$t("common.edit")}
        </NButton>
        <NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
          {{
            default: () => $t("common.confirmDelete"),
            trigger: () => (
              <NButton type="error" ghost size="small">
                {$t("common.delete")}
              </NButton>
            ),
          }}
        </NPopconfirm>
      </div>
    ),
  },
];

// 编辑
const handleEdit = (id: number) => {
  console.log(id);
};

// 删除确认
const handleDelete = (id: number) => {
  console.log(id);
};

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
    fetchAppOptions();
  }
});
</script>
