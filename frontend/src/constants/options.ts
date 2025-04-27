import type { SelectOption } from 'naive-ui';
export const sensitiveOptions: SelectOption[] = [
  { value: '', label: '不限' },
  { value: '1', label: '普通' },
  { value: '2', label: '重要' },
  { value: '3', label: '核心' }
];

export const filteredSensitiveOptions = sensitiveOptions.filter(
  option => !(option.value === '' && option.label === '不限')
);

// 添加维度筛选options
export const filterOptions: SelectOption[] = [
  { label: '=', value: '=' },
  { label: '!=', value: '!=' },
  { label: 'IN', value: 'in' },
  { label: 'NOT IN', value: 'not in' }
];

// 添加统计周期筛选options
export const statisticalPeriodOptions: SelectOption[] = [
  { label: '日', value: 'daily' },
  { label: '周', value: 'weekly' },
  // { label: "季度", value: "quarter" },
  { label: '月', value: 'monthly' },
  { label: '年', value: 'yearly' },
  { label: '累计', value: 'cumulative' }
];

// 升序或者降序
export const sortOptions: SelectOption[] = [
  { label: '升序', value: 'ASC' },
  { label: '降序', value: 'DESC' }
];

// 图表类型
export const chartTypeOptions: SelectOption[] = [
  { label: '折线图', value: 'line' },
  { label: '柱状图', value: 'bar' }
];

// 统计类型
export const staticTypeOptions = [
  { label: '日期', value: 'date' },
  { label: '维度', value: 'dim' },
  { label: '指标', value: 'metric' },
  { label: '普通', value: 'none' }
];

// 日期类型
export const dateFormatOptions = [
  { label: 'YYYY-MM-DD', value: '%Y-%m-%d' },
  { label: 'YYYY/MM/DD', value: '%Y/%m/%d' },
  { label: 'YYYY年MM月DD日', value: '%Y年%m月%d日' }
];

// 指标类型
export const metricStaticOptions = [
  { label: '平均值', value: 'avg' },
  { label: '最大值', value: 'max' },
  { label: '最小值', value: 'min' },
  { label: '总和', value: 'sum' },
  { label: '计数', value: 'count' }
];

// 数值类型
export const metricFormatOptions = [
  { label: '数值', value: 'number' },
  { label: '货币', value: 'currency' },
  { label: '百分比', value: 'percent' },
  { label: '流量(MB)', value: 'flow' }
];

// 获取排序方式列表
export const orderOptions = [
  { label: '创建时间升序', value: 'create_time' },
  { label: '创建时间降序', value: '-create_time' }
];

//  数据库类型
export const databaseOptions: SelectOption[] = [
  {
    label: 'MySQL',
    value: 'MySQL'
  },
  {
    label: 'Oracle',
    value: 'Oracle'
  },
  {
    label: 'SQL Server',
    value: 'SQL Server'
  },
  {
    label: 'PostgreSQL',
    value: 'PostgreSQL'
  },
  {
    label: 'MongoDB',
    value: 'MongoDB'
  },
  {
    label: 'Redis',
    value: 'Redis'
  },
  {
    label: 'ClickHouse',
    value: 'ClickHouse'
  },
  {
    label: 'HBase',
    value: 'HBase'
  },
  {
    label: 'Hive',
    value: 'Hive'
  },
  {
    label: 'Elasticsearch',
    value: 'Elasticsearch'
  },
  {
    label: 'Kafka',
    value: 'Kafka'
  },
  {
    label: 'RabbitMQ',
    value: 'RabbitMQ'
  }
];
