<script setup lang="ts">
import { $t } from '@/locales';
import { enableStatusOptions } from '@/constants/business';
import { translateOptions } from '@/utils/common';

defineOptions({
  name: 'AppSearch'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.DataService.ServiceAppSearchParams>('model', {
  required: true
});

function reset() {
  emit('reset');
}

function search() {
  emit('search');
}
</script>

<template>
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm :model="model" label-placement="left" :label-width="70">
      <NGrid cols="30" responsive="screen" item-responsive>
        <NFormItemGi span="24 s:12 m:6" label="App名称" path="appName" class="pr-16px">
          <NInput v-model:value="model.appName" />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6" label="状态" path="status" class="pr-16px">
          <NSelect v-model:value="model.status" :options="translateOptions(enableStatusOptions)" clearable />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6" label="创建人" path="createBy" class="pr-16px">
          <NInput v-model:value="model.createBy" />
        </NFormItemGi>

        <NFormItemGi span="24 m:12" class="pr-16px">
          <NFlex class="w-full" justify="end">
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
          </NFlex>
        </NFormItemGi>
      </NGrid>
    </NForm>
  </NCard>
</template>

<style scoped></style>
