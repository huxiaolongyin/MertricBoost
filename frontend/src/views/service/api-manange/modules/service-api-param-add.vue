<template>
  <NCard
    style="width: 800px"
    title="添加入参定义"
    :bordered="false"
    size="huge"
    role="dialog"
    aria-modal="true"
  >
    <NDivider style="margin: -16px 0 26px 0" />
    <!-- <template #header-extra> 噢！ </template> -->
    <NForm :model="formValue" :rules="rules">
      <NFormItem label="参数名" label-placement="left" :label-width="80" path="paramName">
        <NInput v-model:value="formValue.paramName" placeholder="请输入参数名称" />
      </NFormItem>
      <NFormItem
        label="参数位置"
        label-placement="left"
        :label-width="80"
        path="paramType"
      >
        <span>{{ methodKey[props.method].content }}</span
        ><span class="ml-4 text-xs text-slate-400">{{
          methodKey[props.method].desc
        }}</span>
      </NFormItem>
      <NFormItem
        label="参数类型"
        label-placement="left"
        :label-width="80"
        path="paramType"
      >
        <NSelect v-model:value="formValue.paramType" :options="paramOptions" />
      </NFormItem>
      <NFormItem
        label="是否必填"
        label-placement="left"
        :label-width="80"
        path="isRequired"
      >
        <NSwitch v-model:value="formValue.isRequired" />
      </NFormItem>
      <NFormItem label="示例值" label-placement="left" :label-width="80" path="example">
        <NInput
          v-model:value="formValue.example"
          placeholder="将API提供给别人时的参考值"
        />
      </NFormItem>
      <NFormItem label="描述" label-placement="left" :label-width="80" path="paramDesc">
        <NInput
          v-model:value="formValue.paramDesc"
          placeholder="请输入入参描述"
          type="textarea"
        />
      </NFormItem>
    </NForm>
    <!-- <template #footer> 尾部 </template> -->
    <template #footer>
      <NFlex justify="end">
        <NButton class="px-6" @click="showModal = false">取消</NButton>
        <NButton class="px-6" type="primary" @click="handleSubmit">确定</NButton>
      </NFlex>
    </template>
  </NCard>
</template>

<script setup lang="ts">
import { ref } from "vue";

// 定义双向模型
const showModal = defineModel("showModal");
const paramList = defineModel<Api.DataAsset.ParamValue[]>("paramList", {
  required: true,
});
// 定义传入参数
type Props = {
  method: Api.DataService.Method;
};
const props = defineProps<Props>();

const rules = {
  paramName: {
    required: true,
    message: "参数名称不能为空",
    trigger: "blur",
  },
  paramType: {
    required: true,
    message: "参数类型不能为空",
    trigger: "blur",
  },
  isRequired: {
    required: true,
    message: "是否必填不能为空",
    trigger: "blur",
  },
  example: {
    required: true,
    message: "示例值不能为空",
    trigger: "blur",
  },
  paramDesc: {
    required: true,
    message: "参数描述不能为空",
    trigger: "blur",
  },
};

// 如果是 GET 则使用 query，如果是POST 则使用 body
const methodKey = {
  get: {
    content: "QUERY",
    desc: "query参数",
  },
  post: {
    content: "BODY",
    desc: "请求方式为POST，参数位置为 BODY",
  },
};

// 设置表单初始值
const formValue = ref<Api.DataAsset.ParamValue>({
  paramName: null,
  paramLoc: methodKey[props.method].content,
  paramType: "string",
  isRequired: false,
  example: null,
  paramDesc: null,
});

const paramOptions = [
  {
    label: "整型(long)",
    value: "long",
  },
  {
    label: "浮点型(double)",
    value: "double",
  },
  {
    label: "字符串(string)",
    value: "string",
  },
  {
    label: "布尔型(boolean)",
    value: "boolean",
  },
];

const handleSubmit = () => {
  showModal.value = false;

  paramList.value.push(formValue.value);
  console.log(paramList.value);
};
</script>
