<template>
  <div>
    <NGrid cols="5">
      <NGi span="4">
        <MetricFilter v-model:metricData="metricData" v-model:searchParams="searchParams" @submit="handleSubmit"
          @update="handleUpdate" />
        <div class="px-6 mt-2">
          <NCard class="bg-white dark:bg-slate-700 rounded-xl " title="数据趋势">
            <NTabs type="line" animated @update:value="handleTabChange">
              <NTabPane name="chart" tab="图表">
                <MetricChart v-model:metricData="metricData" />
              </NTabPane>
              <NTabPane name="detail" tab="详情">
                <MetricDetail v-model:metricData="metricData" v-model:searchParams="searchParams"
                  v-model:isDataLoading="isDataLoading" />
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

<script setup lang="ts">
import { ref, onMounted } from "vue";
import MetricFilter from "./modules/metric-filter.vue";
import MetricChart from "./modules/metric-chart.vue";
import MetricDetail from "./modules/metric-detail.vue";
import MetricSidebar from "./modules/metric-sidebar.vue";
import { useRoute } from "vue-router";
import { fetchMetric } from "@/service/api";

// 通过路由参数获取 metric的 ID、item
const route = useRoute();
const id = parseInt(route.params.id as string);

// 获取指标数据
const metricData = ref<Api.Metric.MetricData>({} as Api.Metric.MetricData);
const isDataLoading = ref(false);

// 定义搜索表单模型
const searchParams = ref<Api.Metric.MetricSearchParams>({
  dateRange: null,
  statisticalPeriod: null,
  dimensionDrillDown: null,
  dimensionFilter: null,
  comparisonOperators: null,
  conditions: [],
  sort: "asc"
});

// 首先定义时间计算常量
const TIME_UNITS: Record<Api.Common.TimeType, number> = {
  "day": 24 * 60 * 60 * 1000,
  "week": 7 * 24 * 60 * 60 * 1000,
  "month": 30 * 24 * 60 * 60 * 1000,
  // "quarter": 90 * 24 * 60 * 60 * 1000,
  "year": 365 * 24 * 60 * 60 * 1000
};

// 计算日期差值
const calculateDateDiff = (record: any) => {
  const displayDate = record?.chartDisplayDate ?? 1;
  const period: Api.Common.TimeType = record?.statisticalPeriod ?? 'day';

  return displayDate * (TIME_UNITS[period] || TIME_UNITS.day);
};

// 获取指标数据
const fetchMetricData = async () => {
  isDataLoading.value = true;
  const { data } = await fetchMetric({ id: id, ...searchParams.value });
  metricData.value = data?.records[0] ?? {} as Api.Metric.MetricData;

  // 设置日期范围
  if (searchParams.value?.dateRange == null && data?.records?.[0]) {
    const diff = calculateDateDiff(data.records[0]);
    const now = Date.now();
    searchParams.value.dateRange = [now - diff, now];
  }

  // 设置统计周期
  if (searchParams.value?.statisticalPeriod == null && data?.records?.[0]) {
    searchParams.value.statisticalPeriod = data.records[0].statisticalPeriod;
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
const handleUpdate = () => { };

// 处理切换tab
const handleTabChange = (tabName: string) => {
  if (tabName === 'chart') {
    handleSubmit()
  }
}
</script>
