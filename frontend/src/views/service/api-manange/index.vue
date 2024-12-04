<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <ApiSearch
      v-model:model="searchParams"
      @reset="resetSearchParams"
      @search="getData"
    />
    <NCard
      title="API管理"
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
          :show-add-button="false"
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
        :row-key="(row) => row.id"
        :pagination="mobilePagination"
        class="sm:h-full"
      />
      <ServiceApiDrawer
        v-model:visible="drawerVisible"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="getData"
      />
    </NCard>
  </div>
</template>
<script setup lang="tsx">
import { $t } from "@/locales";
import ServiceApiDrawer from "./modules/service-api-operate-drawer.vue";
import ApiSearch from "./modules/api-search.vue";
import { enableStatusRecord } from "@/constants/business";
import { fetchServiceApiList, fetchDeleteServiceApi } from "@/service/api";
import { useAppStore } from "@/store/modules/app";
import { useTable, useTableOperate } from "@/hooks/common/table";
import { NButton, NPopconfirm, NTag } from "naive-ui";

const appStore = useAppStore();

const {
  columns,
  columnChecks,
  data,
  loading,
  getData,
  mobilePagination,
  searchParams,
  resetSearchParams,
} = useTable({
  apiFn: fetchServiceApiList,
  apiParams: {
    current: 1,
    size: 10,
    // 如果要在Form中使用searchParams，则需要定义以下属性，且值为null
    // 该值不能为undefined，否则Form中的属性将不会反应
    status: null,
    apiMethod: null,
    apiName: null,
    createBy: null,
  },
  columns: () => [
    {
      type: "selection",
      align: "center",
      width: 48,
    },
    {
      key: "apiName",
      title: "API名称",
      width: 200,
    },
    {
      key: "apiDesc",
      title: "API描述",
      width: 400,
    },
    {
      key: "metricName",
      title: "指标名称",
      width: 200,
    },
    {
      key: "status",
      title: "状态",
      width: 80,
      render: (row) => {
        if (row.status === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          1: "success",
          2: "warning",
        };

        const label = $t(enableStatusRecord[row.status]);

        return <NTag type={tagMap[row.status]}>{label}</NTag>;
      },
    },
    {
      key: "apiMethod",
      title: "类型",
      width: 120,
    },
    {
      key: "apiPath",
      title: "API路径",
      align: "center",
      width: 160,
    },

    {
      title: "创建时间",
      key: "createTime",
      width: 160,
    },
    {
      title: "创建人",
      key: "createBy",
      width: 160,
    },
    {
      key: "operate",
      title: $t("common.operate"),
      align: "center",
      width: 160,
      render: (row) => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
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
  ],
});

const {
  drawerVisible,
  operateType,
  editingData,
  handleAdd,
  handleEdit,
  checkedRowKeys,
  onBatchDeleted,
  onDeleted,
  // closeDrawer
} = useTableOperate(data, getData);

async function handleDelete(id: number) {
  // request
  const { error } = await fetchDeleteServiceApi({ id });
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>

<style scoped></style>
