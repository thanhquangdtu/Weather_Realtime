"""
Schema Definition Module
Định nghĩa schema cho dữ liệu thời tiết
"""

from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    IntegerType, LongType, TimestampType
)


def get_weather_schema():
    """
    Định nghĩa schema cho weather data từ Kafka
    
    Returns:
        StructType: Spark schema cho weather data
    """
    return StructType([
        StructField("city", StringType(), nullable=False),
        StructField("timestamp", StringType(), nullable=False),
        StructField("temperature", DoubleType(), nullable=False),
        StructField("feels_like", DoubleType(), nullable=True),
        StructField("temp_min", DoubleType(), nullable=True),
        StructField("temp_max", DoubleType(), nullable=True),
        StructField("pressure", IntegerType(), nullable=True),
        StructField("humidity", IntegerType(), nullable=True),
        StructField("weather_main", StringType(), nullable=True),
        StructField("weather_description", StringType(), nullable=True),
        StructField("wind_speed", DoubleType(), nullable=True),
        StructField("wind_deg", IntegerType(), nullable=True),
        StructField("clouds", IntegerType(), nullable=True),
        StructField("country", StringType(), nullable=True),
        StructField("sunrise", LongType(), nullable=True),
        StructField("sunset", LongType(), nullable=True),
        StructField("timezone", IntegerType(), nullable=True),
        StructField("visibility", IntegerType(), nullable=True),
        StructField("rain_1h", DoubleType(), nullable=True),
        StructField("rain_3h", DoubleType(), nullable=True),
    ])


def get_aggregated_schema():
    """
    Schema cho aggregated weather data
    
    Returns:
        StructType: Spark schema cho aggregated data
    """
    return StructType([
        StructField("city", StringType(), nullable=False),
        StructField("window_start", TimestampType(), nullable=False),
        StructField("window_end", TimestampType(), nullable=False),
        StructField("avg_temperature", DoubleType(), nullable=True),
        StructField("max_temperature", DoubleType(), nullable=True),
        StructField("min_temperature", DoubleType(), nullable=True),
        StructField("avg_humidity", DoubleType(), nullable=True),
        StructField("avg_wind_speed", DoubleType(), nullable=True),
        StructField("record_count", LongType(), nullable=True),
    ])


# Database table schema SQL
WEATHER_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    feels_like DECIMAL(5,2),
    temp_min DECIMAL(5,2),
    temp_max DECIMAL(5,2),
    pressure INT,
    humidity INT,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100),
    wind_speed DECIMAL(5,2),
    wind_deg INT,
    clouds INT,
    country VARCHAR(10),
    sunrise BIGINT,
    sunset BIGINT,
    timezone INT,
    visibility INT,
    rain_1h DECIMAL(5,2) DEFAULT 0,
    rain_3h DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_timestamp (timestamp),
    INDEX idx_city_timestamp (city, timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

AGGREGATED_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS weather_aggregated (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    window_start DATETIME NOT NULL,
    window_end DATETIME NOT NULL,
    avg_temperature DECIMAL(5,2),
    max_temperature DECIMAL(5,2),
    min_temperature DECIMAL(5,2),
    avg_humidity DECIMAL(5,2),
    avg_wind_speed DECIMAL(5,2),
    record_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY idx_city_window (city, window_start),
    INDEX idx_window_start (window_start)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
