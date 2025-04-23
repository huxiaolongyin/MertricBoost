<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { onMounted } from 'vue';
import { orderOptions, sensitiveOptions } from '@/constants/options';
import { useLoadOptions } from '@/hooks/common/option';
import { $t } from '@/locales';
import { fetchGetDomainList, fetchGetTagList } from '@/service/api';
// 定义“搜索”组件的选项
defineOptions({
  name: 'SearchFilter'
});

// 设置模型和父组件的通信
const formData = defineModel<Api.Metric.MetricListSearchParams>('formData');

// 获取主题域列表
const {
  options: domainOptions,
  loading: domainLoading,
  fetchOptions: fetchDomainOptions
} = useLoadOptions(() => fetchGetDomainList(), {
  labelKey: 'domainName',
  valueKey: 'id'
});

// 获取标签列表
const {
  options: tagOptions,
  loading: tagLoading,
  fetchOptions: fetchTagOptions
} = useLoadOptions(() => fetchGetTagList(), {
  labelKey: 'tagName',
  valueKey: 'id'
});

onMounted(async () => {
  await fetchDomainOptions();
  await fetchTagOptions();
});
</script>

<template>
  <!-- 搜索框 -->
  <div class="w-full flex justify-center">
    <NInput
      v-model:value="formData!.nameOrDesc"
      :placeholder="$t('page.metric.metricPlaceholder')"
      class="search-input my-3 h-10 flex items-center rounded-xl dark:bg-slate-700"
    >
      <template #suffix>
        <Icon icon="mdi:magnify" width="28" height="28" class="text-gray-500" />
      </template>
    </NInput>
  </div>
  <NGrid cols="s:1 m:2 l:4" responsive="screen" :x-gap="16" :y-gap="16">
    <!-- 域选择框 -->
    <NGi>
      <div class="mt-4 w-full flex items-center">
        <div class="ml-8 w-18 justify-center text-dark dark:text-white">
          {{ $t('page.metric.domain') }}
        </div>
        <NSelect
          v-model:value="formData!.domainIds"
          multiple
          :options="domainOptions"
          placeholder="请选择域分类"
          :loading="domainLoading"
          clearable
          class="dark:bg-slate-700"
        />
      </div>
    </NGi>

    <!-- 标签类型 -->
    <NGi>
      <div class="mt-4 w-full flex items-center">
        <div class="ml-8 w-18 justify-center text-dark dark:text-white">
          {{ $t('page.metric.tag') }}
        </div>
        <NSelect
          v-model:value="formData!.tagIds"
          multiple
          :options="tagOptions"
          placeholder="请选择标签"
          :loading="tagLoading"
          clearable
          class="w-3/4 dark:bg-slate-700"
        />
      </div>
    </NGi>

    <!-- 敏感度 -->
    <NGi>
      <div class="mt-4 w-full flex items-center">
        <div class="ml-12 w-20 text-dark dark:text-white">
          {{ $t('page.metric.sensitivity') }}
        </div>
        <NRadioGroup v-model:value="formData!.sensitivity">
          <NRadioButton
            v-for="item in sensitiveOptions"
            :key="item.value"
            :value="item.value"
            :label="item.label"
            class="dark:bg-slate-700"
          />
        </NRadioGroup>
      </div>
    </NGi>

    <!-- 排序 -->
    <NGi>
      <div class="mt-4 w-full flex items-center">
        <div class="ml-8 w-18 justify-center text-dark dark:text-white">
          {{ $t('page.metric.order') }}
        </div>
        <NSelect
          v-model:value="formData!.order"
          :options="orderOptions"
          placeholder="请选择排序方式"
          clearable
          class="w-3/4 dark:bg-slate-700"
        />
      </div>
    </NGi>
  </NGrid>
</template>

<style scoped>
.search-input {
  width: 65%;
}
</style>
