<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { onMounted, ref, watch } from 'vue';
import { $t } from '@/locales';
import { fetchAddMetric, fetchGetMetricList } from '@/service/api';
import MetricInfo from '../metric-exploration/modules/metric-info.vue';
import MetricCard from './modules/metric-card.vue';
import Search from './modules/search-filter.vue';

// 获取指标数据列表
const metricDataList = ref<Api.Metric.MetricData[]>([]);

// 定义模态框显示
const infoShow = ref(false);

// 记录总条数
const totalCount = ref<number>(0);

// 初始化搜索、筛选查询
const searchParams = ref<Api.Metric.MetricListSearchParams>({
  nameOrDesc: '',
  domainIds: [],
  tagIds: [],
  sensitivity: null,
  page: 1,
  pageSize: 12
});

// 定义新增指标表单
const metricAddForm = ref<Api.Metric.MetricUpdateParams>({
  id: null,
  metricName: '',
  metricDesc: '',
  dataModelId: null,
  statisticalPeriod: null,
  statisticScope: null,
  chartType: null,
  sensitivity: null
  // domainIds: [],
});

// 获取指标数据列表
const fetchMetricWithSearch = async (metircSearchParams: Api.Metric.MetricListSearchParams) => {
  const response = await fetchGetMetricList({
    ...metircSearchParams
  });
  return response;
};

// 跳转到新增指标页面
const handleSubmit = () => {
  fetchAddMetric(metricAddForm.value);
  window.$message?.success($t('common.addSuccess'));
  infoShow.value = false;
};

// 分页相关事件处理
const handlePageChange = (page: number) => {
  if (searchParams.value) {
    searchParams.value.page = page;
  }
};

// 每页条数变化事件处理
const handlePageSizeChange = (pageSize: number) => {
  if (searchParams.value) {
    searchParams.value.pageSize = pageSize;
  }
};
// 页面加载时获取指标数据列表
onMounted(async () => {
  const response = await fetchMetricWithSearch(searchParams.value);
  metricDataList.value = response.data?.records ?? [];
  totalCount.value = response.data?.total ?? 0;
});

// 监听搜索参数的变化
watch(
  searchParams,
  async newParams => {
    const response = await fetchMetricWithSearch(newParams);
    metricDataList.value = response.data?.records ?? [];
    totalCount.value = response.data?.total ?? 0;
  },
  { deep: true }
);
</script>

<template>
  <div>
    <NFlex vertical :size="16" class="mt-5">
      <Search v-model:form-data="searchParams" />
      <MetricCard v-model:metric-data-list="metricDataList" v-model:search-params="searchParams" />
      <div class="mt-4 flex justify-center">
        <NPagination
          v-model:page="searchParams.page"
          v-model:page-size="searchParams.pageSize"
          :item-count="totalCount"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </div>
    </NFlex>

    <!-- 分页控件 - 绝对定位在底部 -->
    <NFloatButton
      :right="50"
      :bottom="60"
      shape="circle"
      width="60"
      height="60"
      class="bg-red-500"
      @click="infoShow = true"
    >
      <Icon icon="mdi:plus" class="text-white" width="35" height="35" />
    </NFloatButton>
    <NDrawer v-model:show="infoShow" :width="800">
      <NDrawerContent>
        <template #header>新增指标</template>
        <template #footer>
          <NButton class="px-6" type="primary" @click="handleSubmit">提交</NButton>
        </template>
        <MetricInfo v-model:metric-data="metricAddForm" />
      </NDrawerContent>
    </NDrawer>
  </div>
</template>
