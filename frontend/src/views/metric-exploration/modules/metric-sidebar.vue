<template>
    <NFlex vertical class="text-black mt-5 ml-5" size='large'>
        <div class="font-semibold text-xl mb-3 ">{{ model.chineseName }}</div>
        <NButtonGroup>
            <NPopover placement="bottom">
                <template #trigger>
                    <NButton size="small" class="w-40">
                        <template #icon>
                            <Icon icon="mdi:fire" />
                        </template>
                        188
                    </NButton>
                </template>
                查询热度
            </NPopover>
            <NPopover placement="bottom">
                <template #trigger>
                    <NButton size="small" class="w-40">
                        <template #icon>
                            <Icon icon="tabler:star" />
                        </template>
                        0
                    </NButton>
                </template>
                点击收藏
            </NPopover>
        </NButtonGroup>
        <div>
            <div>版本</div>
            <div class="text-gray mt-1">v1</div>
        </div>
        <div>
            <div class="font-medium">负责人</div>
            <div class="text-gray mt-1">{{ model.createBy }}</div>
        </div>
        <div>
            <div class="font-medium">上次更新时间</div>
            <div class="text-gray">{{ model.updateTime }}</div>
        </div>
        <NFlex align="center" size="small">
            <NPopover trigger="hover" :show-arrow="false" placement="bottom">
                <template #trigger>
                    <span class="bg-slate-200 py-1 pr-1 rounded font-medium"> 基础信息 </span>
                </template>
                <div>
                    <div class="font-bold">基础信息</div>
                    <NDivider style="margin: 6px 0;" />
                    <NGrid cols="3" :x-gap="12" :y-gap="12">
                        <NGi :span="1">
                            <NFlex vertical>
                                <div class="font-medium">选用模型：</div>
                                <div class="font-medium">业务口径：</div>
                                <div class="font-medium">中文名：</div>
                                <div class="font-medium">英文名：</div>
                                <div class="font-medium">敏感度：</div>
                                <div class="font-medium">统计显示：</div>
                            </NFlex>
                        </NGi>
                        <NGi :span="2">
                            <NFlex vertical>
                                <div class="font-medium">{{ model.dataModel }}</div>
                                <div class="font-medium">{{ model.businessScope }}</div>
                                <div class="font-medium">{{ model.chineseName }}</div>
                                <div class="font-medium">{{ model.englishName }}</div>
                                <div class="font-medium">{{ model.sensitivity }}</div>
                                <div class="font-medium">{{ model.chartDisplayDate }}{{ model.statisticalPeriod }}</div>
                            </NFlex>
                        </NGi>
                    </NGrid>
                </div>

            </NPopover>
            <NButton quaternary size="tiny" @click="infoShow = true">
                <template #icon>
                    <Icon icon="mynaui:edit" />
                </template>
            </NButton>
        </NFlex>
        <NDrawer v-model:show="infoShow" :width="1000">
            <NDrawerContent>
                <template #header>
                    编辑指标
                </template>
                <template #footer>
                    <NButton @click="handleSubmit" class="px-6" type="primary">提交</NButton>
                </template>
                <MetricInfo v-model:metric-data="model" />
            </NDrawerContent>
        </NDrawer>
        <div>
            <div class="font-medium">标签</div>
            <div class="flex items-center flex-wrap mt-1">
                <span v-for="tag in model.tags"
                    class="text-amber-600 bg-orange-50 dark:bg-slate-500 px-4px py-1px mr-2 rounded relative inline-flex items-center group">
                    {{ tag }}
                    <NPopconfirm @positive-click="handleRemoveTag(tag)" positive-text="确定" negative-text="取消">
                        <template #trigger>
                            <span
                                class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center text-xs cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity">
                                ×
                            </span>
                        </template>
                        确定要删除这个标签吗？
                    </NPopconfirm>
                </span>
                <span class="inline-flex items-center">
                    <NDropdown placement="bottom-start" trigger="click" size="small" :options="tagOptions"
                        @select="handleAddTag">
                        <NButton quaternary size="tiny"
                            class="text-gray bg-slate-100 dark:bg-slate-500 px-8px py-1px mr-2 rounded">
                            <icon-ic:round-plus class="text-icon" />
                        </NButton>
                    </NDropdown>
                </span>
            </div>
        </div>
    </NFlex>
</template>

<script setup lang="ts">
import { useLoadOptions } from '@/hooks/common/option'
import { fetchTag, fetchAddMetricTag, fetchDeleteMetricTag, fetchUpdateMetric } from "@/service/api"
import { onMounted, watch, ref } from 'vue'
import { useAuthStore } from '@/store/modules/auth';
import { Icon } from '@iconify/vue';
import MetricInfo from './metric-info.vue';
import { $t } from '@/locales'

// 定义组件的名称
defineOptions({
    name: 'MetricSidebar'
})

// 获取用户信息
const authStore = useAuthStore();

// 双向同步模型
const model = defineModel<Api.Metric.MetricData>("metricData", { required: true })

// 定义基础信息显示
const infoShow = ref(false)

// 移除标签
const handleRemoveTag = async (tag: string) => {
    fetchDeleteMetricTag({
        metricId: model.value.id,
        tag: tag,
    })
    // 删除标签
    model.value.tags = model.value.tags.filter(t => t !== tag)
    await fetchTagOptions()
    // 执行过滤操作
    filterOptions()
}

// 添加指标标签
const handleAddTag = async (key: string) => {
    fetchAddMetricTag({
        metricId: model.value.id,
        tagId: key,
        createBy: authStore.userInfo.userName
    })
    // 添加标签
    model.value.tags.push(tagOptions.value.filter(item => item.key === key)[0].label as string)
    await fetchTagOptions()
    // 执行过滤操作
    filterOptions()
}


// 当选中数据库时加载表列表
const {
    options: tagOptions,
    loading: tagLoading,
    fetchOptions: fetchTagOptions
} = useLoadOptions(
    () => fetchTag(),
    'tagName',
    'id')
const filterOptions = () => {
    // 执行过滤操作
    tagOptions.value = tagOptions.value.filter(
        item => !model.value.tags.includes(item.label as string)
    )
    // 将 tagOptions 中的 value 属性重命名为 key
    tagOptions.value = tagOptions.value.map(item => ({
        label: item.label,
        key: item.value
    }))
}

// 提交表单
const handleSubmit = async () => {
    const formData: Api.Metric.MetricUpdateParams = {
        id: model.value.id,
        dataModel: model.value.dataModel,
        businessScope: model.value.businessScope,
        chineseName: model.value.chineseName,
        englishName: model.value.englishName,
        alias: model.value.alias,
        sensitivity: model.value.sensitivity,
        statisticalPeriod: model.value.statisticalPeriod,
        chartType: model.value.chartType,
        chartDisplayDate: model.value.chartDisplayDate,
        publishStatus: model.value.publishStatus,
        createBy: authStore.userInfo.userName
    }
    // 更新指标
    const { error } = await fetchUpdateMetric(formData);
    if (!error) {
        window.$message?.success($t('common.updateSuccess'));
    }
    // 关闭抽屉
    infoShow.value = false

}

onMounted(async () => {
    await Promise.all([
        fetchTagOptions(),
        new Promise(resolve => {
            watch(() => model.value.tags, (newTags) => {
                if (newTags) {
                    resolve(newTags)
                }
            }, { immediate: true })
        })
    ])

    filterOptions()
})

</script>