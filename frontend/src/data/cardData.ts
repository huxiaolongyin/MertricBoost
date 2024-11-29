import axios from 'axios';
import { MetricData } from '@/typings/metrics';

const staticCardData: MetricData[] = [
    {
        id: "1",
        chineseName: '使用率',
        englishName: 'Usage Rate',
        alias: '使用率',
        sensitivity: '1',
        dataModel: '访问数据统计信息',
        formatType: 'percent',
        businessScope: '访问数据统计信息',
        chartType: 'line',
        chartDisplayDate: '7',
        statisticColumn: 'id',
        statisticType: 'count',
        showType: '1',
        publishStatus: '1',
        tags: ['用户', '2024'],
        data: [
            { date: '2024-01-01', value: 0.4538 },
            { date: '2024-01-02', value: 0.4936 },
            { date: '2024-01-03', value: 0.4568 },
        ],
    },
    {
        id: '2',
        chineseName: '利润',
        englishName: 'Profit',
        alias: '利润',
        sensitivity: '1',
        dataModel: '经营数据统计信息',
        formatType: 'currency',
        businessScope: '经营数据统计信息',
        chartType: 'bar',
        chartDisplayDate: '7',
        statisticColumn: 'money',
        statisticType: 'sum',
        showType: '2',
        publishStatus: '1',
        tags: ['经营', '2024'],
        data: [
            { date: '2024-01-01', value: 100000 },
            { date: '2024-01-02', value: 120000 },
            { date: '2024-01-03', value: 110000 }],
    },
    {
        id: '3',
        chineseName: '满意度',
        englishName: 'Satisfaction',
        alias: '满意度',
        sensitivity: '1',
        dataModel: '用户满意度调查',
        formatType: 'percent',
        businessScope: '用户满意度调查',
        chartType: 'line',
        chartDisplayDate: '7',
        statisticColumn: 'score',
        statisticType: 'average',
        showType: '1',
        publishStatus: '0',
        tags: ['用户', '2024'],
        data: [
            { date: '2024-01-01', value: 0.8 },
            { date: '2024-01-02', value: 0.85 },
            { date: '2024-01-03', value: 0.83 }],
    },
    {
        id: '4',
        chineseName: '销售额',
        englishName: 'Sales',
        alias: '销售额',
        sensitivity: '3',
        dataModel: '销售数据统计信息',
        formatType: 'currency',
        businessScope: '销售数据统计信息',
        chartType: 'bar',
        chartDisplayDate: '7',
        statisticColumn: 'sales',
        statisticType: 'sum',
        showType: '1',
        publishStatus: '0',
        tags: ['销售', '2024'],
        data: [
            { date: '2024-01-01', value: 100000 },
            { date: '2024-01-02', value: 120000 },
            { date: '2024-01-03', value: 110000 },],
    },
    {
        id: '5',
        chineseName: '故障率',
        englishName: 'Failure Rate',
        alias: '故障率',
        sensitivity: '2',
        dataModel: '系统故障统计信息',
        formatType: 'percent',
        businessScope: '系统故障统计信息',
        chartType: 'line',
        chartDisplayDate: '7',
        statisticColumn: 'failure',
        statisticType: 'average',
        showType: '1',
        publishStatus: '1',
        tags: ['系统', '2024'],
        data: [
            { date: '2024-01-01', value: 0.02 },
            { date: '2024-01-02', value: 0.01 },
            { date: '2024-01-03', value: 0.015 }],
    }]


// 获取指标的api数据，如果是生产环境，则从后端获取，否则使用静态数据
export async function fetchCardData(id?: string | string[]): Promise<MetricData[]> {
    const isProduction = process.env.NODE_ENV === 'production';

    if (isProduction) {
        try {
            const response = await axios.get('/api/v1/cardData', { params: { id } });
            return response.data;
        } catch (error) {
            console.error('Error fetching card data:', error);
            return [];
        }
    } else {
        if (id) {
            return staticCardData.filter(card => card.id === id);
        } else {
            return staticCardData;
        }

    }
}

