<template>
  <NFlex vertical gap="8px" align="center">
    <NDataTable :bordered="true" :single-line="false" :scroll-y="700" :data="dataModelFormStore.stepTwo.fieldConf ?? []"
      :columns="columns" :max-height="400" />
  </NFlex>
</template>

<script setup lang="tsx">
import { onMounted } from "vue";
import { fetchTableColumns } from "@/service/api";
import { useDataModelFormStore } from "@/store/modules/model";
import { NInput, NSelect } from "naive-ui";

// 获取数据模型表单状态存储内容
const dataModelFormStore = useDataModelFormStore();

// 定义传入参数
interface Props {
  operateType: NaiveUI.TableOperateType; 
}
const props = defineProps<Props>();

// 获取表的字段信息
const fetchColumns = async () => {
  if (!dataModelFormStore.stepOne.database || !dataModelFormStore.stepOne.tableName) {
    return;
  }
  const response = await fetchTableColumns({
    database: dataModelFormStore.stepOne.database,
    tableName: dataModelFormStore.stepOne.tableName,
    addOrEdit: props.operateType
  });
  
  dataModelFormStore.stepTwo.fieldConf = response.data?.records;
};

// 在组件挂载时获取表的字段信息
onMounted(async () => {
  // 如果数据为空，则获取表的字段信息
  if (!dataModelFormStore.stepTwo.fieldConf){
    await fetchColumns();
  }
});

// 定义显示数据的字段
const columns = [
  {
    key: "columnName",
    title: "字段名",
    width: 180,
  },
  {
    key: "columnComment",
    title: "字段描述",
    width: 180,
  },
  {
    key: "columnType",
    title: "字段类型",
    width: 150,
  },
  {
    key: 'semanticType',
    title: '语义类型',
    width: 180,
    render: (row: Api.SystemManage.TableColumns) => {
      return (
      <NSelect v-model:value={row.semanticType} options={semanticTypeOptions} placeholder="请选择语义类型" clearable onUpdate:value={(value) => {
        row.semanticType = value
      }}/>)}
    
  },
  {
    key: "aggregation",
    title: "聚合方式",
    width: 150,
    render: (row: Api.SystemManage.TableColumns) => {
      if (row.semanticType === 'metric') {
        return (<NSelect v-model:value={row.staticType} options={metricStaticOptions} placeholder="请选择统计方式" onUpdate:value={(value) => {
            row.staticType = value
          }}/>)
      }
    }
  },
  {
    key: "format",
    title: "格式",
    width: 180,
    render: (row: Api.SystemManage.TableColumns) => {
      if (row.semanticType === 'date') {
        return  (<NSelect v-model:value={row.format} options={dateFormatOptions} placeholder="请选择日期格式" onUpdate:value={(value) => {
            row.format = value
          }}/>)
  
      }
      else if (row.semanticType === 'metric') {
        return (<NSelect v-model:value={row.format} options={formatOptions} placeholder="请选择统计方式" onUpdate:value={(value) => {
            row.format = value
          }}/>)
      }
    }
  },
  {
    key: "extendedComputation",
    title: "扩展计算",
    width: 200,
    render: (row: Api.SystemManage.TableColumns) => {
      if (row.semanticType === 'metric') {
        return (<NInput v-model:value={row.extendedComputation}  placeholder="请输入扩展计算" onUpdate:value={(value) => {
            row.extendedComputation = value
          }}/>)
      }
    }
  },
];

const semanticTypeOptions = [
  { label: "日期", value: "date" },
  { label: "维度筛选", value: "dimension" },
  { label: "指标统计", value: "metric" },
  { label: "普通字段", value: "normal" },
];

const dateFormatOptions = [
  { label: "YYYY-MM-DD", value: "YYYY-MM-DD" },
  { label: "YYYY/MM/DD", value: "YYYY/MM/DD" },
  { label: "YYYY年MM月DD日", value: "YYYY年MM月DD日" },
];

const metricStaticOptions = [
  { label: "平均值", value: "avg" },
  { label: "最大值", value: "max" },
  { label: "最小值", value: "min" },
  { label: "总和", value: "sum" },
  { label: "计数", value: "count" }
]

const formatOptions = [
  { label: "数值", value: "number" },
  { label: "货币", value: "currency" },
  { label: "百分比", value: "percent" },
  { label: "流量", value: "flow" },
]
</script>
