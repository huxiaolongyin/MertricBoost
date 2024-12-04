<template>
    <NModal v-model:show="visible" display-directive="show" transform-origin="center" class="h-3/4 ">
        <NCard :title="modalTitle" :bordered="false" size="small" class="card-wrapper w-3/6 h-3/4">
            <NForm :model="model" :rules="rules" label-placement="left" class="mt-6">
                <NFormItem label="名称" path="dataDomainName">
                    <NInput v-model:value="model.domainName" placeholder="请输入域名称" />
                </NFormItem>
                <NFormItem label="描述" path="datadomainDesc">
                    <NInput v-model:value="model.domainDesc" placeholder="请输入域描述" />
                </NFormItem>
            </NForm>
            <NFlex justify="end">
                <NButton type="primary" class="w-20 mb-5" @click="handleSubmit"> 提 交 </NButton>
            </NFlex>
        </NCard>
    </NModal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/store/modules/auth';
import { fetchAddDataDomain, fetchUpdateDataDomain, fetchAddTopicDomain, fetchUpdateTopicDomain } from '@/service/api'
import { $t } from "@/locales";

// 用户状态，用于获取用户名
const authStore = useAuthStore();

// 双向绑定父组件，用于处理对话框的显示
const visible = defineModel<boolean>("visible", {
    default: false,
});

// 监听父组件传递的值
interface Props {
    operateType: NaiveUI.TableOperateType; // 操作类型
    domainType: 'dataDomain' | 'topicDomain'; // 操作对象
    rowData?: any | null; // 编辑行数据
}

const props = defineProps<Props>();


// 判断operateObject设置title 
const modalTitle = computed(() => {
    const action = props.operateType === 'add' ? '新增' : '编辑'
    const domain = props.domainType === 'dataDomain' ? '数据域' : '主题域'
    return `${action}${domain}`
})


const emit = defineEmits<{
    (e: 'changeDomain'): void;
}>();

// 创建表单初始化
const model = ref<Api.SystemManage.DomainUpdateParams>({
    id: null,
    domainName: null,
    domainDesc: null,
    createBy: null
})

// 设置表单验证规则
const rules = {
    dataDomainName: {
        required: true,
        message: '请输入名称',
    },
    datadomainDesc: {
        required: true,
        message: '请输入描述',
    }
}

// 设置提交逻辑

const handleSubmit = async () => {
    // 调用表单验证
    model.value.createBy = authStore.userInfo.userName
    visible.value = false
    emit('changeDomain')

    const operationMap: Record<string, (data: any) => Promise<any>> = {
        'add-dataDomain': fetchAddDataDomain,
        'add-topicDomain': fetchAddTopicDomain,
        'edit-dataDomain': fetchUpdateDataDomain,
        'edit-topicDomain': fetchUpdateTopicDomain
    }
    const key = `${props.operateType}-${props.domainType}`
    const operation = operationMap[key]

    const { error } = await operation(model.value)
    if (!error) {
        const messageKey = props.operateType === 'add' ? 'addSuccess' : 'updateSuccess'
        window.$message?.success($t(`common.${messageKey}`))
    }
}

watch(() => props.rowData, (newValue) => {
    if (newValue) {
        model.value = {
            id: newValue.value,
            domainName: newValue.label,
            domainDesc: newValue.domainDesc,
            createBy: null
        }
    }
}, { immediate: true })
</script>