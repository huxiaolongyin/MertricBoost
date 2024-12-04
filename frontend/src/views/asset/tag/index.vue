<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <NCard :title="$t('page.dataAsset.tag.title')" :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
      <template #header-extra>
        <TableHeaderOperation v-model:columns="columnChecks" :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading" @add="handleAdd" @refresh="getData" />
      </template>

      <!-- 表格 -->
      <NDataTable v-model:checked-row-keys="checkedRowKeys" :columns="columns" :data="data" size="small"
        :flex-height="!appStore.isMobile" :scroll-x="702" :loading="loading" remote :row-key="(row) => row.id"
        :pagination="mobilePagination" class="sm:h-full" />

      <!-- 操作页 -->
      <TagOperateDialog v-model:visible="drawerVisible" :operate-type="operateType" :row-data="editingData"
        @newData="getData" @submitted="getData" />
    </NCard>
  </div>
</template>

<script setup lang="tsx">
import { useAppStore } from "@/store/modules/app";
import { useTable, useTableOperate } from "@/hooks/common/table";
import { fetchTag, fetchDeleteTag } from "@/service/api";
import { $t } from "@/locales";
import { NButton, NPopconfirm, NTag } from "naive-ui";
import TagOperateDialog from "./modules/tag-operate-drawer.vue";

const appStore = useAppStore();

// 创建表格
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
  apiFn: fetchTag,
  apiParams: {
    current: 1,
    size: 10,
    // 如果要在Form中使用searchParams，则需要定义以下属性，且值为null
    // 该值不能为undefined，否则Form中的属性将不会反应
    tagName: null,
    tagType: null,
    createBy: null,
  },
  // 定义列的属性
  columns: () => [
    {
      type: "selection",
      align: "center",
      width: 48,
    },
    {
      key: "index",
      title: $t("common.index"),
      width: 64,
      align: "center",
    },
    {
      key: "tagName",
      title: $t("page.dataAsset.tag.tagName"),
      align: "center",
      minWidth: 80,
    },
    {
      key: "tagType",
      title: $t("page.dataAsset.tag.tagType"),
      align: "center",
      minWidth: 100,
    },
    {
      key: "tagDesc",
      title: $t("page.dataAsset.tag.tagDesc"),
      align: "center",
      width: 250
    },
    {
      key: "createTime",
      title: $t("common.createTime"),
      align: "center",
      minWidth: 80,
    },
    {
      key: "createBy",
      title: $t("common.createBy"),
      align: "center",
      minWidth: 80,
    },
    {
      key: "operate",
      title: $t("common.operate"),
      align: "center",
      width: 130,
      render: (row) => (
        <div class="flex-center gap-8px" >
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
            {$t("common.edit")}
          </NButton>
          < NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
            {{
              default: () => $t("common.confirmDelete"),
              trigger: () => (
                <NButton type="error" ghost size="small" >
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


const handleDelete = async (id: number) => {
  const { error } = await fetchDeleteTag({ id })
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>