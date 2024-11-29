<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { ref } from 'vue';
import DecisionInfo from './modules/decision-info.vue';

// 定义基础信息显示
const infoShow = ref(false);

// 跳转到新增指标页面
const handleAdd = () => {
  infoShow.value = !infoShow.value;
  //   const { routerPushByKey } = useRouterPush(false);
  //   routerPushByKey("decision-detail", { params: { id: "add" } });
  // };
};
const handleSubmit = () => {};
</script>

<template>
  <div>
    <NFloatButton :right="50" :bottom="60" shape="circle" width="60" height="60" class="bg-red-500" @click="handleAdd">
      <Icon icon="mdi:plus" class="text-white" width="35" height="35" />
    </NFloatButton>

    <NDrawer v-model:show="infoShow" :width="1000">
      <NDrawerContent>
        <template #header>编辑指标</template>
        <template #footer>
          <NButton class="px-6" type="primary" @click="handleSubmit">保存</NButton>
        </template>
        <DecisionInfo v-model:metric-data="model" />
      </NDrawerContent>
    </NDrawer>
  </div>
</template>

<style scoped></style>
