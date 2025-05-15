<script setup lang="tsx">
import { NInput, NSelect } from 'naive-ui';
import { onMounted } from 'vue';
import { fetchTableColumns } from '@/service/api';
import { useDataModelFormStore } from '@/store/modules/model';
import { dateFormatOptions, metricFormatOptions, metricStaticOptions, staticTypeOptions } from '@/constants/options';
defineOptions({
  name: 'ModelStep2'
});

// 获取数据模型表单状态存储内容
const dataModelFormStore = useDataModelFormStore();

// 定义传入参数
interface Props {
  operateType: NaiveUI.TableOperateType;
}
const props = defineProps<Props>();

// 获取表的字段信息
const fetchColumns = async () => {
  if (!dataModelFormStore.stepOne.databaseId || !dataModelFormStore.stepOne.tableName) {
    return;
  }
  const response = await fetchTableColumns({
    databaseId: dataModelFormStore.stepOne.databaseId,
    tableName: dataModelFormStore.stepOne.tableName,
    editMode: props.operateType
  });

  dataModelFormStore.stepTwo.columnsConf = response.data?.records;
};

// 在组件挂载时获取表的字段信息
onMounted(async () => {
  // 如果数据为空，则获取表的字段信息
  if (!dataModelFormStore.stepTwo.columnsConf) {
    await fetchColumns();
  }
});

// 定义显示数据的字段
const columns = [
  {
    key: 'columnName',
    title: '字段名',
    width: 180
  },
  {
    key: 'columnComment',
    title: '字段描述',
    width: 180
  },
  {
    key: 'columnType',
    title: '字段类型',
    width: 150
  },
  {
    key: 'staticType',
    title: '语义类型',
    width: 180,
    render: (row: Api.SystemManage.TableColumns) => {
      return (
        <NSelect
          v-model:value={row.staticType}
          options={staticTypeOptions}
          placeholder="请选择语义类型"
          clearable
          onUpdate:value={value => {
            row.staticType = value;
          }}
        />
      );
    }
  },
  {
    key: 'aggMethod',
    title: '聚合方式',
    width: 150,
    render: (row: Api.SystemManage.TableColumns) => {
      if (row.staticType === 'metric') {
        return (
          <NSelect
            v-model:value={row.aggMethod}
            options={metricStaticOptions}
            placeholder="请选择统计方式"
            onUpdate:value={value => {
              row.aggMethod = value;
            }}
          />
        );
      }
      return null; // 添加明确的返回值
    }
  },

  // 格式列
  {
    key: 'format',
    title: '格式',
    width: 180,
    render: (row: Api.SystemManage.TableColumns) => {
      if (row.staticType === 'date') {
        return (
          <NSelect
            v-model:value={row.format}
            options={dateFormatOptions}
            placeholder="请选择日期格式"
            onUpdate:value={value => {
              row.format = value;
            }}
          />
        );
      } else if (row.staticType === 'metric') {
        return (
          <NSelect
            v-model:value={row.format}
            options={metricFormatOptions}
            placeholder="请选择指标格式"
            onUpdate:value={value => {
              row.format = value;
            }}
          />
        );
      }
      return null; // 添加明确的返回值
    }
  },
  // 扩展计算列
  {
    key: 'extendedComputation',
    title: '扩展计算',
    width: 200,
    render: (row: Api.SystemManage.TableColumns) => {
      if (row.staticType === 'metric' || row.staticType === 'filter') {
        return (
          <NInput
            v-model:value={row.extraCaculate}
            placeholder="请输入扩展计算"
            onUpdate:value={value => {
              row.extraCaculate = value;
            }}
          />
        );
      }
      return null; // 添加明确的返回值
    }
  }
];
</script>

<template>
  <NFlex vertical gap="8px" align="center">
    <NDataTable
      :bordered="true"
      :single-line="false"
      :scroll-y="700"
      :data="dataModelFormStore.stepTwo.columnsConf ?? []"
      :columns="columns"
      :max-height="400"
    />
  </NFlex>
</template>
