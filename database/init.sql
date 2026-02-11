-- Weather Real-time Database Initialization Script
-- Tạo database và tables cho hệ thống thu thập dữ liệu thời tiết

-- Tạo database
CREATE DATABASE IF NOT EXISTS weather_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE weather_db;

-- Bảng lưu trữ dữ liệu thời tiết raw
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    temperature DECIMAL(5,2) NOT NULL COMMENT 'Temperature in Celsius',
    feels_like DECIMAL(5,2) COMMENT 'Feels like temperature',
    temp_min DECIMAL(5,2) COMMENT 'Minimum temperature',
    temp_max DECIMAL(5,2) COMMENT 'Maximum temperature',
    pressure INT COMMENT 'Atmospheric pressure in hPa',
    humidity INT COMMENT 'Humidity percentage',
    weather_main VARCHAR(50) COMMENT 'Weather condition main (Rain, Snow, Clear, etc)',
    weather_description VARCHAR(100) COMMENT 'Weather description',
    wind_speed DECIMAL(5,2) COMMENT 'Wind speed in m/s',
    wind_deg INT COMMENT 'Wind direction in degrees',
    clouds INT COMMENT 'Cloudiness percentage',
    country VARCHAR(10) COMMENT 'Country code',
    sunrise BIGINT COMMENT 'Sunrise time (Unix timestamp)',
    sunset BIGINT COMMENT 'Sunset time (Unix timestamp)',
    timezone INT COMMENT 'Timezone offset',
    visibility INT COMMENT 'Visibility in meters',
    rain_1h DECIMAL(5,2) DEFAULT 0 COMMENT 'Rain volume for last hour (mm)',
    rain_3h DECIMAL(5,2) DEFAULT 0 COMMENT 'Rain volume for last 3 hours (mm)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_city (city),
    INDEX idx_timestamp (timestamp),
    INDEX idx_city_timestamp (city, timestamp),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Real-time weather data from OpenWeatherMap API';


-- Bảng lưu trữ dữ liệu aggregated theo time window
CREATE TABLE IF NOT EXISTS weather_aggregated (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    window_start DATETIME NOT NULL,
    window_end DATETIME NOT NULL,
    avg_temperature DECIMAL(5,2) COMMENT 'Average temperature in window',
    max_temperature DECIMAL(5,2) COMMENT 'Maximum temperature in window',
    min_temperature DECIMAL(5,2) COMMENT 'Minimum temperature in window',
    avg_humidity DECIMAL(5,2) COMMENT 'Average humidity in window',
    avg_wind_speed DECIMAL(5,2) COMMENT 'Average wind speed in window',
    record_count INT COMMENT 'Number of records in window',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY idx_city_window (city, window_start),
    INDEX idx_window_start (window_start),
    INDEX idx_window_end (window_end)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Aggregated weather data by time windows';


-- Bảng lưu trữ metadata về cities
CREATE TABLE IF NOT EXISTS cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(10) NOT NULL,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    timezone INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY idx_city_country (city_name, country_code),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Metadata for monitored cities';


-- Bảng lưu trữ logs/alerts
CREATE TABLE IF NOT EXISTS weather_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    alert_type VARCHAR(50) NOT NULL COMMENT 'Type: extreme_temp, heavy_rain, strong_wind',
    alert_level VARCHAR(20) NOT NULL COMMENT 'Level: warning, critical',
    message TEXT,
    threshold_value DECIMAL(10,2),
    actual_value DECIMAL(10,2),
    timestamp DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_city (city),
    INDEX idx_type (alert_type),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Weather alerts and warnings';


-- Insert sample cities
INSERT INTO cities (city_name, country_code, latitude, longitude, timezone, is_active) 
VALUES 
    ('Hanoi', 'VN', 21.0285, 105.8542, 25200, TRUE),
    ('Ho Chi Minh City', 'VN', 10.8231, 106.6297, 25200, TRUE),
    ('Da Nang', 'VN', 16.0544, 108.2022, 25200, TRUE),
    ('Hai Phong', 'VN', 20.8449, 106.6881, 25200, TRUE),
    ('Can Tho', 'VN', 10.0452, 105.7469, 25200, TRUE)
ON DUPLICATE KEY UPDATE 
    latitude = VALUES(latitude),
    longitude = VALUES(longitude),
    timezone = VALUES(timezone),
    is_active = VALUES(is_active);


-- View để xem latest weather cho mỗi city
CREATE OR REPLACE VIEW latest_weather AS
SELECT 
    w.*
FROM weather_data w
INNER JOIN (
    SELECT city, MAX(timestamp) as max_timestamp
    FROM weather_data
    GROUP BY city
) latest ON w.city = latest.city AND w.timestamp = latest.max_timestamp;


-- View để xem statistics theo city
CREATE OR REPLACE VIEW weather_statistics AS
SELECT 
    city,
    COUNT(*) as total_records,
    AVG(temperature) as avg_temp,
    MAX(temperature) as max_temp,
    MIN(temperature) as min_temp,
    AVG(humidity) as avg_humidity,
    AVG(wind_speed) as avg_wind_speed,
    MIN(timestamp) as first_record,
    MAX(timestamp) as last_record
FROM weather_data
GROUP BY city;


-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON weather_db.* TO 'weather_user'@'%';
-- FLUSH PRIVILEGES;

-- Show tables
SHOW TABLES;

-- Show table structure
DESCRIBE weather_data;
DESCRIBE weather_aggregated;
DESCRIBE cities;
DESCRIBE weather_alerts;
