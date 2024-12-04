<template>
  <NForm :rules="rules">
    <NFormItem :label="$t('page.dataAsset.dataModel.dataModelName')" path="dataModelName">
      <NInput v-model:value="dataModelFormStore.stepThree.dataModelName"
        :placeholder="$t('page.dataAsset.dataModel.form.dataModelName')" />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.dataModelDesc')" path="dataModelDesc">
      <NInput v-model:value="dataModelFormStore.stepThree.dataModelDesc"
        :placeholder="$t('page.dataAsset.dataModel.form.dataModelDesc')" />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.dataDomain')" path="dataDomain">
      <NSelect v-model:value="dataModelFormStore.stepThree.dataDomain"
        :placeholder="$t('page.dataAsset.dataModel.form.dataDomain')" :loading="dataDomainLoading"
        :options="dataDomainOptions" />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.topicDomain')" path="topicDomain">
      <NSelect v-model:value="dataModelFormStore.stepThree.topicDomain"
        :placeholder="$t('page.dataAsset.dataModel.form.topicDomain')" :loading="topicDomainLoading"
        :options="topicDomainOptions" />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.status')" path="status">
      <NRadioGroup v-model:value="dataModelFormStore.stepThree.status">
        <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="$t(item.label)" />
      </NRadioGroup>
    </NFormItem>
  </NForm>
</template>

<script setup lang="ts">
import { enableStatusOptions, } from '@/constants/business';
import { useDataModelFormStore } from "@/store/modules/model";
import { FormRules } from 'naive-ui';
import { useLoadOptions } from '@/hooks/common/option'
import { fetchGetTopicDomainList, fetchGetDataDomainList } from "@/service/api";

// 获取数据模型表单状态存储内容
const dataModelFormStore = useDataModelFormStore();

// 加载数据域列表
const {
  options: dataDomainOptions,
  loading: dataDomainLoading,
  fetchOptions: fetchDataDomainOptions
} = useLoadOptions(
  () => fetchGetDataDomainList(),
  'domainName',
  'id')
fetchDataDomainOptions()

// 加载主题域列表
const {
  options: topicDomainOptions,
  loading: topicDomainLoading,
  fetchOptions: fetchTopicDomainOptions
} = useLoadOptions(
  () => fetchGetTopicDomainList(),
  'domainName',
  'id')
fetchTopicDomainOptions()

const rules: FormRules = {
  dataModelName: {
    required: true,
    message: '请输入数据模型名称',
  },
  dataModelDesc: {
    required: true,
    message: '请输入数据模型的描述'
  },
  dataDomain: {
    required: true,
    message: '请选择数据域'
  },
  topicDomain: {
    required: true,
    message: '请选择主题域'
  },
  status: {
    required: true,
    message: '请选择数据模型的状态'
  }
}
</script>
