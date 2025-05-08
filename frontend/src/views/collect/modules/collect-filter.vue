<script setup lang="tsx">
import type { TreeOption } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { onMounted, ref } from 'vue';
import { fetchDatabaseList } from '@/service/api';

defineOptions({
  name: 'CollectFilter'
});

const emit = defineEmits<{
  (e: 'search'): void;
}>();

// 和父组件双向绑定模型
const model = defineModel<Api.Collect.CollectSearchParams>('model', {
  required: true
});

// 初始化一些数据
const filterTreeData = ref<TreeOption[]>([]);

const filterText = ref('');

const databaseTotal = ref(0);

// 从后端获取数据源，并处理成树形结构
const createTreeData = async (): Promise<TreeOption[]> => {
  const { data: databaseList } = await fetchDatabaseList();

  databaseTotal.value = databaseList?.records?.length ?? 0;

  const databasesByType: Record<string, Api.SystemManage.Database[]> = {};
  if (databaseList?.records && Array.isArray(databaseList.records)) {
    databaseList.records.forEach(db => {
      if (!databasesByType[db.type]) {
        databasesByType[db.type] = [];
      }
      databasesByType[db.type].push(db);
    });
  }

  const treeData: TreeOption[] = [];

  for (const type in databasesByType) {
    if (Object.hasOwn(databasesByType, type)) {
      const databases = databasesByType[type];
      const typeNode: TreeOption = {
        label: `${type}(${databases.length})`,
        key: type,
        children: databases.map(db => ({
          label: db.name,
          key: db.id.toString(),
          value: db.id,
          type: db.type
        }))
      };
      treeData.push(typeNode);
    }
  }
  return treeData;
};

// 获取数据
const getDatabase = async () => {
  filterTreeData.value = await createTreeData();
};

// 处理选中节点逻辑
const handleNodeSelect = (keys: string[]) => {
  if (keys.length === 0) {
    // 如果没有选中项，清空数据源ID
    model.value.originDatabaseIds = null;
    emit('search');
    return;
  }
  // 更新model，使用选中的keys而不是处理子节点id
  model.value.originDatabaseIds = [...keys];

  // 触发搜索事件
  emit('search');
};

// 在组件加载后，更新筛选树的数据
onMounted(() => {
  try {
    getDatabase();
  } catch (e: any) {
    window.$message?.error(e);
  }
});
</script>

<template>
  <NInput v-model:value="filterText" placeholder="输入数据源类型或名称">
    <template #prefix>
      <Icon icon="mdi:magnify" />
    </template>
  </NInput>
  <div class="mb-2 mt-2">全部数据来源({{ databaseTotal }})</div>
  <NTree
    block-line
    cascade
    :selectable="true"
    :data="filterTreeData"
    :pattern="filterText"
    :show-irrelevant-nodes="false"
    class="custom-tree"
    @update:selected-keys="handleNodeSelect"
  />
</template>

<style scoped>
/* 不使用 @apply */
.custom-tree :deep(.n-tree-node-content) {
  font-size: 0.875rem;
  color: rgb(82, 88, 102);
}
</style>
