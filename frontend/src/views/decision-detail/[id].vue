<template>
  <div>
    <NCard>

      <NForm class="ml-5 mt-5">
        <NFlex align="center" class="mb-5">
          <Icon icon="mdi:numeric-1-circle" width="40" height="40" class="text-blue-700" />
          <div class="font-semibold text-xl">决策事件基本信息</div>
        </NFlex>
        <div class="ml-20">
          <NFormItem label="事件名称" label-placement="left" class="w-7/12">
            <NInput placeholder="请输入事件名称" />
          </NFormItem>
          <NFormItem label="事件描述" label-placement="left" class="w-7/12">
            <NInput placeholder="请输入事件描述" type="textarea" />
          </NFormItem>
          <NFormItem label="事件状态" label-placement="left" class="w-7/12">
            <NSwitch />
          </NFormItem>
          <NFormItem label="执行频率：" label-placement="left" class="w-7/12">
            <NFlex align="center" class="w-full">
              <div>
                每隔
              </div>
              <NInputNumber class="w-2/12" />
              <NSelect class="w-2/12" />
              <div>
                检查一次
              </div>
            </NFlex>
          </NFormItem>
        </div>
        <NFlex align="center" class="mb-5">
          <Icon icon="mdi:numeric-2-circle" width="40" height="40" class="text-blue-700" />
          <div class="font-semibold text-xl">配置决策</div>
        </NFlex>
        <NFormItem>
          <NFlex align="center" class="ml-15 w-7/12 bg-slate-100 px-5 py-2">
            <div>如果</div>
            <NSelect placeholder="生产效率" class="w-3/12" />
            <NSelect placeholder="低于" class="w-2/12" />
            <div class="w-2/12">
              <NInput placeholder="80%" />
            </div>
            <div>那么</div>
            <NSelect placeholder="发送通知邮件" class="w-3/12" />
          </NFlex>
        </NFormItem>
        <div class="ml-15 text-blue-700 hover:text-blue-900 add-branch">添加分支+</div>
        <NFlex justify="center">
          <NButton type="primary" class="w-24">保存</NButton>
        </NFlex>

      </NForm>

    </NCard>
  </div>
</template>
<script setup lang="ts">
import { Icon } from "@iconify/vue";
</script>

<style scoped>
.add-branch {
  cursor: pointer;
  user-select: none;
}

.add-branch:hover {
  opacity: 0.8;
}
</style>
