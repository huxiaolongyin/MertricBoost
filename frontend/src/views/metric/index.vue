<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { onMounted, ref, watch } from 'vue';
import { fetchGetMetricList } from '@/service/api';
import { useAuth } from '@/hooks/business/auth';
import MetricCard from './modules/metric-card.vue';
import Search from './modules/search-filter.vue';
import MetricOperateDrawer from './modules/metric-operate-drawer.vue';

// 获取指标数据列表
const metricDataList = ref<Api.Metric.MetricData[]>([]);

const drawerVisible = ref<boolean>(false);

// 记录总条数
const totalCount = ref<number>(0);

const operateType = ref<NaiveUI.TableOperateType>('add');

const { hasAuth } = useAuth();
// 初始化搜索、筛选查询
const searchParams = ref<Api.Metric.MetricListSearchParams>({
  nameOrDesc: '',
  domainIds: [],
  tagIds: [],
  sensitivity: '',
  page: 1,
  pageSize: 12
});

// 定义指标
const metricForm = ref<Api.Metric.MetricUpdateParams>({});

// 定义点击指标卡片事件
const handleClickCard = (id: number) => {
  drawerVisible.value = true;
  operateType.value = 'edit';
  metricForm.value = metricDataList.value.filter(item => item.id === id)[0];
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

// 获取指标数据
const getMetricData = async () => {
  const response = await fetchGetMetricList({
    ...searchParams.value
  });
  metricDataList.value = response.data?.records ?? [];
  totalCount.value = response.data?.total ?? 0;
};

// 页面加载时获取指标数据列表
onMounted(async () => {
  getMetricData();
});

// 监听搜索参数的变化
watch(
  searchParams,
  async () => {
    getMetricData();
  },
  { deep: true }
);
</script>

<template>
  <div>
    <NFlex vertical :size="16" class="mt-5">
      <Search v-model:form-data="searchParams" />
      <MetricCard
        v-model:metric-data-list="metricDataList"
        v-model:search-params="searchParams"
        @click-id="handleClickCard"
      />
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
      v-if="hasAuth('metric-add')"
      :right="50"
      :bottom="60"
      shape="circle"
      width="60"
      height="60"
      class="bg-red-500"
      @click="drawerVisible = true"
    >
      <Icon icon="mdi:plus" class="text-white" width="35" height="35" />
    </NFloatButton>
    <MetricOperateDrawer
      v-model:visible="drawerVisible"
      :operate-type="operateType"
      :row-data="metricForm"
      @submitted="getMetricData"
    />
  </div>
</template>
