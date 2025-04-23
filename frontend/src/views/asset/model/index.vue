<script setup lang="tsx">
import { NButton, NPopconfirm, NTag } from 'naive-ui';
import { enableStatusRecord } from '@/constants/business';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { $t } from '@/locales';
import { fetchDataModelList, fetchDeleteDataModel } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import DataModelOperateDialog from './modules/data-model-operate-drawer.vue';
import DataModelSearch from './modules/data-model-search.vue';
import DomainFilter from './modules/domain-filter.vue';

const appStore = useAppStore();

// 创建表格
const { columns, columnChecks, data, loading, getData, mobilePagination, searchParams, resetSearchParams } = useTable({
  apiFn: fetchDataModelList,
  apiParams: {
    page: 1,
    pageSize: 10,
    // 如果要在Form中使用searchParams，则需要定义以下属性，且值为null
    // 该值不能为undefined，否则Form中的属性将不会反应
    domainIds: [],
    name: null,
    status: null,
    createBy: null
  },
  // 定义列的属性
  columns: () => [
    {
      type: 'selection',
      align: 'center',
      width: 48
    },
    {
      key: 'index',
      title: $t('common.index'),
      width: 64,
      align: 'center'
    },
    {
      key: 'name',
      title: $t('page.dataAsset.dataModel.name'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'description',
      title: $t('page.dataAsset.dataModel.description'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'status',
      title: $t('page.dataAsset.dataModel.status'),
      align: 'center',
      width: 100,
      render: row => {
        if (row.status === null) {
          return null;
        }
        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          1: 'success',
          0: 'warning'
        };
        const label = $t(enableStatusRecord[row.status]);
        return <NTag type={tagMap[row.status]}> {label} </NTag>;
      }
    },
    {
      key: 'createTime',
      title: $t('common.createTime'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'createBy',
      title: $t('common.createBy'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 130,
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
            {$t('common.edit')}
          </NButton>
          <NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
            {{
              default: () => $t('common.confirmDelete'),
              trigger: () => (
                <NButton type="error" ghost size="small">
                  {$t('common.delete')}
                </NButton>
              )
            }}
          </NPopconfirm>
        </div>
      )
    }
  ]
});

const {
  drawerVisible,
  operateType,
  editingData,
  handleAdd,
  handleEdit,
  checkedRowKeys,
  // onBatchDeleted,
  onDeleted
  // closeDrawer
} = useTableOperate(data, getData);

// async function handleBatchDelete() {
//   // request
//   const { error } = await fetchBatchDeleteDatabase({ ids: checkedRowKeys.value });
//   if (!error) {
//     onBatchDeleted();
//   }
// }

async function handleDelete(id: number) {
  const { error } = await fetchDeleteDataModel({ id });
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>

<template>
  <NGrid cols="6" x-gap="16" y-gap="16" responsive="screen" class="h-full">
    <!-- 左侧的筛选栏 -->
    <NGi span="1" class="h-full">
      <NCard :title="$t('page.dataAsset.dataModel.filter')" :bordered="false" size="small" class="h-full">
        <DomainFilter v-model:model="searchParams" @search="getData" />
      </NCard>
    </NGi>
    <NGi span="5" class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
      <!-- 顶部搜索栏 -->
      <DataModelSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData" />
      <NCard
        :title="$t('page.dataAsset.dataModel.title')"
        :bordered="false"
        size="small"
        class="sm:flex-1-hidden card-wrapper"
      >
        <template #header-extra>
          <TableHeaderOperation
            v-model:columns="columnChecks"
            :disabled-delete="checkedRowKeys.length === 0"
            :loading="loading"
            @add="handleAdd"
            @refresh="getData"
          />
        </template>

        <!-- 表格 -->
        <NDataTable
          v-model:checked-row-keys="checkedRowKeys"
          :columns="columns"
          :data="data"
          size="small"
          :flex-height="!appStore.isMobile"
          :scroll-x="702"
          :loading="loading"
          remote
          :row-key="row => row.id"
          :pagination="mobilePagination"
          class="sm:h-full"
        />

        <!-- 操作页 -->
        <DataModelOperateDialog
          v-model:visible="drawerVisible"
          :operate-type="operateType"
          :row-data="editingData"
          @new-data="getData"
          @submitted="getData"
        />
      </NCard>
    </NGi>
  </NGrid>
</template>

<style scoped></style>
