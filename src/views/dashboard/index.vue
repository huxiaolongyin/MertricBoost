<template>
    <div>
        <div class="flex justify-center w-full mb-5">
            <NInput placeholder="大屏搜索" class='my-3 h-10 rounded-xl dark:bg-slate-700 flex items-center'
                style="width: 65%">
                <template #suffix>
                    <Icon icon="mdi:magnify" width="28" height="28" />
                </template>
            </NInput>
        </div>
        <NGrid cols="s:1 m:2 l:4" responsive="screen" :x-gap="16" :y-gap="16">
            <NGi>
                <NCard class="rounded-e-2xl">
                    <NImage height="100%" width="100%"
                        src="https://pic2.zhimg.com/v2-83eaaad2462a2136660a8281809365d7_1440w.jpg" />
                    <div class="bottom-title-bar">
                        大数据分析系统
                    </div>
                </NCard>
            </NGi>
            <NGi>
                <NCard class="rounded-e-2xl">
                    <NImage height="100%" width="100%"
                        src="https://i.postimg.cc/Pq3jxqX8/Snipaste-2024-11-13-18-04-15.png" />
                    <div class="bottom-title-bar">
                        停车场监控大屏
                    </div>
                </NCard>
            </NGi>
            <NGi>
                <NCard class="rounded-e-2xl">
                    <NImage height="100%" width="100%"
                        src="https://i.postimg.cc/6qRJYLdd/Snipaste-2024-11-13-18-06-13.png" />
                    <div class="bottom-title-bar">
                        企业综合驾驶舱
                    </div>
                </NCard>
            </NGi>
        </NGrid>
    </div>
</template>

<script lang="ts">
import { defineComponent, h } from 'vue'
import { NButton, NGrid, NImage, NTag, useMessage } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'

interface RowData {
    key: number
    id: number
    name: string
    detail: string
    creator: string
    update_time: string
}

function createColumns({
    viewDetails,
    handleDelete
}: {
    viewDetails: (rowData: RowData) => void,
    handleDelete: (rowData: RowData) => void
}): DataTableColumns<RowData> {
    return [
        {
            title: 'ID',
            key: 'id'
        },
        {
            title: '名称',
            key: 'name'
        },
        {
            title: '描述',
            key: 'detail'
        },
        {
            title: '创建人',
            key: 'creator'
        },
        {
            title: '更新日期',
            key: 'update_time'
        },
        {
            title: '操作',
            key: 'actions',
            render(row) {
                return h('div', [
                    h(
                        NButton,
                        {
                            size: 'small',
                            style: 'margin-right: 8px',
                            onClick: () => viewDetails(row)
                        },
                        { default: () => '查看' }
                    ),
                    h(
                        NButton,
                        {
                            size: 'small',
                            type: 'error',
                            onClick: () => handleDelete(row)
                        },
                        { default: () => '删除' }
                    )
                ])
            }
        }
    ]
}

function createData(): RowData[] {
    return [
        {
            key: 0,
            id: 1,
            name: '业务大屏',
            detail: '用于展示业务相关的大屏',
            creator: 'admin',
            update_time: '2023-01-01 12:00:00'
        },
        {
            key: 0,
            id: 2,
            name: '业务大屏',
            detail: '用于展示业务相关的大屏',
            creator: 'admin',
            update_time: '2023-01-01 12:00:00'
        },

    ]
}

export default defineComponent({
    setup() {
        const message = useMessage()
        return {
            data: createData(),
            columns: createColumns({
                viewDetails(rowData) {
                    message.info(`查看 ${rowData.name}`)
                },
                handleDelete(rowData) {
                    message.info(`删除 ${rowData.name}`)
                }
            }),
            pagination: {
                pageSize: 10
            }
        }
    }
})
</script>

<style scoped>
.bottom-title-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40px;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    align-items: center;
    padding: 0 16px;
}
</style>