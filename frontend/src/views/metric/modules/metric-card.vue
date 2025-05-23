<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { h } from 'vue';
import { getFormattedValue } from '@/hooks/common/metric-format';
import { useRouterPush } from '@/hooks/common/router';
import { $t } from '@/locales';
import { fetchDeleteMetric, fetchGetMetricList } from '@/service/api';
import EChart from './echart-preview.vue';

defineOptions({
  name: 'MetricCard'
});

// 通过模型获取卡片数据
const metricDataList = defineModel<Api.Metric.MetricData[]>('metricDataList', {
  required: true
});
const searchParams = defineModel<Api.Metric.MetricListSearchParams>('searchParams', {
  required: true
});

const emit = defineEmits<{
  (e: 'clickId', id: number): void;
}>();

// 获取小数位数，设置金额、流量、百分数的小数位数为 2 ，其他为 0 位
const getDemicals = (FormatType: Api.Metric.FormatType) => {
  switch (FormatType) {
    case 'currency':
    case 'flow':
    case 'percent':
      return 2;
    default:
      return 0;
  }
};

// 获取后缀
const getSuffix = (FormatType: Api.Metric.FormatType) => {
  switch (FormatType) {
    case 'percent':
      return '%';
    case 'flow':
      return 'MB';
    default:
      return '';
  }
};

// 获取前缀
const getPrefix = (FormatType: Api.Metric.FormatType) => {
  return FormatType === 'currency' ? '￥' : '';
};

const getMenuOptions = (item: Api.Metric.MetricData) => [
  { label: '基本信息', key: 'metric-info' },
  {
    label: '指标探索',
    key: 'metric-exploration',
    disabled: item.statisticalPeriod === 'cumulative'
  },
  { label: '智能报告', key: 'metric-report', disabled: true },
  { label: 'API服务', key: 'metric-api', disabled: true },
  { label: () => h('span', { style: { color: 'red' } }, '删除'), key: 'delete' }
];

const handleSelect = (key: string, item: Api.Metric.MetricData) => {
  const { routerPushByKey } = useRouterPush(false);
  if (key === 'metric-info') {
    emit('clickId', item.id);
  } else if (key === 'metric-exploration') {
    routerPushByKey('metric-exploration', { params: { id: item.id.toString() } }).catch(error => {
      // eslint-disable-next-line no-console
      console.log('路由导航失败:', error);
      window.$message?.error('切换到指标探索页面失败，请刷新页面重试');
    });
  } else if (key === 'metric-report') {
    window.$message?.warning('开发中，敬请期待');
  } else if (key === 'metric-api') {
    window.$message?.warning('开发中，敬请期待');
  } else if (key === 'delete') {
    window.$dialog?.warning({
      title: '确认删除',
      content: '确定要删除该指标吗？',
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        // 执行删除逻辑
        const { error } = await fetchDeleteMetric({ id: item.id });
        if (error) {
          window.$message?.error(error.message);
          return;
        }
        window.$message?.success($t('common.deleteSuccess'));

        // 删除成功后，重新获取数据
        const { ...requestParams } = searchParams.value;
        const response = await fetchGetMetricList(requestParams);
        metricDataList.value = response.data?.records ?? [];
      }
    });
  }
};
</script>

<template>
  <NCard :bordered="false" class="h-[calc(55vh)] overflow-auto bg-transparent">
    <!-- 设置边距、大小、屏幕适应 -->
    <NGrid cols="s:1 m:2 l:4" responsive="screen" :x-gap="16" :y-gap="16">
      <NGi v-for="(item, index) in metricDataList" :key="item.id">
        <div class="h-38 rd-8px bg-white px-16px pb-4px pt-12px text-dark shadow-md dark:bg-slate-700 dark:text-white">
          <NGrid cols="2">
            <!-- 左侧 -->
            <NGi>
              <h3 class="text-16px">{{ item.metricName }}</h3>
              <div class="flex justify-between pt-12px">
                <!-- 添加动态的数字动画 -->
                <CountTo
                  v-if="metricDataList[index].chartType !== 'grafana'"
                  :start-value="0"
                  :end-value="getFormattedValue(item)"
                  :decimals="getDemicals(item.metricFormat)"
                  :suffix="getSuffix(item.metricFormat)"
                  :prefix="getPrefix(item.metricFormat)"
                  class="mb-4 text-26px font-semibold"
                />
                <CountTo
                  v-if="metricDataList[index].chartType === 'grafana'"
                  :start-value="0"
                  :end-value="0"
                  class="mb-4 text-26px font-semibold"
                />
              </div>
              <div class="tags">
                <span
                  v-for="tag in item.tags.slice(0, 3)"
                  :key="tag"
                  class="mr-2 rounded bg-slate-100 px-1 py-0.5 text-xs dark:bg-slate-500"
                >
                  {{ tag }}
                </span>
                <span
                  v-if="item.tags.length > 3"
                  class="mr-2 cursor-pointer rounded bg-slate-100 px-1 py-0.5 text-xs dark:bg-slate-500"
                  :title="item.tags.slice(3).join(', ')"
                >
                  ...
                </span>
              </div>
            </NGi>

            <!-- 右侧 -->
            <NGi>
              <!-- 菜单栏 -->
              <div class="flex justify-end">
                <NDropdown
                  placement="bottom-end"
                  trigger="click"
                  :options="getMenuOptions(item)"
                  @select="key => handleSelect(key, item)"
                >
                  <Icon
                    icon="material-symbols:more-horiz"
                    width="24"
                    height="24"
                    class="text-slate-400 hover:text-slate-600"
                  />
                </NDropdown>
              </div>
              <div v-if="metricDataList[index].chartType === 'grafana'">
                <!-- 从本地加载图片 -->
                <img src="https://i.postimg.cc/6qXVNGGX/Snipaste-2025-05-22-11-06-45.png" alt="Grafana Chart" />
              </div>
              <!-- 图表 -->
              <EChart
                v-if="
                  metricDataList[index].chartType !== 'grafana' &&
                  metricDataList[index].statisticalPeriod !== 'cumulative'
                "
                v-model:metric-data="metricDataList[index]"
                class="metric-chart"
              />
            </NGi>
          </NGrid>
        </div>
      </NGi>
    </NGrid>
  </NCard>
</template>

<style scoped>
.search-input {
  width: 65%;
}

.metric-chart {
  width: 100%;
  height: 100px;
}
</style>
