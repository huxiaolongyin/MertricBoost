<template>
  <NForm :rules="rules">
    <NFormItem label="数据库" path="database">
      <NSelect v-model:value="dataModelFormStore.stepOne.database"
        :placeholder="$t('page.dataAsset.dataModel.form.databaseSelect')" :options="databaseOptions"
        :loading="databaseLoading" clearable />
    </NFormItem>
    <NFormItem label="表名" path="tableName">
      <NSelect v-model:value="dataModelFormStore.stepOne.tableName"
        :placeholder="$t('page.dataAsset.dataModel.form.tableName')" :options="tableOptions" :loading="tableLoading"
        clearable @update:value="() => dataModelFormStore.stepTwo.fieldConf = null" />
    </NFormItem>
  </NForm>
  <NButton type="primary" class="w-20 mb-5" @click="handlePreview"> 预 览 </NButton>
  <NDataTable :columns="columns" :data="previewData" size="small" :loading="isDataLoading" class="sm:h-full"
    :pagination="pagination" scroll-y="700" :max-height="250" />
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import type { DataTableColumns } from "naive-ui";
import { fetchDatabaseList, fetchGetTableList, fetchDataPreview } from "@/service/api";
import { useDataModelFormStore } from "@/store/modules/model";
import type { FormRules } from 'naive-ui';
import { useLoadOptions } from '@/hooks/common/option'

// 获取数据模型表单状态存储内容
const dataModelFormStore = useDataModelFormStore();

// 定义传入参数
interface Props {
  operateType: NaiveUI.TableOperateType;
}
const props = defineProps<Props>();

// 设置表单的验证规则
const rules: FormRules = {
  database: {
    required: true,
    message: '请选择数据库',
    // trigger: ['input']
  },
  tableName: {
    required: true,
    message: '请选择表名',
    // trigger: ['change'],
  }
};

// 加载非禁用的数据库列表
const {
  options: databaseOptions,
  loading: databaseLoading,
  fetchOptions: fetchDatabaseOptions
} = useLoadOptions(
  () => fetchDatabaseList({ status: '1' }),
  'databaseName',
  'id')

fetchDatabaseOptions()

// 当选中数据库时加载表列表
const {
  options: tableOptions,
  loading: tableLoading,
  fetchOptions: fetchTableOptions
} = useLoadOptions(
  () => {
    const database = dataModelFormStore.stepOne.database
    if (!database) {
      return Promise.reject('Database is required')
    }
    return fetchGetTableList({ database })
  },
  'TABLE_NAME(TABLE_COMMENT)',
  'TABLE_NAME'
)

// 监听数据库选择变化，或者当数据库有值时，加载表列表
if (dataModelFormStore.stepOne.database) {
  fetchTableOptions()
}
watch(() => dataModelFormStore.stepOne.database, async (newValue) => {
  if (newValue) {
    await fetchTableOptions()
  } else {
    tableOptions.value = []
  }
})


// 数据预览
const previewData = ref<Api.SystemManage.DataPreview[]>([]);
const columns = ref<DataTableColumns>([]);
const isDataLoading = ref(false);

const handlePreview = async () => {
  isDataLoading.value = true;
  try {
    const responseData = await fetchDataPreview({
      current: 1,
      size: 10,
      databaseId: dataModelFormStore.stepOne.database,
      tableName: dataModelFormStore.stepOne.tableName,
      addOrEdit: props.operateType
    });
    columns.value =
      (responseData as any).response.data.columns?.map((item: any) => ({
        title: `${item.columnName}(${item.columnComment})`,
        key: item.columnName,
        sorter: 'default'
      })) || [];
    previewData.value = responseData.data?.records || [];
  } catch (error) {
    console.log(error);
  } finally {
    isDataLoading.value = false;
  }
};

const pagination = ref({
  page: 1,
  pageSize: 5,
  showSizePicker: true,
  pageSizes: [5, 10, 20, 30, 50],
  onChange: (page: number) => {
    pagination.value.page = page
    handlePreview()
  },
  onUpdatePageSize: (pageSize: number) => {
    pagination.value.pageSize = pageSize
    pagination.value.page = 1
    handlePreview()
  }
}
);
</script>
