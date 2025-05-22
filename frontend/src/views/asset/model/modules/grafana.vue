<script setup lang="ts">
import type { FormRules } from 'naive-ui';
import { useLoadOptions } from '@/hooks/common/option';
import { fetchDatabaseList, fetchGetDataDomainList, fetchGetTopicDomainList } from '@/service/api';
import { useDataModelFormStore } from '@/store/modules/model';
import { enableStatusOptions } from '@/constants/business';

defineOptions({
  name: 'Grafana'
});

// 获取数据模型表单状态存储内容
const dataModelFormStore = useDataModelFormStore();

// 加载非禁用的数据库列表
const {
  options: databaseOptions,
  loading: databaseLoading,
  fetchOptions: fetchdatabaseOptions
} = useLoadOptions(() => fetchDatabaseList({ status: '1', type: 'Grafana' }), {
  labelKey: 'name(type)',
  valueKey: 'id'
});

// 加载数据域列表
const {
  options: dataDomainOptions,
  loading: dataDomainLoading,
  fetchOptions: fetchDataDomainOptions
} = useLoadOptions(() => fetchGetDataDomainList(), {
  labelKey: 'domainName',
  valueKey: 'id'
});
fetchDataDomainOptions();

// 加载主题域列表
const {
  options: topicDomainOptions,
  loading: topicDomainLoading,
  fetchOptions: fetchTopicDomainOptions
} = useLoadOptions(() => fetchGetTopicDomainList(), {
  labelKey: 'domainName',
  valueKey: 'id'
});
fetchTopicDomainOptions();

const rules: FormRules = {
  database: {
    required: true,
    message: '请选择数据库'
    // trigger: ['input']
  },
  url: {
    required: true,
    message: '请输入url'
    // trigger: ['change'],
  },
  name: {
    required: true,
    message: '请输入数据模型名称'
  },
  description: {
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
};

fetchdatabaseOptions();
</script>

<template>
  <NForm :rules="rules">
    <NFormItem label="数据库" path="database">
      <NSelect
        v-model:value="dataModelFormStore.stepOne.databaseId"
        :placeholder="$t('page.dataAsset.dataModel.form.databaseSelect')"
        :options="databaseOptions"
        :loading="databaseLoading"
        clearable
      />
    </NFormItem>
    <NFormItem label="url(Grafana-分享-共享嵌入)" path="url">
      <NInput v-model:value="dataModelFormStore.grafana.url" />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.name')" path="name">
      <NInput
        v-model:value="dataModelFormStore.stepThree.name"
        :placeholder="$t('page.dataAsset.dataModel.form.name')"
      />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.description')" path="description">
      <NInput
        v-model:value="dataModelFormStore.stepThree.description"
        :placeholder="$t('page.dataAsset.dataModel.form.description')"
      />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.dataDomain')" path="dataDomains">
      <NSelect
        v-model:value="dataModelFormStore.stepThree.dataDomains"
        multiple
        :placeholder="$t('page.dataAsset.dataModel.form.dataDomain')"
        :loading="dataDomainLoading"
        :options="dataDomainOptions"
      />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.topicDomain')" path="topicDomains">
      <NSelect
        v-model:value="dataModelFormStore.stepThree.topicDomains"
        multiple
        :placeholder="$t('page.dataAsset.dataModel.form.topicDomain')"
        :loading="topicDomainLoading"
        :options="topicDomainOptions"
      />
    </NFormItem>
    <NFormItem :label="$t('page.dataAsset.dataModel.status')" path="status">
      <NRadioGroup v-model:value="dataModelFormStore.stepThree.status">
        <NRadio v-for="item in enableStatusOptions" :key="item.value" :value="item.value" :label="$t(item.label)" />
      </NRadioGroup>
    </NFormItem>
  </NForm>
</template>
