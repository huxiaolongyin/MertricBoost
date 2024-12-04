<script setup lang="ts">
import { $t } from '@/locales';
import { enableStatusOptions } from '@/constants/business';
import { translateOptions } from '@/utils/common';

defineOptions({
  name: 'DataModelSearch'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.SystemManage.DataModelSearchParams>('model', { required: true });

function reset() {
  emit('reset');
}

function search() {
  emit('search');
}
</script>

<template>
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm :model="model" label-placement="left" :label-width="80">
      <NGrid responsive="screen" item-responsive>

        <NFormItemGi span="24 s:12 m:6" :label="$t('page.dataAsset.dataModel.dataModelName')" path="dataModelName"
          class="pr-24px">
          <NInput v-model:value="model.dataModelName"
            :placeholder="$t('page.dataAsset.dataModel.form.dataModelName')" />
        </NFormItemGi>
        <!-- 
        <NFormItemGi span="24 s:12 m:6" :label="$t('page.dataAsset.dataModel.dataDomain')" path="dataDomain"
          class="pr-24px">
          <NInput v-model:value="model.dataDomain" :placeholder="$t('page.dataAsset.dataModel.form.dataDomain')" />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6" :label="$t('page.dataAsset.dataModel.topicDomain')" path="topicDomain"
          class="pr-24px">
          <NInput v-model:value="model.topicDomain" :placeholder="$t('page.dataAsset.dataModel.form.topicDomain')" />
        </NFormItemGi> -->

        <NFormItemGi span="24 s:12 m:6" :label="$t('common.createBy')" path="createBy" class="pr-24px">
          <NInput v-model:value="model.createBy" :placeholder="$t('page.dataAsset.dataModel.form.createBy')" />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6" :label="$t('page.dataAsset.dataModel.status')" path="status" class="pr-24px">
          <NSelect v-model:value="model.status" :placeholder="$t('page.dataAsset.dataModel.form.status')"
            :options="translateOptions(enableStatusOptions)" clearable />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6">
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
