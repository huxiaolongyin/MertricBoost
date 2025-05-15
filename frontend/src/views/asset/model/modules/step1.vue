<script setup lang="ts">
import type { DataTableColumns, FormRules } from 'naive-ui';
import { ref, watch } from 'vue';
import { useLoadOptions } from '@/hooks/common/option';
import { fetchDataPreview, fetchDatabaseList, fetchGetTableList } from '@/service/api';
import { useDataModelFormStore } from '@/store/modules/model';

defineOptions({
  name: 'ModelStep1'
});

// 获取数据模型表单状态存储内容
const dataModelFormStore = useDataModelFormStore();

// 定义传入参数
// interface Props {
//   operateType: NaiveUI.TableOperateType;
// }
// const props = defineProps<Props>();

// 设置表单的验证规则
const rules: FormRules = {
  database: {
    required: true,
    message: '请选择数据库'
    // trigger: ['input']
  },
  tableName: {
    required: true,
    message: '请选择表名'
    // trigger: ['change'],
  }
};

// 加载非禁用的数据库列表
const {
  options: databaseOptions,
  loading: databaseLoading,
  fetchOptions: fetchdatabaseOptions
} = useLoadOptions(() => fetchDatabaseList({ status: '1' }), {
  labelKey: 'name',
  valueKey: 'id'
});

fetchdatabaseOptions();

// 当选中数据库时加载表列表
const {
  options: tableOptions,
  loading: tableLoading,
  fetchOptions: fetchTableOptions
} = useLoadOptions(
  () => {
    const databaseId = dataModelFormStore.stepOne.databaseId;
    if (!databaseId) {
      return Promise.reject(new Error('Database is required'));
    }
    return fetchGetTableList({ databaseId });
  },
  { labelKey: 'tableName(tableComment)', valueKey: 'tableName' }
);

// 监听数据库选择变化，或者当数据库有值时，加载表列表
if (dataModelFormStore.stepOne.databaseId) {
  fetchTableOptions();
}
watch(
  () => dataModelFormStore.stepOne.databaseId,
  async newValue => {
    if (newValue) {
      await fetchTableOptions();
    } else {
      tableOptions.value = [];
    }
  }
);

// 数据预览
const previewData = ref<Api.SystemManage.DataPreview[]>([]);
const columns = ref<DataTableColumns>([]);
const isDataLoading = ref(false);

const handlePreview = async () => {
  isDataLoading.value = true;
  try {
    const responseData = await fetchDataPreview({
      page: 1,
      pageSize: 10,
      databaseId: dataModelFormStore.stepOne.databaseId,
      tableName: dataModelFormStore.stepOne.tableName
    });
    if (responseData.data?.records && responseData.data.records.length > 0) {
      const firstRecord = responseData.data.records[0];
      columns.value = Object.keys(firstRecord).map(key => ({
        title: key,
        key,
        sorter: 'default'
      }));
    } else {
      columns.value = [];
    }
    previewData.value = responseData.data?.records || [];
  } catch (error) {
    window.$message?.error(`Failed to fetch data preview: ${error}`);
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
    pagination.value.page = page;
    handlePreview();
  },
  onUpdatePageSize: (pageSize: number) => {
    pagination.value.pageSize = pageSize;
    pagination.value.page = 1;
    handlePreview();
  }
});
</script>

<template>
  <NForm :rules="rules">
    <NFormItem label="数据库" path="database">
      <NSelect
        v-model:value="dataModelFormStore.stepOne.databaseId"
        :placeholder="$t('page.dataAsset.dataModel.form.databaseSelect')"
        :options="databaseOptions"
        :loading="databaseLoading"
        clearable
      />
    </NFormItem>
    <NFormItem label="表名" path="tableName">
      <NSelect
        v-model:value="dataModelFormStore.stepOne.tableName"
        :placeholder="$t('page.dataAsset.dataModel.form.tableName')"
        :options="tableOptions"
        :loading="tableLoading"
        clearable
        @update:value="() => (dataModelFormStore.stepTwo.columnsConf = null)"
      />
    </NFormItem>
  </NForm>
  <NButton type="primary" class="mb-5 w-20" @click="handlePreview">预 览</NButton>
  <NDataTable
    :columns="columns"
    :data="previewData"
    size="small"
    :loading="isDataLoading"
    class="sm:h-full"
    :pagination="pagination"
    scroll-y="700"
    :max-height="250"
  />
</template>
