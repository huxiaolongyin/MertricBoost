<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import * as XLSX from 'xlsx';
import { fetchGetMetricDetail } from '@/service/api';
import { useThemeStore } from '@/store/modules/theme';
import MetricChart from './modules/metric-chart.vue';
import MetricDetail from './modules/metric-detail.vue';
import MetricFilter from './modules/metric-filter.vue';
import MetricSidebar from './modules/metric-sidebar.vue';

// 通过路由参数获取 metric的 ID、item
const route = useRoute();
const id = Number.parseInt(route.params.id as string, 10);

// 获取主题配置
const themeStore = useThemeStore();
console.log();

// 跟踪当前激活的标签页
const activeTab = ref('chart');

// 获取指标数据
const metricData = ref<Api.Metric.MetricData>({} as Api.Metric.MetricData);
const isDataLoading = ref(false);

// 定义搜索表单模型
const searchDetailParams = ref<Api.Metric.MetricDetailSearchParams>({
  dateRange: null,
  statisticalPeriod: null,
  dimSelect: null,
  dimFilter: null
  // sort: "asc"
});

// 首先定义时间计算常量
const TIME_UNITS: Record<Api.Common.TimeType, number> = {
  daily: 24 * 60 * 60 * 1000,
  weekly: 7 * 24 * 60 * 60 * 1000,
  monthly: 30 * 24 * 60 * 60 * 1000,
  // "quarter": 90 * 24 * 60 * 60 * 1000,
  yearly: 365 * 24 * 60 * 60 * 1000,
  cumulative: 0
};

// 计算日期差值
const calculateDateDiff = (record: Api.Metric.MetricData) => {
  const statisticScope = record?.statisticScope ?? 1;
  const period: Api.Metric.StatisticalPeriod = record?.statisticalPeriod ?? 'daily';

  return statisticScope * (TIME_UNITS[period] || TIME_UNITS.daily);
};

// 获取指标数据
const fetchMetricData = async () => {
  isDataLoading.value = true;
  const { data } = await fetchGetMetricDetail({ id, ...searchDetailParams.value });
  const record = data?.records;
  metricData.value = record ?? ({} as Api.Metric.MetricData);

  // 设置日期范围
  if (searchDetailParams.value?.dateRange === null && record) {
    const diff = calculateDateDiff(record);
    const now = Date.now();
    searchDetailParams.value.dateRange = [now - diff, now];
  }

  // 设置统计周期
  if (searchDetailParams.value?.statisticalPeriod === null && record) {
    searchDetailParams.value.statisticalPeriod = record.statisticalPeriod;
  }
};

// 获取 grafana url
const grafanaUrl = computed(() => {
  const baseUrl = metricData.value?.url;
  if (!baseUrl || !searchDetailParams.value.dateRange) {
    return baseUrl;
  }

  try {
    const url = new URL(baseUrl);
    const [from, to] = searchDetailParams.value.dateRange;

    // 更新URL中的时间范围参数
    if (from) url.searchParams.set('from', Math.floor(from).toString());
    if (to) url.searchParams.set('to', Math.floor(to).toString());
    if (themeStore.darkMode) {
      url.searchParams.set('theme', 'dark');
    } else {
      url.searchParams.set('theme', 'light');
    }
    // 处理维度筛选参数
    if (searchDetailParams.value.dimFilter) {
      // 解析维度筛选字符串，格式如: "vin = 'HTWW312407A000020'"
      const filterStr = searchDetailParams.value.dimFilter[0];
      const match = filterStr.match(/(\w+)\s*=\s*['"]([^'"]+)['"]/);

      if (match && match.length >= 3) {
        const [, dimension, value] = match;
        // 将维度添加为Grafana模板变量，格式为 var-dimension=value
        url.searchParams.set(`var-${dimension}`, value);
      }
    }

    return url.toString();
  } catch (error) {
    console.error('Error parsing Grafana URL:', error);
    return baseUrl;
  }
});

// 添加导出Excel的功能
const exportToExcel = () => {
  if (!metricData.value?.data || metricData.value.data.length === 0) {
    window.$message?.warning('没有数据可导出');
    return;
  }

  // 创建一个工作簿
  const workbook = XLSX.utils.book_new();

  // 转换数据为工作表格式
  const worksheet = XLSX.utils.json_to_sheet(metricData.value.data);

  // 添加工作表到工作簿
  XLSX.utils.book_append_sheet(workbook, worksheet, '指标详情');

  // 确定文件名
  const fileName = `${metricData.value.metricName || '指标详情'}_${new Date().toISOString().slice(0, 10)}.xlsx`;

  // 导出Excel文件
  XLSX.writeFile(workbook, fileName);

  window.$message?.success('导出成功');
};

onMounted(async () => {
  await fetchMetricData();

  isDataLoading.value = false;
});

// 处理提交
const handleSubmit = async () => {
  fetchMetricData();
  isDataLoading.value = false;
};

// 处理维度筛选
const handleUpdate = () => {};

// 处理切换tab
const handleTabChange = (tabName: string) => {
  activeTab.value = tabName;
  if (tabName === 'chart') {
    handleSubmit();
  }
};
</script>

<template>
  <div>
    <NGrid cols="5">
      <NGi span="4">
        <MetricFilter
          v-model:metric-data="metricData"
          v-model:search-detail-params="searchDetailParams"
          @submit="handleSubmit"
          @update="handleUpdate"
        />
        <div v-if="metricData.chartType === 'grafana'" class="mt-2 px-6">
          <NCard class="rounded-xl bg-white dark:bg-slate-700">
            <div class="grafana-container">
              <iframe :src="grafanaUrl" width="100%" height="550" frameborder="0" allowfullscreen></iframe>
            </div>
          </NCard>
        </div>
        <div v-if="metricData.chartType !== 'grafana'" class="mt-2 px-6">
          <NCard class="rounded-xl bg-white dark:bg-slate-700" title="数据趋势">
            <template #header-extra>
              <NButton
                v-if="activeTab === 'detail'"
                type="primary"
                size="small"
                :disabled="!metricData?.data?.length"
                @click="exportToExcel"
              >
                导出Excel
              </NButton>
            </template>
            <NTabs type="line" animated @update:value="handleTabChange">
              <NTabPane name="chart" tab="图表">
                <MetricChart v-model:metric-data="metricData" />
              </NTabPane>
              <NTabPane name="detail" tab="详情">
                <MetricDetail
                  v-model:metric-data="metricData"
                  v-model:search-detail-params="searchDetailParams"
                  v-model:is-data-loading="isDataLoading"
                />
              </NTabPane>
            </NTabs>
          </NCard>
        </div>
      </NGi>
      <NGi>
        <MetricSidebar v-model:metric-data="metricData" />
      </NGi>
    </NGrid>
  </div>
</template>
