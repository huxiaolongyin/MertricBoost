# 待办事项

优先级说明：

- 🔴P1: 紧急且重要，立即处理
- 🟠P2: 重要但不紧急，本迭代完成
- 🟡P3: 常规任务，按计划进行
- 🟢P4: 待定/低优先级，有空闲资源时处理

## 系统

- [x] 🟡P3 隐藏主题配置按钮，或者配置为角色可管控
- [ ] 🟠P2 增加短信登录验证码
- [ ] 🟡P3 新增用户中心管理页
- [ ] 🟡P3 优化浏览器缩放情况下导致的指标数据溢出卡片

## 指标管理

- [ ] 🟡P3 路由加载问题，导致点击指标探索时，无法进入(临时措施，没有加载到路由时，提示刷新)
- [x] 🟠P2 将累计数据改为不可点击指标探索
- [ ] 🟡P3 将指标格式的显示从数据模型层，改到指标层设置
- [x] 🟡P3 修复指标详情字段显示问题
- [ ] 🟡P3 指标卡片页新增热度显示

## 智能报告
通过Prompt + AI + 指标具体内容 的形式，生成一份报告，支持PDF下载
- [ ] 🟡P3 编写智能报告接口
- [ ] 🟡P3 新增智能报告模板接口

## 大数据采集
- [ ] 🔴P1 离线数据采集开发
- [ ] 🔴P1 实时数据采集开发

## 查询和检索功能
- [ ] 🔴P1 历史轨迹数据检索
- [ ] 🔴P1 机器人充电过程数据检索

## 数据开发
- [ ] 🟠P2 数据任务的提交
- [ ] 🟠P2 数据任务的调度管理

## 部署
<!-- - [ ] 🟠P2 后端的Nginx的转发，如果释放公网前端 -->

## BUG FIX
- [ ] 🟡P3 登录时，metricboost.core.exceptions.HTTPException: 4010: 登录已过期在前端不显示