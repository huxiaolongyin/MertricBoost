<template>
  <NCard>
    <div ref="domRef" class="h-360px overflow-hidden"></div>
  </NCard>
</template>

<script setup lang="ts">
import { useEcharts } from "@/hooks/common/echarts";
import * as echarts from "echarts/core";
import { onMounted } from "vue";


const props = defineProps({
  labelList: Array<string>,
  valueList: Array<number>,
});

const { domRef, updateOptions } = useEcharts(() => ({
  // title: {
  //   text: "排行榜top10",
  // },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  grid: {
    left: "2%",
    right: "3%",
    bottom: "0%",
    top: "0%",
    containLabel: true,
  },
  xAxis: {
    type: "value",
    axisLine: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    //不显示X轴刻度线和数字
    splitLine: { show: false },
    axisLabel: { show: false },
  },
  yAxis: {
    type: "category",
    data: [] as Array<string>,
    //升序
    inverse: true,
    splitLine: { show: false },
    axisLine: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    //key和图间距
    offset: 10,
    //动画部分
    animationDuration: 300,
    animationDurationUpdate: 300,
    //key文字大小
    nameTextStyle: {
      fontSize: 5,
    },
  },
  series: [
    {
      //柱状图自动排序，排序自动让Y轴名字跟着数据动
      realtimeSort: true,
      name: "数量",
      type: "bar",
      data: [] as Array<number>,
      barWidth: 14,
      barGap: 10,
      smooth: true,
      valueAnimation: true,
      //Y轴数字显示部分
      label: {
        show: true,
        position: "right",
        valueAnimation: true,
        offset: [5, -2],
        color: "#333",
        fontSize: 13,
      },
      emphasis: {
        itemStyle:
          { borderRadius: 7, }
      },
      itemStyle: {
        //颜色样式部分
        borderRadius: 7,
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: "#3977E6" },
          { offset: 1, color: "#37BBF8" },
        ]),
      },
    },
  ],
}));

onMounted(async () => {
  await new Promise((resolve) => {
    setTimeout(resolve, 1000);
  });

  updateOptions((opts) => {
    opts.yAxis.data = props.labelList ?? [];
    opts.series[0].data = props.valueList ?? [];
    return opts;
  });
});
</script>
