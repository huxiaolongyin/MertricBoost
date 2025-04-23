<script setup lang="tsx">
import { NButton, NPopconfirm } from 'naive-ui';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { $t } from '@/locales';
import { fetchDecisionList, fetchDeleteDecision } from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import DecisionDrawer from './modules/decision-operate-drawer.vue';
import DecisionSearch from './modules/decision-search.vue';

const appStore = useAppStore();

const { columns, columnChecks, data, loading, getData, mobilePagination, searchParams, resetSearchParams } = useTable({
  apiFn: fetchDecisionList,
  apiParams: {
    page: 1,
    pageSize: 10,
    // 如果要在Form中使用searchParams，则需要定义以下属性，且值为null
    // 该值不能为undefined，否则Form中的属性将不会反应
    decisionName: null,
    decisionDesc: null,
    createBy: null
  },
  columns: () => [
    {
      type: 'selection',
      align: 'center',
      width: 48
    },
    {
      key: 'decisionName',
      title: '名称',
      width: 200
    },
    {
      key: 'decisionDesc',
      title: '描述',
      width: 400
    },
    {
      title: '创建时间',
      key: 'createTime',
      width: 160
    },
    {
      title: '创建人',
      key: 'createBy',
      width: 160
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 160,
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
  onDeleted
  // closeDrawer
} = useTableOperate(data, getData);

// 定义基础信息显示
// const infoShow = ref(false);

async function handleDelete(id: number) {
  // request
  const { error } = await fetchDeleteDecision({ id });
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}

// const handleSubmit = () => { };
</script>

<template>
  <!--
 <NFloatButton :right="50" :bottom="60" shape="circle" width="60" height="60" class="bg-red-500" @click="handleAdd">
    <Icon icon="mdi:plus" class="text-white" width="35" height="35" />
  </NFloatButton> 
-->
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <DecisionSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData" />
    <NCard title="决策管理" :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          :show-add-button="false"
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
      <DecisionDrawer
        v-model:visible="drawerVisible"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="getData"
      />
    </NCard>
  </div>
</template>

<style scoped></style>
