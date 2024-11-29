<template>
  <div>
    <NFlex vertical :size="16" class="mt-5">
      <Search v-model:formData="searchParams" />
      <MetricCard v-model:metricDataList="metricDataList" v-model:searchParams="searchParams" />
    </NFlex>
    <NFloatButton :right="50" :bottom="60" shape="circle" width="60" height="60" class="bg-red-500"
      @click="infoShow = true">
      <Icon icon="mdi:plus" class="text-white" width="35" height="35" />
    </NFloatButton>
    <NDrawer v-model:show="infoShow" :width="1000">
      <NDrawerContent>
        <template #header>
          新增指标
        </template>
        <template #footer>
          <NButton @click="handleSubmit" class="px-6" type="primary">提交</NButton>
        </template>
        <MetricInfo v-model:metric-data='metricAddForm' />
      </NDrawerContent>
    </NDrawer>
  </div>

</template>

<script setup lang="ts">
import Search from "./modules/search-filter.vue";
import MetricCard from "./modules/metric-card.vue";
import MetricInfo from '../metric-exploration/modules/metric-info.vue';
import { onMounted, ref, watch } from "vue";
import { fetchMetric, fetchAddMetric } from "@/service/api";
import { Icon } from "@iconify/vue";
import { useAuthStore } from '@/store/modules/auth';
import { $t } from '@/locales'

// 获取指标数据列表
const metricDataList = ref<Api.Metric.MetricData[]>([]);

// 定义模态框显示
const infoShow = ref(false);

// 初始化搜索、筛选查询
const searchParams = ref<Api.Metric.MetricSearchParams>({
  chineseName: "",
  sensitivity: '',
  displayStatus: '',
  favoritePerson: '',
  publishStatus: '',
  topicDomain: null,
  createBy: "",
  current: 1,
  size: 10
});


// 获取用户信息
const authStore = useAuthStore();

// 定义新增指标表单
const metricAddForm = ref<Api.Metric.MetricUpdateParams>({
  id: null,
  dataModel: null,
  businessScope: null,
  chineseName: null,
  englishName: null,
  alias: null,
  sensitivity: null,
  statisticalPeriod: null,
  chartType: null,
  chartDisplayDate: null,
  publishStatus: '2',
  createBy: authStore.userInfo.userName
});

// 获取指标数据列表
const fetchMetricWithSearch = async (searchParams: Api.Metric.MetricSearchParams) => {
  const response = await fetchMetric({
    ...searchParams
  });
  return response;
};

// 跳转到新增指标页面
const handleSubmit = () => {
  fetchAddMetric(metricAddForm.value);
  window.$message?.success($t('common.addSuccess'));
  infoShow.value = false;
};

// 页面加载时获取指标数据列表
onMounted(async () => {
  const { displayStatus, ...requestParams } = searchParams.value;
  const response = await fetchMetricWithSearch(requestParams);
  metricDataList.value = response.data?.records ?? [];
})

// 监听搜索参数的变化
watch(searchParams, async (newParams) => {
  const { displayStatus, ...requestParams } = newParams;
  const authStore = useAuthStore();
  if (displayStatus === '1') {
    // 获取当前用户信息
    newParams.createBy = authStore.userInfo.userName;
    newParams.favoritePerson = '';
  }
  else if (displayStatus === '2') {
    newParams.favoritePerson = authStore.userInfo.userName;
    newParams.createBy = '';
  }
  else {
    newParams.createBy = '';
    newParams.favoritePerson = '';
  }
  const response = await fetchMetricWithSearch(requestParams);
  metricDataList.value = response.data?.records ?? [];
}, { deep: true });

</script>
