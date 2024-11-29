<template>
  <NCard :bordered="false" class="bg-transparent">

    <!-- 设置边距、大小、屏幕适应 -->
    <NGrid cols="s:1 m:2 l:4" responsive="screen" :x-gap="16" :y-gap="16">
      <NGi v-for="(item, index) in metricDataList" :key="item.id">
        <div class="rd-8px px-16px pb-4px pt-12px text-dark dark:text-white shadow-md bg-white dark:bg-slate-700 h-38">
          <NGrid cols="2">
            <!-- 左侧 -->
            <NGi>
              <h3 class="text-16px">{{ item.chineseName }}</h3>
              <div class="flex justify-between pt-12px">
                <!-- 添加动态的数字动画 -->
                <CountTo :start-value="0" :end-value="getFormattedValue(item)" :decimals="getDemicals(item.formatType)"
                  :suffix="getSuffix(item.formatType)" :prefix="getPrefix(item.formatType)"
                  class="text-26px font-semibold mb-4" />
              </div>
              <div class="tags">
                <span class="bg-slate-100 dark:bg-slate-500 px-4px py-1px mr-2 rounded" v-for="tag in item.tags"
                  :key="tag">{{ tag }}</span>
              </div>
            </NGi>

            <!-- 右侧 -->
            <NGi>
              <!-- 菜单栏 -->
              <div class="flex justify-end">
                <NDropdown placement="bottom-end" trigger="click" :options="menuOptions"
                  @select="(key) => handleSelect(key, item)">
                  <Icon icon="material-symbols:more-horiz" width="24" height="24"
                    class="text-slate-400 hover:text-slate-600" />
                </NDropdown>
              </div>

              <!-- 图表 -->
              <EChart v-model:metricData="metricDataList[index]" style="width: 100%; height: 100px;" />
            </NGi>
          </NGrid>
        </div>
      </NGi>
    </NGrid>
  </NCard>
</template>
<script setup lang="ts">

import EChart from "./echart-preview.vue";
import { Icon } from "@iconify/vue";
import { fetchDeleteMetric, fetchMetric } from "@/service/api"
import { useRouterPush } from '@/hooks/common/router';
import { getFormattedValue } from '@/hooks/common/metric-format';
import { h } from 'vue'
import { $t } from "@/locales";

defineOptions({
  name: "MetricCard",
});

// 通过模型获取卡片数据
const metricDataList = defineModel<Api.Metric.MetricData[]>('metricDataList', { required: true })
const searchParams = defineModel<Api.Metric.MetricSearchParams>('searchParams', { required: true })

// 获取小数位数，设置金额、流量、百分数的小数位数为 2 ，其他为 0 位
const getDemicals = (FormatType: Api.Metric.FormatType) => {
  switch (FormatType) {
    case "currency":
    case "flow":
    case "percent":
      return 2;
    default:
      return 0;
  }
};

// 获取后缀
const getSuffix = (FormatType: Api.Metric.FormatType) => {
  switch (FormatType) {
    case "percent":
      return "%";
    case "flow":
      return "MB";
    default:
      return "";
  }
};

// 获取前缀
const getPrefix = (FormatType: Api.Metric.FormatType) => {
  return (FormatType === "currency" ? "￥" : "");
};

const menuOptions = [
  { label: '指标探索', key: "metric-exploration" },
  { label: '发布分享', key: "metric-publish" },
  { label: '生成报告', key: "metric-report" },
  { label: 'AI 分析', key: "metric-ai" },
  { label: "加入收藏", key: "saveToFavorites" },
  { label: () => h('span', { style: { color: 'red' } }, '删除'), key: "delete", }
]

const handleSelect = (key: string, item: Api.Metric.MetricData) => {
  const { routerPushByKey } = useRouterPush(false);
  if (key === "metric-exploration") {
    routerPushByKey("metric-exploration", { params: { id: item.id.toString() } });
  }
  else if (key === "metric-publish") {
    routerPushByKey("metric-publish", { params: { id: item.id.toString() } });
  }
  else if (key === "metric-report") {
    routerPushByKey("metric-report", { params: { id: item.id.toString() } });
  }
  else if (key === "metric-ai") {
    routerPushByKey("metric-ai", { params: { id: item.id.toString(), } });
  }
  else if (key === 'delete') {
    window.$dialog?.warning({
      title: '确认删除',
      content: '确定要删除该指标吗？',
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        // 执行删除逻辑
        const { error } = await fetchDeleteMetric({ id: item.id });
        if (error) {
          window.$message?.error(error.message)
          return
        }
        window.$message?.success($t('common.deleteSuccess'))

        // 删除成功后，重新获取数据
        const { displayStatus, ...requestParams } = searchParams.value;
        const response = await fetchMetric(requestParams);
        metricDataList.value = response.data?.records ?? [];
      }
    })
    return
  }
}


</script>
