<template>
  <NModal v-model:show="visible" display-directive="show" transform-origin="center" class="h-3/4">
    <NCard :title="title" :bordered="false" size="small" class="card-wrapper w-4/6 h-3/4">
      <NSteps :current="currentStep" status="process" class="mb-10 ml-38">
        <NStep title="选择数据" />
        <NStep title="字段设置" />
        <NStep title="模型信息" />
      </NSteps>
      <Step1 v-if="currentStep === 1" :operateType="props.operateType" />
      <Step2 v-if="currentStep === 2" :operateType="props.operateType" />
      <Step3 v-if="currentStep === 3" />
      <template #footer>
        <NFlex :size="16" justify="end">
          <NButton v-if="currentStep > 1" @click="prevStep" class="w-20">上一个</NButton>
          <NButton v-if="currentStep < 3" @click="nextStep" class="w-20">下一个</NButton>
          <NButton v-if="currentStep === 3" @click="handleSubmit" class="w-20" type="primary">
            确 认
          </NButton>
        </NFlex>
      </template>
    </NCard>
  </NModal>
</template>

<script setup lang="ts">
import { computed, watch } from "vue";
import { useNaiveForm } from "@/hooks/common/form";
import { $t } from "@/locales";
import Step1 from "./step1.vue";
import Step2 from "./step2.vue";
import Step3 from "./step3.vue";
import { useDataModelFormStore } from "@/store/modules/model";
import { useAuthStore } from '@/store/modules/auth';
import { fetchAddDataModel, fetchUpdateDataModel } from '@/service/api';

// 用户状态，用于获取用户名
const authStore = useAuthStore();

defineOptions({
  name: "DataModelOperateDrawer",
});

// 定义传入参数
interface Props {
  operateType: NaiveUI.TableOperateType; // 操作类型
  rowData?: Api.SystemManage.DataModel | null; // 编辑行数据
}

const props = defineProps<Props>();

// 定义传出参数
interface Emits {
  (e: "submitted"): void;
  (e: "newData"): void;
}
const emit = defineEmits<Emits>();

// 设置弹窗标题
const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t("page.dataAsset.dataModel.addDataModel"),
    edit: $t("page.dataAsset.dataModel.editDataModel"),
  };
  return titles[props.operateType];
});


// 双向绑定父组件，用于处理对话框的显示
const visible = defineModel<boolean>("visible", {
  default: false,
});

const { formRef, validate, restoreValidation } = useNaiveForm();

// page2：table 表单的校验逻辑
const validatePage2 = (): boolean => {
  // 至少选择一个日期和一个指标
  const hasDate = dataModelFormStore.stepTwo.fieldConf?.some(row => row.semanticType === 'date');
  const hasMetric = dataModelFormStore.stepTwo.fieldConf?.some(row => row.semanticType === 'metric');

  if (!hasDate) {
    window.$message?.error('请至少选择一个日期类型的字段');
    return false;
  }

  if (!hasMetric) {
    window.$message?.error('请至少选择一个指标类型的字段');
    return false;
  }
  for (const item of dataModelFormStore.stepTwo.fieldConf || []) {


    // 如果语义类型是 'metric'，需要校验 staticType 和 format
    if (item.semanticType === 'metric') {
      if (!item.staticType) {
        window.$message?.error("指标的聚合方式未选择");
        return false;
      }
      if (!item.format) {
        window.$message?.error("指标的格式未选择");
        return false;
      }
    }

    // 如果语义类型是 'date'，需要校验 format
    if (item.semanticType === 'date') {
      if (!item.format) {
        window.$message?.error("日期的格式未选择");
        return false;
      }
    }
  };
  return true;
}

// page3：model 表单的校验逻辑
const validatePage3 = (): boolean => {
  // 必填项校验
  if (!dataModelFormStore.stepThree.dataModelName) {
    window.$message?.error("模型名称不能为空");
    return false;
  }
  if (!dataModelFormStore.stepThree.dataModelDesc) {
    window.$message?.error("模型描述不能为空");
    return false;
  }
  if (!dataModelFormStore.stepThree.dataDomain) {
    window.$message?.error("数据域不能为空");
    return false;
  }
  if (!dataModelFormStore.stepThree.topicDomain) {
    window.$message?.error("主题域不能为空");
    return false;
  }
  if (!dataModelFormStore.stepThree.status) {
    window.$message?.error("状态不能为空");
    return false;
  }
  return true;
}

// 步骤切换模块
const dataModelFormStore = useDataModelFormStore();
const currentStep = computed(() => dataModelFormStore.currentStep);
const nextStep = () => {
  // 表单校验逻辑
  if (currentStep.value == 1) {
    if (dataModelFormStore.stepOne.database && dataModelFormStore.stepOne.tableName) {
      dataModelFormStore.nextStep()
    } else {
      window.$message?.error("未选择数据库或数据表");
    }
  }
  else if (currentStep.value == 2 && validatePage2()) {
    dataModelFormStore.nextStep()
  }
}
const prevStep = () => dataModelFormStore.prevStep();

// 表单提交
const handleSubmit = async () => {
  // 展开数据
  const flattenObject = {
    id: props.rowData?.id,
    database: dataModelFormStore.stepOne.database,
    tableName: dataModelFormStore.stepOne.tableName,
    dataModelName: dataModelFormStore.stepThree.dataModelName,
    dataModelDesc: dataModelFormStore.stepThree.dataModelDesc,
    dataDomain: dataModelFormStore.stepThree.dataDomain,
    topicDomain: dataModelFormStore.stepThree.topicDomain,
    status: dataModelFormStore.stepThree.status,
    fieldConf: JSON.stringify(dataModelFormStore.stepTwo.fieldConf),
    createBy: authStore.userInfo.userName
  }

  // 提交到接口
  if (props.operateType === 'add' && validatePage3()) {
    const { error } = await fetchAddDataModel(flattenObject);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
      // 重置Store
      dataModelFormStore.resetStore();
      // 关闭窗口
      visible.value = false;
      // 刷新列表数据
      emit('newData');
    }
  }
  if (props.operateType === 'edit' && validatePage3()) {
    const { error } = await fetchUpdateDataModel(flattenObject);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
      // 重置Store
      dataModelFormStore.resetStore();
      // 关闭窗口
      visible.value = false;
      // 刷新列表数据
      emit('newData');
    }
  }
}

// 显示时加载数据
watch(visible, () => {
  if (visible.value) {
    // handleInitModel();
    restoreValidation();

    // 如果是编辑，传入数据
    if (props.operateType === 'edit') {
      dataModelFormStore.updateFormData(props.rowData);
    }
    // 如果是新增，重置表单
    else {
      dataModelFormStore.resetStore();
    }
  }
});
</script>


<style scoped>
.steps {
  max-width: 85%;
  margin: 16px auto;
}
</style>
