-- 创建数据库
create database metric_platform;

use metric_platform;
-- 指标管理表
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    chinese_name VARCHAR(100),
    english_name VARCHAR(100),
    alias VARCHAR(100),
    sensitivity VARCHAR(10),
    data_model VARCHAR(100),
    format_type VARCHAR(50),
    business_scope VARCHAR(100),
    chart_type VARCHAR(50),
    chart_display_date VARCHAR(20),
    statistic_column VARCHAR(50),
    statistic_type VARCHAR(50),
    show_type VARCHAR(10),
    publish_status VARCHAR(10),
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 指标收藏表
CREATE TABLE metric_favorites (
    id SERIAL PRIMARY KEY,
    metric_id INTEGER REFERENCES metrics(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(metric_id, user_id)  -- 防止重复收藏
);
-- 指标数据表
CREATE TABLE metric_data (
    id SERIAL PRIMARY KEY,
    metric_id INTEGER,
    date DATE,
    value DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (metric_id) REFERENCES metrics(id)
);

-- 角色-指标关联表
CREATE TABLE role_metrics (
    role_id INTEGER,
    metric_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (metric_id) REFERENCES metrics(id)
);