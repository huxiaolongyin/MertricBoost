<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { fetchGetMetricDetail } from '@/service/api';
import MetricChart from './modules/metric-chart.vue';
import MetricDetail from './modules/metric-detail.vue';
import MetricFilter from './modules/metric-filter.vue';
import MetricSidebar from './modules/metric-sidebar.vue';

// 通过路由参数获取 metric的 ID、item
const route = useRoute();
const id = Number.parseInt(route.params.id as string, 10);

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
  yearly: 365 * 24 * 60 * 60 * 1000
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
        <div class="mt-2 px-6">
          <NCard class="rounded-xl bg-white dark:bg-slate-700" title="数据趋势">
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
