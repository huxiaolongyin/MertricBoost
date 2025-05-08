<script setup lang="ts">
import { NSelect } from 'naive-ui';
import { onMounted, ref } from 'vue';
import type { TreeSelectOption } from 'naive-ui';
import { $t } from '@/locales';
import { enableStatusOptions } from '@/constants/business';
import { translateOptions } from '@/utils/common';
import { collectOptions } from '@/constants/options';
import { fetchDatabaseList } from '@/service/api';

defineOptions({
  name: 'CollectSearch'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.Collect.CollectSearchParams>('model', {
  required: true
});

const targetTreeData = ref<TreeSelectOption[]>([]);

// 从后端获取数据源，并处理成树形结构
const createTreeData = async (): Promise<TreeSelectOption[]> => {
  const { data: databaseList } = await fetchDatabaseList();

  const databasesByType: Record<string, Api.SystemManage.Database[]> = {};
  if (databaseList?.records && Array.isArray(databaseList.records)) {
    databaseList.records.forEach(db => {
      if (!databasesByType[db.type]) {
        databasesByType[db.type] = [];
      }
      databasesByType[db.type].push(db);
    });
  }

  const treeData: TreeSelectOption[] = [];

  for (const type in databasesByType) {
    if (Object.hasOwn(databasesByType, type)) {
      const databases = databasesByType[type];
      const typeNode: TreeSelectOption = {
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

const getDatabase = async () => {
  targetTreeData.value = await createTreeData();
};

function reset() {
  emit('reset');
}

function search() {
  emit('search');
}

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
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm :model="model" label-placement="left" :label-width="60">
      <NGrid cols="30" responsive="screen" item-responsive>
        <NFormItemGi span="24 s:12 m:6" :label="$t('page.collect.name')" path="name" class="pr-16px">
          <NInput v-model:value="model.name" :placeholder="$t('page.collect.form.name')" />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6" :label="$t('page.collect.type')" path="type" class="pr-16px">
          <NSelect v-model:value="model.type" :placeholder="$t('page.collect.form.type')" :options="collectOptions" />
        </NFormItemGi>

        <NFormItemGi
          span="24 s:12 m:6"
          :label="$t('page.collect.targetDatabase')"
          path="targetDatabaseIds"
          class="pr-16px"
        >
          <NTreeSelect
            v-model:value="model.targetDatabaseIds"
            :placeholder="$t('page.collect.form.targetDatabase')"
            multiple
            :options="targetTreeData"
            clearable
          />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6" :label="$t('page.collect.status')" path="status" class="pr-16px">
          <NSelect
            v-model:value="model.status"
            :placeholder="$t('page.collect.form.status')"
            :options="translateOptions(enableStatusOptions)"
            clearable
          />
        </NFormItemGi>

        <NFormItemGi span="24 m:6" class="pr-16px">
          <NFlex class="w-full" justify="end">
            <NButton @click="reset">
              <template #icon>
                <icon-ic-round-refresh class="text-icon" />
              </template>
              {{ $t('common.reset') }}
            </NButton>
            <NButton type="primary" ghost @click="search">
              <template #icon>
                <icon-ic-round-search class="text-icon" />
              </template>
              {{ $t('common.search') }}
            </NButton>
          </NFlex>
        </NFormItemGi>
      </NGrid>
    </NForm>
  </NCard>
</template>

<style scoped></style>
