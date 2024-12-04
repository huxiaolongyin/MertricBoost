<template>
    <NTree block-line cascade checkable :selectable="false" :data="filterTreeData"
        @update:checked-keys="updateCheckedKeys" :render-label="renderLabel" />
    <DataDomainNew v-model:visible="visible" @changeDomain="getDomain" :operateType="operateType"
        :domainType="domainType" :rowData="editingData" />
</template>

<script setup lang="tsx">
import type { TreeOption } from 'naive-ui'
import { fetchGetTopicDomainList, fetchGetDataDomainList, fetchDeleteTopicDomain, fetchDeleteDataDomain } from '@/service/api'
import { ref, onMounted, h } from 'vue'
import { NButton, NFlex, NPopconfirm } from 'naive-ui'
import { Icon } from '@iconify/vue';
import { $t } from '@/locales';
import DataDomainNew from './domain-operate.vue';

defineOptions({
    name: 'DomainFilter'
});

const emit = defineEmits<{
    (e: 'search'): void;
}>()

// 和父组件双向绑定模型
const model = defineModel<Api.SystemManage.DataModelSearchParams>('model', { required: true });

// 设置模型显隐性
const visible = ref(false);

// 设置传入表单的操作类型、域的类型
const operateType = ref<NaiveUI.TableOperateType>('add');
type DomainType = 'dataDomain' | 'topicDomain'
const domainType = ref<DomainType>('dataDomain')

// 设置传入表单的行数据
const editingData = ref(null);

// 获取筛选树的数据
const filterTreeData = ref<TreeOption[]>([])

const createTreeData = async (): Promise<TreeOption[]> => {
    // 获取数据域数据
    const { data: dataDomainData } = await fetchGetDataDomainList()

    // 获取主题域数据
    const { data: topicDomainData } = await fetchGetTopicDomainList()

    return [
        {
            label: '数据域',
            key: 'dataDomain',
            children: dataDomainData?.records?.map(item => ({
                label: item.domainName,
                key: `data_${item.id}`,
                domainType: 'dataDomain',
                domainDesc: item.domainDesc,
                value: item.id,
            })) || []
        },
        {
            label: '主题域',
            key: 'topicDomain',
            children: topicDomainData?.records?.map(item => ({
                label: item.domainName,
                domainType: 'topicDomain',
                domainDesc: item.domainDesc,
                key: `topic_${item.id}`,
                value: item.id
            })) || []
        }
    ]
}

// 增加类的删除和增加按钮
const renderLabel = (node: any) => {
    return (
        <NFlex justify="space-between">
            <div>{node.option.label}</div>
            {!node.option.domainType && (
                <NButton size='tiny' onClick={() => handleAdd(node.option.key)} quaternary>
                    <Icon icon="mdi:plus" width={16} height={16} class='text-slate-600' />
                </NButton>
            )}
            {node.option.domainType && (
                <NFlex justify="end" size={0} >
                    <NButton size='tiny' onClick={() => handleEdit(node.option.key, node.option)} quaternary>
                        <Icon icon="mdi:square-edit-outline" width={16} height={16} class='text-slate-600' />
                    </NButton>
                    <NPopconfirm onPositiveClick={() => handleDelete(node.option.domainType, node.option.value)}>
                        {{
                            default: () => $t('common.confirmDelete'),
                            trigger: () => (
                                <NButton size='tiny' quaternary>
                                    <Icon icon="mdi:minus" width={16} height={16} class='text-slate-600' />
                                </NButton>
                            )
                        }}
                    </NPopconfirm>
                </NFlex>
            )}
        </NFlex>
    )
}



const handleAdd = async (key: any) => {
    // 处理增加逻辑
    operateType.value = 'add'
    domainType.value = key
    visible.value = true
    // 重载数据
    filterTreeData.value = await createTreeData()
}

// 处理编辑
const handleEdit = async (key: any, data: any) => {
    // 处理编辑逻辑
    operateType.value = 'edit'
    domainType.value = data.domainType
    visible.value = true
    editingData.value = data
    // 重载数据
    filterTreeData.value = await createTreeData()
}

const handleDelete = async (domainType: DomainType, value: number) => {
    // 处理删除逻辑
    let error;

    if (domainType === 'dataDomain') {
        ({ error } = await fetchDeleteDataDomain({ id: value }));
    } else {
        ({ error } = await fetchDeleteTopicDomain({ id: value }));
    }

    if (!error) {
        window.$message?.success("删除成功");
        filterTreeData.value = await createTreeData()
    } else {
        console.log(error)
    }
}

// 获取数据
const getDomain = async () => {
    filterTreeData.value = await createTreeData()
}

// 在组件加载后，更新筛选树的数据
onMounted(() => {
    try {
        getDomain()
    }
    catch (e: any) {
        window.$message?.error(e);
    }
})

const updateCheckedKeys = (
    keys: Array<string | number>,
    options: Array<TreeOption | null>,
    meta: {
        node: TreeOption | null
        action: 'check' | 'uncheck'
    }
) => {
    model.value.dataDomainList = []
    model.value.topicDomainList = []
    options.forEach(option => {
        if (!option) return
        if (option.domainType === 'dataDomain' && option.value != null) {
            model.value.dataDomainList?.push(option.value as number)
        }
        else if (option.domainType === 'topicDomain' && option.value != null) {
            model.value.topicDomainList?.push(option.value as number)
        }
    }
    )
    emit('search')
}

</script>
