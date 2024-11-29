<template>
  <div>
    <NFloatButton :right="50" :bottom="60" shape="circle" width="60" height="60" class="bg-red-500" @click="handleAdd">
      <Icon icon="mdi:plus" class="text-white" width="35" height="35" />
    </NFloatButton>
  </div>
</template>

<script setup lang="ts">
import { useRouterPush } from "@/hooks/common/router";
import { Icon } from "@iconify/vue";
// 跳转到新增指标页面
const handleAdd = () => {
  const { routerPushByKey } = useRouterPush(false);
  routerPushByKey("decision-detail", { params: { id: "add" } });
};
</script>



<style scoped></style>
