<template>
  <!-- 搜索框 -->
  <div class="flex justify-center w-full">
    <NInput v-model:value="formData!.chineseName" :placeholder="$t('page.metric.metricPlaceholder')"
      class='my-3 h-10 rounded-xl dark:bg-slate-700 flex items-center' style="width: 65%">
      <template #suffix>
        <Icon icon="mdi:magnify" width="28" height="28" class="text-gray-500" />
      </template>
    </NInput>
  </div>
  <NGrid cols="s:1 m:2 l:4" responsive="screen" :x-gap="16" :y-gap="16">

    <!-- 主题域选择框 -->
    <NGi>
      <div class="flex items-center w-full mt-4">
        <div class="text-dark dark:text-white w-18 ml-8 justify-center">{{ $t("page.metric.topicDomain") }}</div>
        <NSelect v-model:value="formData!.topicDomain" :options="topicDomainOptions" placeholder="请选择主题域"
          :loading="topicDomainLoading" clearable class="dark:bg-slate-700" />
      </div>
    </NGi>
    数据服务
    <!-- 展示类型 -->
    <NGi>
      <div class="flex items-center w-full mt-4">
        <div class="text-dark dark:text-white w-20 ml-12 ">{{ $t("page.metric.displayStatus") }}</div>
        <NRadioGroup v-model:value="formData!.displayStatus">
          <NRadioButton v-for="item in OPTIONS_CONFIG.showType" :key='item.value' :value="item.value"
            :label="item.label" class="dark:bg-slate-700" />
        </NRadioGroup>
      </div>
    </NGi>

    <!-- 发布状态 -->
    <NGi>
      <div class="flex items-center w-full mt-4">
        <div class="text-dark dark:text-white w-20 ml-12 ">{{ $t("page.metric.publishStatus") }}</div>
        <NRadioGroup v-model:value="formData!.publishStatus">
          <NRadioButton v-for="item in OPTIONS_CONFIG.publish" :key='item.value' :value="item.value" :label="item.label"
            class="dark:bg-slate-700" />
        </NRadioGroup>
      </div>
    </NGi>

    <!-- 敏感度 -->
    <NGi>
      <div class="flex items-center w-full mt-4">
        <div class="text-dark dark:text-white w-20 ml-12 ">{{ $t("page.metric.sensitivity") }}</div>
        <NRadioGroup v-model:value="formData!.sensitivity">
          <NRadioButton v-for="item in OPTIONS_CONFIG.sensitive" :key='item.value' :value="item.value"
            :label="item.label" class="dark:bg-slate-700" />
        </NRadioGroup>
      </div>
    </NGi>
  </NGrid>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { OPTIONS_CONFIG } from '@/constants/options'
import { useLoadOptions } from '@/hooks/common/option'
import { fetchGetTopicDomainList } from "@/service/api";
import { $t } from '@/locales';
import { onMounted } from "vue";

// 定义“搜索”组件的选项
defineOptions({
  name: "Search",
})

// 设置模型和父组件的通信
const formData = defineModel<Api.Metric.MetricSearchParams>('formData');

// 获取主题域列表
const {
  options: topicDomainOptions,
  loading: topicDomainLoading,
  fetchOptions: fetchTopicDomainOptions
} = useLoadOptions(
  () => fetchGetTopicDomainList(),
  'domainName',
  'id')



// 定义按钮组的选项
interface RadioGroup {
  radiotitle: string
  radioType: keyof Api.Metric.MetricSearchParams | 'displayStatus'
  options: {
    value: string
    label: string
  }[]
}

const radioGroups: RadioGroup[] = [
  {
    radiotitle: '展示类型',
    radioType: 'displayStatus',
    options: OPTIONS_CONFIG.showType
  },
  {
    radiotitle: '是否发布',
    radioType: 'publishStatus',
    options: OPTIONS_CONFIG.publish
  },
  {
    radiotitle: '敏感度',
    radioType: 'sensitivity',
    options: OPTIONS_CONFIG.sensitive
  }
]
onMounted(async () =>
  await fetchTopicDomainOptions()
)
</script>
