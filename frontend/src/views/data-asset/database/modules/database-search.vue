<script setup lang="ts">
import { $t } from '@/locales';
import { enableStatusOptions } from '@/constants/business';
import { translateOptions } from '@/utils/common';

defineOptions({
  name: 'DatabaseSearch'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.SystemManage.DatabaseSearchParams>('model', { required: true });

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
        <NFormItemGi span="24 s:12 m:6" :label="$t('page.dataAsset.database.databaseName')" path="databaseName"
          class="pr-24px">
          <NInput v-model:value="model.databaseName" :placeholder="$t('page.dataAsset.database.form.databaseName')" />
        </NFormItemGi>

        <NGi span="24 s:12 m:6" :label="$t('page.dataAsset.database.databaseType')" path="databaseType" class="pr-24px">
          <NInput v-model:value="model.databaseType" :placeholder="$t('page.dataAsset.database.form.databaseType')" />
        </NGi>

        <NFormItemGi span="24 s:12 m:6" :label="$t('page.dataAsset.database.createBy')" path="createBy" class="pr-24px">
          <NInput v-model:value="model.createBy" :placeholder="$t('page.dataAsset.database.form.createBy')" />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6" :label="$t('page.dataAsset.database.status')" path="status" class="pr-24px">
          <NSelect v-model:value="model.status" :placeholder="$t('page.dataAsset.database.form.status')"
            :options="translateOptions(enableStatusOptions)" clearable />
        </NFormItemGi>

        <NFormItemGi span="24 m:32" class="pr-24px">
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
