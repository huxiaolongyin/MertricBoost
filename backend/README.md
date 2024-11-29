# 数据库启动
```bash
docker run -d --name mysql -p 5260:3306 -v ${PWD}/mysql/conf.d:/etc/mysql/conf.d -v ${PWD}/mysql/logs:/logs -v ${PWD}/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -e TZ=Asia/Shanghai mysql:9.0
```


# 指标功能
1. 根据模型(另外的表，用于记录统计的sql语句)，查询数据
2. 能够