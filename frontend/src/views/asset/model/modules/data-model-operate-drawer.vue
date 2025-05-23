<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue';
import { useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { fetchAddDataModel, fetchUpdateDataModel } from '@/service/api';
import { useDataModelFormStore } from '@/store/modules/model';
import Step1 from './step1.vue';
import Step2 from './step2.vue';
import Step3 from './step3.vue';
import Grafana from './grafana.vue';

defineOptions({
  name: 'DataModelOperateDrawer'
});

// 定义传入参数
interface Props {
  operateType: NaiveUI.TableOperateType; // 操作类型
  rowData?: Api.SystemManage.DataModel | null; // 编辑行数据
}

const props = defineProps<Props>();

// 定义传出参数
interface Emits {
  // (e: "submitted"): void;
  (e: 'newData'): void;
}
const emit = defineEmits<Emits>();

// 获取数据模型表单状态
const dataModelFormStore = useDataModelFormStore();

const uiState = reactive({
  // 设置弹窗标题
  title: computed(() => {
    const titles: Record<NaiveUI.TableOperateType, string> = {
      add: $t('page.dataAsset.dataModel.addDataModel'),
      edit: $t('page.dataAsset.dataModel.editDataModel')
    };
    return titles[props.operateType];
  }),
  // 步骤切换模块
  defaultTab: computed(() => {
    return dataModelFormStore.stepOne.tableName ? 'SQL' : 'Grafana';
  }),
  // 当前步骤
  currentStep: computed(() => dataModelFormStore.currentStep)
});

// 双向绑定父组件，用于处理对话框的显示
const visible = defineModel<boolean>('visible', {
  default: false
});

// 当前激活的标签
const activeTab = ref<string>('SQL');

const { restoreValidation } = useNaiveForm();

// page2：table 表单的校验逻辑
const validatePage2 = (): boolean => {
  // 至少选择一个日期和一个指标
  const hasDate = dataModelFormStore.stepTwo.columnsConf?.some(row => row.staticType === 'date');
  const hasMetric = dataModelFormStore.stepTwo.columnsConf?.some(row => row.staticType === 'metric');

  if (!hasDate) {
    window.$message?.error('请至少选择一个日期类型的字段');
    return false;
  }

  if (!hasMetric) {
    window.$message?.error('请至少选择一个指标类型的字段');
    return false;
  }
  for (const item of dataModelFormStore.stepTwo.columnsConf || []) {
    // 如果语义类型是 'metric'，需要校验 staticType 和 format
    if (item.staticType === 'metric') {
      if (!item.aggMethod) {
        window.$message?.error('指标的聚合方式未选择');
        return false;
      }
      if (!item.format) {
        window.$message?.error('指标的格式未选择');
        return false;
      }
    }

    // 如果语义类型是 'date'，需要校验 format
    if (item.staticType === 'date') {
      if (!item.format) {
        window.$message?.error('日期的格式未选择');
        return false;
      }
    }
  }
  return true;
};

// page3：model 表单的校验逻辑
const validatePage3 = (): boolean => {
  // 必填项校验
  if (!dataModelFormStore.stepThree.name) {
    window.$message?.error('模型名称不能为空');
    return false;
  }
  if (!dataModelFormStore.stepThree.description) {
    window.$message?.error('模型描述不能为空');
    return false;
  }
  if (!dataModelFormStore.stepThree.dataDomains) {
    window.$message?.error('数据域不能为空');
    return false;
  }
  if (!dataModelFormStore.stepThree.topicDomains) {
    window.$message?.error('主题域不能为空');
    return false;
  }
  if (!dataModelFormStore.stepThree.status) {
    window.$message?.error('状态不能为空');
    return false;
  }
  return true;
};

const nextStep = () => {
  // 表单校验逻辑
  if (uiState.currentStep === 1) {
    if (dataModelFormStore.stepOne.databaseId && dataModelFormStore.stepOne.tableName) {
      dataModelFormStore.nextStep();
    } else {
      window.$message?.error('未选择数据库或数据表');
    }
  } else if (uiState.currentStep === 2 && validatePage2()) {
    dataModelFormStore.nextStep();
  }
};
const prevStep = () => dataModelFormStore.prevStep();

// 表单提交
const handleSubmit = async () => {
  // 展开数据
  const flattenObject = {
    id: props.rowData?.id,
    name: dataModelFormStore.stepThree.name,
    description: dataModelFormStore.stepThree.description,
    tableName: dataModelFormStore.stepOne.tableName,
    status: dataModelFormStore.stepThree.status,
    columnsConf: JSON.stringify(dataModelFormStore.stepTwo.columnsConf),
    databaseId: dataModelFormStore.stepOne.databaseId,
    domainIds: [
      ...(dataModelFormStore.stepThree.dataDomains ?? []),
      ...(dataModelFormStore.stepThree.topicDomains ?? [])
    ],
    url: dataModelFormStore.grafana.url
  };

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
};

// 显示时加载数据
watch(visible, () => {
  if (visible.value) {
    restoreValidation();

    // 如果是编辑，传入数据
    if (props.operateType === 'edit') {
      dataModelFormStore.updateFormData(props.rowData);
      // Set the active tab based on the data after it's loaded
      nextTick(() => {
        activeTab.value = dataModelFormStore.grafana.url ? 'Grafana' : 'SQL';
      });
    }
    // 如果是新增，重置表单
    else {
      dataModelFormStore.resetStore();
      activeTab.value = 'SQL'; // Default for new entries
    }
  }
});

// Add a handler for tab changes
const handleTabChange = (tabName: string) => {
  activeTab.value = tabName;
};
</script>

<template>
  <NModal v-model:show="visible" display-directive="show" transform-origin="center" class="h-3/4 w-4/6">
    <NTabs
      type="bar"
      placement="left"
      tab-class="bg-indigo-200 rounded-xl"
      pane-class="bg-gray-400 rounded-sm"
      :value="activeTab"
      default-value="SQL"
      @update:value="handleTabChange"
    >
      <NTabPane name="SQL" tab="数据库">
        <NCard :title="uiState.title">
          <NSteps :current="uiState.currentStep" status="process" class="mb-10 ml-38">
            <NStep title="选择数据" />
            <NStep title="字段设置" />
            <NStep title="模型信息" />
          </NSteps>
          <Step1 v-if="uiState.currentStep === 1" />
          <Step2 v-if="uiState.currentStep === 2" :operate-type="props.operateType" />
          <Step3 v-if="uiState.currentStep === 3" />
          <template #footer>
            <NFlex :size="16" justify="end">
              <NButton v-if="uiState.currentStep > 1" class="w-20" @click="prevStep">上一个</NButton>
              <NButton v-if="uiState.currentStep < 3" class="w-20" @click="nextStep">下一个</NButton>
              <NButton v-if="uiState.currentStep === 3" class="w-20" type="primary" @click="handleSubmit">
                确 认
              </NButton>
            </NFlex>
          </template>
        </NCard>
      </NTabPane>
      <NTabPane name="Grafana" tab="Grafana">
        <NCard :title="uiState.title">
          <Grafana />
          <template #footer>
            <NFlex :size="16" justify="end">
              <NButton class="w-20" type="primary" @click="handleSubmit">确 认</NButton>
            </NFlex>
          </template>
        </NCard>
      </NTabPane>
    </NTabs>
  </NModal>
</template>

<style scoped>
.steps {
  max-width: 85%;
  margin: 16px auto;
}
</style>
