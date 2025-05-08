<script setup lang="ts">
import type { SeriesOption } from 'echarts';
import type { CallbackDataParams } from 'echarts/types/dist/shared';
import { watch } from 'vue';
import { formatEchartDisplay } from '@/hooks/common/metric-format';
import { useEcharts } from '@/hooks/common/echarts';

// 双向绑定数据
const metricData = defineModel<Api.Metric.MetricData>('metricData', { required: false });

const { domRef, updateOptions } = useEcharts(() => ({}));

// 根据获取到的数据进行渲染 Echart 图表
// 如果只有 date + value，则只有单系列
// 如果有除上面以外的维度，超过1个，使用多系列处理。目前无更好方式处理超过2个及以上的情况
const renderChart = async () => {
  if (!metricData.value?.data || !Array.isArray(metricData.value.data) || metricData.value.data.length === 0) {
    // 如果没有数据，您可以在这里处理，或者直接返回
    return;
  }
  const data = metricData.value.data;

  // 获取所有去重日期作为 x 轴
  const xAxisData = [...new Set(data.map(item => item.date))];

  // 获取除 date、 value 之外的所有维度
  const dimensions = Object.keys(data[0] ?? {}).filter(key => key !== 'date' && key !== 'value');

  // 初步配置图表配置
  const chartOption = {
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    // 图表工具
    toolbox: {
      show: true,
      feature: {
        magicType: { show: true, type: ['line', 'bar'] },
        saveAsImage: { show: true }
      }
    },
    tooltip: {
      formatter: (params: CallbackDataParams[]) => {
        // 处理单系列数据
        if (params.length === 1) {
          return `${params[0].marker}${params[0].seriesName}: ${formatEchartDisplay[
            metricData.value?.metricFormat ?? 'default'
          ]((params[0].value ?? '-').toString())}`;
        }

        // 过滤掉非常小的值并排序
        const validParams = params
          .filter(item => Number(item.value) >= 0.0001)
          .sort((a, b) => Number(b.value) - Number(a.value));

        // 处理多系列数据
        const MAX_ROWS = 15;
        const columns = Math.ceil(validParams.length / MAX_ROWS);

        // 创建单个数据项的HTML
        const createItem = (item: CallbackDataParams) => `
      <div style="display:flex;justify-content:space-between;min-width:180px;gap:10px">
        <span>${item.marker}${item.seriesName}</span>
        <span>${formatEchartDisplay[metricData.value?.metricFormat ?? 'default']((item.value ?? '-').toString())}</span>
      </div>`;

        // 如果需要分列显示
        if (columns > 1) {
          const itemsPerColumn = Math.ceil(validParams.length / columns);
          const columnDivs = [];

          for (let i = 0; i < columns; i += 1) {
            const columnItems = validParams.slice(i * itemsPerColumn, (i + 1) * itemsPerColumn);
            columnDivs.push(`<div>${columnItems.map(createItem).join('')}</div>`);
          }

          return `<div style="display:flex;gap:20px">${columnDivs.join('')}</div>`;
        }

        // 单列显示
        return validParams.map(createItem).join('');
      },
      position: (point: number[], params: CallbackDataParams[]) => {
        // 如果是多维数据，固定位置
        if (params.length >= 2) {
          return [20, 20]; // 固定在左上角
        }

        // 单维度数据，跟随鼠标
        return [point[0] + 10, point[1]]; // 默认跟随鼠标，略微偏右
      },
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      }
    },
    xAxis: { type: 'category', data: xAxisData },
    yAxis: { type: 'value' },
    legend: {
      // selectedMode: 'single',
      textStyle: {
        fontSize: 12, // Set legend text size
        fontWeight: 'normal'
      }
    }, // 自动生成图例
    series: [] as SeriesOption[]
  };

  if (dimensions.length === 0) {
    // 单系列情况
    const seriesData = [
      {
        name: '数据',
        type: metricData.value.chartType || 'line',
        label: {
          show: true,
          position: 'top',
          formatter: (params: CallbackDataParams) =>
            formatEchartDisplay[metricData.value?.metricFormat ?? 'default']((params.value as string) ?? '-'), // Display the value
          fontSize: 12,
          color: '#666'
          // Optional: Format number with decimal places
          // formatter: (params) => params.value.toFixed(2)
        },
        data: data.map(item => item.value)
      }
    ];
    chartOption.series = seriesData;
  } else {
    // 多系列，根据第一个维度自动生成系列
    const dimensionName: string = dimensions[0]; // 使用第一个维度
    const dimensionValues = [...new Set(data.map(item => item[dimensionName]))]; // 获取维度的唯一值

    const seriesData = dimensionValues.map(dimValue => {
      const filteredData = data.filter(item => item[dimensionName] === dimValue);
      return {
        name: dimValue,
        type: metricData.value?.chartType || 'line',
        stack: 'Total',
        emphasis: {
          focus: 'series'
        },
        areaStyle: {},
        label: {
          show: false
          // show: true,
          // position: "right",
          // // formatter: '{c}', // Display the value
          // fontSize: 12,
          // color: '#666',
          // Optional: Format number with decimal places
          // formatter: (params) => params.value.toFixed(2)
        },
        data: xAxisData.map(date => {
          // Find matching data point for this date and dimension value
          const point = filteredData.find(item => item.date === date);
          return point ? point.value : 0;
        })
      };
    });
    chartOption.series = seriesData;
    // 更新图表
  }
  updateOptions(() => chartOption);
};

watch(() => metricData.value, renderChart);
</script>

<template>
  <div ref="domRef" class="chart-container h-full w-full"></div>
</template>

<style scoped>
.chart-container {
  height: 400px;
  width: 100%;
}
</style>
