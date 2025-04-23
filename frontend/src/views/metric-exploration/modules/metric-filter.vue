<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { SelectOption } from 'naive-ui';
import { reactive, ref, watch } from 'vue';

// 定义组件的名称
defineOptions({
  name: 'MetricFilter'
});

// 使用一个对象管理过滤条件
const filter = reactive<{
  dim: string | null;
  operator: string | null;
  value: string | null;
}>({
  dim: null,
  operator: null,
  value: null
});

// 双向绑定数据
const metricData = defineModel<Api.Metric.MetricData>('metricData', { required: true });
const searchDetailParams = defineModel<Api.Metric.MetricDetailSearchParams>('searchDetailParams', { required: true });

// 添加维度筛选options
const FilterOptions: SelectOption[] = [
  { label: '=', value: '=' },
  { label: '!=', value: '!=' },
  { label: 'IN', value: 'in' },
  { label: 'NOT IN', value: 'not in' }
];

// 添加统计周期筛选options
const StatisticalPeriodOptions: SelectOption[] = [
  { label: '日', value: 'daily' },
  { label: '周', value: 'weekly' },
  // { label: "季度", value: "quarter" },
  { label: '月', value: 'monthly' },
  { label: '年', value: 'yearly' }
];

// 升序或者降序
const sortOptions: SelectOption[] = [
  { label: '升序', value: 'ASC' },
  { label: '降序', value: 'DESC' }
];

// 添加维度筛选框
const conditionOptions = ref<SelectOption[]>([]);

// 设置上传提交事件
const emit = defineEmits<{
  (e: 'submit'): void;
  //  (e: "update"): void
}>();

const handleClick = () => {
  emit('submit');
};

// const handleUpdate = () => {
//     emit("update");
// };

// // 增加维度选项组，todo
// const handleAddGroup = () => { };

// 监听filter的变化，更新searchDetailParams.dimFilter
watch(
  filter,
  newFilter => {
    // 处理维度选择变化，更新条件选项
    if (newFilter.dim && metricData.value?.dimData) {
      let found = false;
      // 查找选中维度的数据
      for (const item of metricData.value.dimData) {
        // 检查当前项是否包含选中维度作为键
        if (newFilter.dim in item) {
          // 将维度值转换为SelectOption格式，使用Set去重
          const values = item[newFilter.dim as keyof typeof item] as string[];
          const uniqueValues = [...new Set(values)];
          conditionOptions.value = uniqueValues.map(value => ({
            label: value,
            value
          }));
          found = true;
          break; // 找到匹配项后终止循环
        }
      }

      // 如果没有找到匹配的维度数据
      if (!found) {
        conditionOptions.value = [];
      }
    } else {
      conditionOptions.value = [];
    }

    // 处理筛选条件，更新dimFilter
    if (newFilter.dim && newFilter.operator && newFilter.value) {
      let valueStr;

      // 处理数组值的情况
      if (Array.isArray(newFilter.value)) {
        // 为数组中的每个字符串值添加单引号
        const quotedValues = newFilter.value.map(val => `'${val}'`);
        valueStr = quotedValues.join(',');

        // 对于IN和NOT IN操作符，加上括号
        if (newFilter.operator === 'in' || newFilter.operator === 'not in') {
          valueStr = `(${valueStr})`;
        }
      } else {
        // 为单个字符串值添加单引号
        valueStr = `'${newFilter.value}'`;
      }

      // 拼接成完整的筛选条件字符串
      searchDetailParams.value.dimFilter = [`${newFilter.dim} ${newFilter.operator} ${valueStr}`];
    } else {
      searchDetailParams.value.dimFilter = [];
    }
  },
  { deep: true }
);
</script>

<template>
  <div class="mt-2 px-6">
    <NCard class="rounded-xl bg-white dark:bg-slate-700">
      <NForm class="mt-3">
        <NFlex>
          <NFormItem label="日期区间：" label-placement="left" class="w-3/12">
            <NDatePicker v-model:value="searchDetailParams.dateRange" type="daterange" clearable />
          </NFormItem>
          <NFormItem label="统计周期：" label-placement="left" class="ml-5 w-2/12">
            <NSelect
              v-model:value="searchDetailParams.statisticalPeriod"
              :options="StatisticalPeriodOptions"
              clearable
            />
          </NFormItem>
        </NFlex>
        <NFormItem label="维度下钻：" label-placement="left" class="w-full">
          <NSelect
            v-model:value="searchDetailParams.dimSelect"
            class="w-3/12"
            :options="metricData.dimCols"
            clearable
          />
          <NSelect
            v-model:value="searchDetailParams.sort"
            class="ml-2 w-1/12"
            :options="sortOptions"
            placeholder="排名升降序"
            clearable
          />
          <div class="ml-5 w-full text-orange-600">（图表最多显示排名前10行数据）</div>
        </NFormItem>
        <NFormItem label="维度筛选：" label-placement="left">
          <NFlex :size="5" class="w-full">
            <NSelect v-model:value="filter.dim" class="w-2/12" clearable :options="metricData.dimCols" />
            <NSelect v-model:value="filter.operator" class="w-1/12" clearable :options="FilterOptions" />
            <NSelect
              v-model:value="filter.value"
              class="w-2/12"
              filterable
              clearable
              :multiple="filter.operator === 'in' || filter.operator === 'not in'"
              :options="conditionOptions"
            />
            <!--
 <NButton @click="handleAddGroup">
                            <Icon icon="material-symbols:add" />
                        </NButton> 
-->
            <NButton class="bg-sky-700 text-white" @click="handleClick">
              <Icon icon="material-symbols:search" class="mr-2" />
              查询
            </NButton>
          </NFlex>
        </NFormItem>
      </NForm>
    </NCard>
  </div>
</template>
