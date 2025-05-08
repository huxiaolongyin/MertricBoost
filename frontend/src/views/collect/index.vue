<script setup lang="tsx">
import { NButton, NPopconfirm, NTag } from 'naive-ui';
import { enableStatusRecord } from '@/constants/business';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { $t } from '@/locales';
import { fetchCollectList, fetchDeleteCollect } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import CollectOperateDrawer from './modules/collect-operate-drawer.vue';
import CollectSearch from './modules/collect-search.vue';
import CollectFilter from './modules/collect-filter.vue';

const appStore = useAppStore();

const { columns, columnChecks, data, loading, getData, mobilePagination, searchParams, resetSearchParams } = useTable({
  apiFn: fetchCollectList,
  apiParams: {
    page: 1,
    pageSize: 10,
    // 如果要在Form中使用searchParams，则需要定义以下属性，且值为null
    // 该值不能为undefined，否则Form中的属性将不会反应
    name: null,
    type: null,
    status: null,
    originDatabaseIds: null,
    targetDatabaseIds: null
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
      key: 'name',
      title: $t('page.collect.name'),
      align: 'center',
      minWidth: 50
    },
    {
      key: 'type',
      title: $t('page.collect.type'),
      align: 'center',
      minWidth: 50
    },
    {
      key: 'schedule',
      title: $t('page.collect.schedule'),
      align: 'center',
      minWidth: 50
    },

    {
      key: 'originDatabase',
      title: $t('page.collect.originDatabase'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'originTable',
      title: $t('page.collect.originTable'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'targetDatabase',
      title: $t('page.collect.targetDatabase'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'targetTable',
      title: $t('page.collect.targetTable'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'status',
      title: $t('page.collect.status'),
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
  // request
  const { error } = await fetchDeleteCollect({ id });
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
      <NCard :title="$t('page.collect.dataSourceFilter')" :bordered="false" size="small" class="h-full">
        <CollectFilter v-model:model="searchParams" @search="getData" />
      </NCard>
    </NGi>
    <NGi span="5" class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
      <CollectSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData" />
      <NCard :title="$t('page.collect.title')" :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
        <template #header-extra>
          <TableHeaderOperation
            v-model:columns="columnChecks"
            :disabled-delete="checkedRowKeys.length === 0"
            :loading="loading"
            @add="handleAdd"
            @refresh="getData"
          />
          <!-- @delete="handleBatchDelete" -->
        </template>
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
        <CollectOperateDrawer
          v-model:visible="drawerVisible"
          :operate-type="operateType"
          :row-data="editingData"
          @submitted="getData"
        />
      </NCard>
    </NGi>
  </NGrid>
</template>

<style scoped></style>
