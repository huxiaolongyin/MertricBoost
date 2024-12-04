<template>
  <div class="text-black ml-5 h-14">
    <NRadioGroup
      size="small"
      v-model:value="dateSwitch"
      :theme-overrides="radioGroupthemeOverrides"
      @update:value="handleDateSwitch"
    >
      <NRadioButton value="date_picker" style="padding-left: 0px; padding-right: 0px">
        <NDatePicker
          clearable
          size="small"
          type="daterange"
          v-model:value="datePickerValue"
          :theme-overrides="datePickerthemeOverrides"
          :style="datePickerStyle"
          :on-confirm="handleDatePickerConfirm"
        />
      </NRadioButton>
      <NRadioButton value="today">今 天</NRadioButton>
      <NRadioButton value="last_7_days">近7天</NRadioButton>
      <NRadioButton value="last_30_days">近30天</NRadioButton>
    </NRadioGroup>
    <NGrid cols="5" class="mt-4">
      <NGi v-for="item in serviceMetricList" :key="item.name">
        <NFlex :size="1" align="center">
          <div>{{ item.name }}</div>
          <NTooltip>
            <template #trigger
              ><Icon icon="codicon:question" width="18" height="18"
            /></template>
            <span class="text-xs">{{ item.desc }}</span>
          </NTooltip>
        </NFlex>
        <div class="text-2xl font-medium my-3">{{ item.value }}</div>
      </NGi>
    </NGrid>
    <NGrid cols="2" class="mt-2" xGap="24" yGap="12">
      <NGi v-for="item in serviceDetailList" :key="item.title">
        <NFlex :size="1" align="center">
          <div>{{ item.title }}</div>
          <NTooltip>
            <template #trigger
              ><Icon icon="codicon:question" width="18" height="18"
            /></template>
            <span class="text-xs">{{ item.desc }}</span>
          </NTooltip>
        </NFlex>
        <RankEchart :labelList="item.labelList" :valueList="item.valueList" />
      </NGi>
    </NGrid>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Icon } from "@iconify/vue";
import RankEchart from "./modules/rankEchart.vue";
import { DatePickerProps, RadioGroupProps } from "naive-ui";

type ServiceMetric = {
  name: string;
  value: number;
  desc: string;
};
type ServiceMetricList = ServiceMetric[];

// 服务的指标数据
const serviceMetricList: ServiceMetricList = [
  {
    name: "累计已发布API数量",
    value: 100,
    desc: "累计处于已发布状态的API数量",
  },
  {
    name: "累计调用API数量",
    value: 100,
    desc: "累计处于已发布状态的API数量",
  },
  {
    name: "累计已发布API数量",
    value: 100,
    desc: "累计处于已发布状态的API数量",
  },
  {
    name: "累计已发布API数量",
    value: 100,
    desc: "累计处于已发布状态的API数量",
  },
  {
    name: "累计已发布API数量",
    value: 100,
    desc: "累计处于已发布状态的API数量",
  },
];

// 获取图表的数据
const serviceDetail: {
  title: string;
  desc: string;
  labelList: Array<string>;
  valueList: Array<number>;
} = {
  title: "API调用TOP10",
  desc: "已发布的API中，调用排名前10的API",
  labelList: [
    "0001",
    "0002",
    "0003",
    "0004",
    "0005",
    "0006",
    "0007",
    "0008",
    "0009",
    "0010",
  ],
  valueList: [730, 801, 924, 1259, 1600, 411, 1090, 888, 466, 877],
};

// 设置日期选择器的圆角
const serviceDetailList = [serviceDetail, serviceDetail, serviceDetail];
type DatePickerThemeOverrides = NonNullable<DatePickerProps["themeOverrides"]>;
const datePickerthemeOverrides: DatePickerThemeOverrides = {
  peers: {
    Input: {
      borderRadius: "0px",
    },
  },
};

// 设置单选按钮组的圆角
type RadioGroupThemeOverrides = NonNullable<RadioGroupProps["themeOverrides"]>;
const radioGroupthemeOverrides: RadioGroupThemeOverrides = {
  buttonBorderRadius: "0px",
};

const datePickerValue = ref<[number, number]>();
// 设置单选按钮组的点击触发
const dateSwitch = ref("");
const handleDateSwitch = (value: string) => {
  dateSwitch.value = value;
  if (value !== "date_picker") {
    datePickerStyle.value = defaultStyle;
  }
  if (value === "today") {
    datePickerValue.value = [Date.now(), Date.now()];
  }
  if (value === "last_7_days") {
    datePickerValue.value = [Date.now() - 7 * 24 * 60 * 60 * 1000, Date.now()];
  }
  if (value === "last_30_days") {
    datePickerValue.value = [Date.now() - 30 * 24 * 60 * 60 * 1000, Date.now()];
  }
};
// 设置日期选择器的点击触发
// 默认边框样式
const defaultStyle = {
  width: "100%", // 设置宽度
  marginTop: "-1px",
  border: "1px  #dcdfe6",
};
const datePickerStyle = ref(defaultStyle);
const handleDatePickerConfirm = () => {
  dateSwitch.value = "date_picker";
  datePickerStyle.value = {
    width: "100%", // 设置宽度
    marginTop: "-2px",
    border: "1px solid #646CFF", // 默认边框样式
  };
};
</script>

<style scoped></style>
