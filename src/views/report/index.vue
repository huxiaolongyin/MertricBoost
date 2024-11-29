<template>
  <div>
    <NFlex justify="end" align="center" class="w-full mb-5">
      <div class="w-2/12">
        <NInput placeholder="搜索报告名称">
          <template #prefix>
            <Icon icon="mdi:search" class="text-gray" width="20" height="20" />
          </template>
        </NInput>
      </div>
      <NButton class="bg-blue-700 text-white">
        <template #icon>
          <Icon icon="mdi:plus" width="35" height="35" />
        </template>
        新建
      </NButton>
    </NFlex>
    <NDataTable :columns="columns" :data="data" striped></NDataTable>
  </div>
</template>

<script setup lang="tsx">
import { NFlex, type DataTableColumns, NButton, NDropdown } from 'naive-ui'
import { Icon } from '@iconify/vue';

const columns: DataTableColumns = [
  {
    type: 'selection',
  },
  {
    title: '报告名称',
    key: 'reportName',
    sorter: 'default',
    width: 100
  },
  {
    title: '报告类型',
    key: 'reportType',
    sorter: 'default',
    width: 100
  },
  {
    title: '生成日期',
    key: 'generateDate',
    sorter: 'default',
    width: 100
  },
  {
    title: '操作',
    key: 'operate',
    align: 'center',
    width: 200,
    render: row => (
      <div>
        <NFlex align='center' justify='center'>
          <NButton round size='small' strong secondary type="info" class="w-22">查看</NButton>
          <NButton round size='small' strong secondary type="success" class="w-22">智能分析</NButton>
          <NButton round size='small' strong secondary type="error" class="w-22">删除</NButton>
          <NButton quaternary ><Icon icon='uim:favorite' width="25" height="25" class="text-gray" /></NButton>
          <NDropdown options={menuOpiton} trigger="click" >
            <Icon icon="material-symbols:more-horiz" width="24" height="24" class="ml-5 text-slate-400 hover:text-slate-600" />
          </NDropdown>
        </NFlex>
      </div >
    )
  },
]

const data = [
  {
    id: 1,
    reportName: '报告1',
    reportType: '类型1',
    generateDate: '2023-09-01',
    actions: '操作1'
  },
  {
    id: 2,
    reportName: '报告2',
    reportType: '类型2',
    generateDate: '2023-09-02',
    actions: '操作2'
  },
  {
    id: 3,
    reportName: '报告3',
    reportType: '类型3',
    generateDate: '2023-09-03',
    actions: '操作3'
  },
  {
    id: 4,
    reportName: '报告4',
    reportType: '类型4',
    generateDate: '2023-09-04',
    actions: '操作4'
  },
  {
    id: 5,
    reportName: '报告5',
    reportType: '类型5',
    generateDate: '2023-09-05',
    actions: '操作5'
  }]

// 添加更多的选项
const menuOpiton = [
  {
    label: '选项1',
    key: 'option1',
  },
  {
    label: '选项2',
    key: 'option2',
  },
  {
    label: '选项3',
    key: 'option3',
  },]
</script>
<style scoped></style>
