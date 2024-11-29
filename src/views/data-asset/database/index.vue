<script setup lang="tsx">
import { NButton, NPopconfirm, NTag } from 'naive-ui';
import { fetchDatabaseList, fetchDeleteDatabase } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { $t } from '@/locales';
import { enableStatusRecord } from '@/constants/business';
import DatabaseOperateDrawer from './modules/database-operate-drawer.vue';
import DatabaseSearch from './modules/database-search.vue';

const appStore = useAppStore();

const { columns, columnChecks, data, loading, getData, mobilePagination, searchParams, resetSearchParams } = useTable({
  apiFn: fetchDatabaseList,
  apiParams: {
    current: 1,
    size: 10,
    // 如果要在Form中使用searchParams，则需要定义以下属性，且值为null
    // 该值不能为undefined，否则Form中的属性将不会反应
    status: null,
    createBy: null
  },
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
      key: 'databaseName',
      title: $t('page.dataAsset.database.databaseName'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'databaseType',
      title: $t('page.dataAsset.database.databaseType'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'databaseHost',
      title: $t('page.dataAsset.database.databaseHost'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'databaseDatabase',
      title: $t('page.dataAsset.database.databaseDatabase'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'status',
      title: $t('page.dataAsset.database.status'),
      align: 'center',
      width: 100,
      render: row => {
        if (row.status === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          1: 'success',
          2: 'warning'
        };

        const label = $t(enableStatusRecord[row.status]);

        return <NTag type={tagMap[row.status]}>{label}</NTag>;
      }
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
  onBatchDeleted,
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
  // request
  const { error } = await fetchDeleteDatabase({ id });
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <DatabaseSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData" />
    <NCard :title="$t('page.dataAsset.database.title')" :bordered="false" size="small"
      class="sm:flex-1-hidden card-wrapper">
      <template #header-extra>
        <TableHeaderOperation v-model:columns="columnChecks" :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading" @add="handleAdd" @refresh="getData" />
        <!-- @delete="handleBatchDelete" -->
      </template>
      <NDataTable v-model:checked-row-keys="checkedRowKeys" :columns="columns" :data="data" size="small"
        :flex-height="!appStore.isMobile" :scroll-x="702" :loading="loading" remote :row-key="row => row.id"
        :pagination="mobilePagination" class="sm:h-full" />
      <DatabaseOperateDrawer v-model:visible="drawerVisible" :operate-type="operateType" :row-data="editingData"
        @submitted="getData" />
    </NCard>
  </div>
</template>

<style scoped></style>