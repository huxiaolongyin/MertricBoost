-- 创建hypertable存储电池数据
CREATE TABLE
    battery_metrics (
        time TIMESTAMPTZ NOT NULL,
        vin TEXT NOT NULL,
        battery_soc FLOAT,
        battery_voltage FLOAT,
        battery_charge_current_per_second FLOAT,
        battery_discharge_current_per_second FLOAT,
        charge_cumulative_capacity_this_time FLOAT,
        charge_cumulative_energy_this_time FLOAT,
        discharge_cumulative_capacity_this_time FLOAT,
        discharge_cumulative_energy_this_time FLOAT,
        charge_time_this_time FLOAT,
        discharge_time_this_time FLOAT,
        actual_capacity FLOAT,
        actual_charge_capacity FLOAT
    );

-- 转换为hypertable并设置分区
SELECT
    create_hypertable (
        'battery_metrics',
        'time',
        chunk_time_interval => INTERVAL '1 month'
    );

-- 为VIN创建索引以加速按车辆查询
CREATE INDEX idx_battery_vin ON battery_metrics (vin, time DESC);

CREATE TABLE
    vin_list (vin TEXT NOT NULL);