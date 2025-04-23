<script setup lang="ts">
import { apiMethodOptions, enableStatusOptions } from '@/constants/business';
import { useNaiveForm } from '@/hooks/common/form';
import { $t } from '@/locales';
import { translateOptions } from '@/utils/common';

defineOptions({
  name: 'ServiceApiSearch'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const { formRef, validate, restoreValidation } = useNaiveForm();

const model = defineModel<Api.DataService.ServiceApiSearchParams>('model', {
  required: true
});

async function reset() {
  await restoreValidation();
  emit('reset');
}

async function search() {
  await validate();
  emit('search');
}
</script>

<template>
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm ref="formRef" :model="model" label-placement="left" :label-width="80">
      <NGrid responsive="screen" item-responsive>
        <NFormItemGi span="24 s:12 m:6" :label="$t('page.service.serviceApi.apiName')" path="apiName" class="pr-24px">
          <NInput v-model:value="model.apiName" :placeholder="$t('page.service.serviceApi.form.apiName')" />
        </NFormItemGi>
        <NFormItemGi
          span="24 s:12 m:6"
          :label="$t('page.service.serviceApi.apiMethod')"
          path="apiMethod"
          class="pr-24px"
        >
          <NSelect
            v-model:value="model.apiMethod"
            :placeholder="$t('page.service.serviceApi.form.apiMethod')"
            :options="
              translateOptions(apiMethodOptions).filter(method => method.value === 'get' || method.value === 'post')
            "
            clearable
          />
        </NFormItemGi>
        <NFormItemGi
          span="24 s:12 m:6"
          :label="$t('page.service.serviceApi.metricName')"
          path="metricName"
          class="pr-24px"
        >
          <NSelect v-model:value="model.metricName" :placeholder="$t('page.service.serviceApi.form.metricName')" />
        </NFormItemGi>
        <NFormItemGi span="24 s:12 m:6" :label="$t('page.service.serviceApi.appName')" path="appName" class="pr-24px">
          <NInput v-model:value="model.appName" :placeholder="$t('page.service.serviceApi.form.appName')" />
        </NFormItemGi>
        <NFormItemGi span="24 s:12 m:6" :label="$t('page.service.serviceApi.status')" path="status" class="pr-24px">
          <NSelect
            v-model:value="model.status"
            :placeholder="$t('page.service.serviceApi.form.status')"
            :options="translateOptions(enableStatusOptions)"
            clearable
          />
        </NFormItemGi>
        <NFormItemGi span="24 m:16" class="pr-24px">
          <NSpace class="w-full" justify="end">
            <NButton @click="reset">
              <template #icon>
                <icon-ic-round-refresh class="text-icon" />
              </template>
              {{ $t('common.reset') }}
            </NButton>
            <NButton type="primary" ghost @click="search">
              <template #icon>
                <icon-ic-round-search class="text-icon" />
              </template>
              {{ $t('common.search') }}
            </NButton>
          </NSpace>
        </NFormItemGi>
      </NGrid>
    </NForm>
  </NCard>
</template>

<style scoped></style>
