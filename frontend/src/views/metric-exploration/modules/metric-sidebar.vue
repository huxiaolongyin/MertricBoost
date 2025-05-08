<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { onMounted, ref, watch } from 'vue';
import { useLoadOptions } from '@/hooks/common/option';
import { fetchAddMetricTag, fetchDeleteMetricTag, fetchGetTagList } from '@/service/api';
import MetricOperateDrawer from '@/views/metric/modules/metric-operate-drawer.vue';

// 定义组件的名称
defineOptions({
  name: 'MetricSidebar'
});

// 双向同步模型
const model = defineModel<Api.Metric.MetricData>('metricData', { required: true });

// 定义基础信息显示
const drawerVisible = ref(false);

// 当选中数据库时加载表列表
const {
  options: tagOptions,
  // loading: tagLoading,
  fetchOptions: fetchTagOptions
} = useLoadOptions(() => fetchGetTagList(), { labelKey: 'tagName', valueKey: 'id' });

const filterOptions = () => {
  // 执行过滤操作
  tagOptions.value = tagOptions.value.filter(item => !model.value.tags.includes(item.label as string));
  // 将 tagOptions 中的 value 属性重命名为 key
  tagOptions.value = tagOptions.value.map(item => ({
    label: item.label,
    key: item.value
  }));
};

// 移除标签
const handleRemoveTag = async (tag: string) => {
  fetchDeleteMetricTag({
    metricId: model.value.id,
    tagName: tag
  });
  // 删除标签
  model.value.tags = model.value.tags.filter(t => t !== tag);
  await fetchTagOptions();
  // 执行过滤操作
  filterOptions();
};

// 添加指标标签
const handleAddTag = async (tagId: number) => {
  fetchAddMetricTag({
    metricId: model.value.id,
    tagId
  });
  // 添加标签
  model.value.tags.push(tagOptions.value.filter(item => item.key === tagId)[0].label as string);
  await fetchTagOptions();
  // 执行过滤操作
  filterOptions();
};

onMounted(async () => {
  await Promise.all([
    fetchTagOptions(),
    new Promise(resolve => {
      watch(
        () => model.value.tags,
        newTags => {
          if (newTags) {
            resolve(newTags);
          }
        },
        { immediate: true }
      );
    })
  ]);

  filterOptions();
});
</script>

<template>
  <NFlex vertical class="ml-5 mt-5 text-black" size="large">
    <div class="mb-3 text-xl font-semibold">{{ model.metricName }}</div>
    <NButtonGroup>
      <NPopover placement="bottom">
        <template #trigger>
          <NButton size="small" class="w-60">
            <template #icon>
              <Icon icon="mdi:fire" />
            </template>
            {{ model.queryCount }}
          </NButton>
        </template>
        查询热度
      </NPopover>
      <!--
 <NPopover placement="bottom">
        <template #trigger>
          <NButton size="small" class="w-40">
            <template #icon>
              <Icon icon="tabler:star" />
            </template>
            0
          </NButton>
        </template>
        点击收藏
      </NPopover> 
-->
    </NButtonGroup>
    <div>
      <div>版本</div>
      <div class="mt-1 text-gray">v1</div>
    </div>

    <div>
      <div class="font-medium">创建时间</div>
      <div class="mt-1 text-gray">{{ model.createTime }}</div>
    </div>
    <div>
      <div class="font-medium">创建人</div>
      <div class="mt-1 text-gray">{{ model.createBy }}</div>
    </div>
    <div>
      <div class="font-medium">上次更新时间</div>
      <div class="mt-1 text-gray">{{ model.updateTime }}</div>
    </div>
    <div>
      <div class="font-medium">更新人</div>
      <div class="mt-1 text-gray">{{ model.updateBy }}</div>
    </div>
    <NFlex align="center" size="small">
      <NPopover trigger="hover" :show-arrow="false" placement="bottom">
        <template #trigger>
          <span class="rounded bg-slate-200 py-1 pr-1 font-medium">基础信息</span>
        </template>
        <div>
          <div class="font-bold">基础信息</div>
          <NDivider class="section-divider" />
          <NGrid cols="3" :x-gap="12" :y-gap="12">
            <NGi :span="1">
              <NFlex vertical>
                <div class="font-medium">指标名：</div>
                <div class="font-medium">指标描述：</div>
                <div class="font-medium">选用模型：</div>
                <div class="font-medium">统计周期：</div>
                <div class="font-medium">统计范围：</div>
                <div class="font-medium">图表类型：</div>
                <div class="font-medium">敏感等级：</div>
                <div class="font-medium">指标显示：</div>
              </NFlex>
            </NGi>
            <NGi :span="2">
              <NFlex vertical>
                <div class="font-medium">{{ model.metricName }}</div>
                <div class="font-medium">{{ model.metricDesc }}</div>
                <div class="font-medium">{{ model.dataModelId }}</div>
                <div class="font-medium">{{ model.statisticalPeriod }}</div>
                <div class="font-medium">{{ model.statisticScope }}</div>
                <div class="font-medium">{{ model.chartType }}</div>
                <div class="font-medium">{{ model.sensitivity }}</div>
                <div class="font-medium">{{ model.metricFormat }}</div>
              </NFlex>
            </NGi>
          </NGrid>
        </div>
      </NPopover>
      <NButton quaternary size="tiny" @click="drawerVisible = true">
        <template #icon>
          <Icon icon="mynaui:edit" />
        </template>
      </NButton>
    </NFlex>
    <MetricOperateDrawer v-model:visible="drawerVisible" operate-type="edit" :row-data="metricData" />
    <div>
      <div class="font-medium">标签</div>
      <div class="mt-1 flex flex-wrap items-center">
        <span
          v-for="tag in model.tags"
          :key="tag"
          class="group relative mr-2 inline-flex items-center rounded bg-orange-50 px-4px py-1px text-amber-600 dark:bg-slate-500"
        >
          {{ tag }}
          <NPopconfirm positive-text="确定" negative-text="取消" @positive-click="handleRemoveTag(tag)">
            <template #trigger>
              <span
                class="absolute h-4 w-4 flex cursor-pointer items-center justify-center rounded-full bg-red-500 text-xs text-white opacity-0 transition-opacity -right-2 -top-2 group-hover:opacity-100"
              >
                ×
              </span>
            </template>
            确定要删除这个标签吗？
          </NPopconfirm>
        </span>
        <span class="inline-flex items-center">
          <NDropdown placement="bottom-start" trigger="click" size="small" :options="tagOptions" @select="handleAddTag">
            <NButton quaternary size="tiny" class="mr-2 rounded bg-slate-100 px-8px py-1px text-gray dark:bg-slate-500">
              <icon-ic:round-plus class="text-icon" />
            </NButton>
          </NDropdown>
        </span>
      </div>
    </div>
  </NFlex>
</template>

<style scoped>
/* Add this class definition (include your other classes if they exist) */
.section-divider {
  margin: 6px 0;
}
</style>
