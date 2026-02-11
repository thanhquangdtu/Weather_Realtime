"""
Transform Module
Các hàm transformation cho weather data
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col, from_json, to_timestamp, window,
    avg, max, min, count, current_timestamp,
    round as spark_round
)
from schema import get_weather_schema


def parse_kafka_message(df: DataFrame) -> DataFrame:
    """
    Parse Kafka message từ JSON string sang structured data
    
    Args:
        df: Raw Kafka DataFrame
    
    Returns:
        Parsed DataFrame với schema đã định nghĩa
    """
    weather_schema = get_weather_schema()
    
    # Parse JSON value từ Kafka
    parsed_df = df.select(
        from_json(col("value").cast("string"), weather_schema).alias("data")
    ).select("data.*")
    
    # Convert timestamp string sang timestamp type
    parsed_df = parsed_df.withColumn(
        "timestamp",
        to_timestamp(col("timestamp"))
    )
    
    return parsed_df


def clean_weather_data(df: DataFrame) -> DataFrame:
    """
    Làm sạch và validate weather data
    
    Args:
        df: Weather DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    # Filter out null values và invalid data
    cleaned_df = df.filter(
        (col("city").isNotNull()) &
        (col("timestamp").isNotNull()) &
        (col("temperature").isNotNull()) &
        (col("temperature") > -100) &
        (col("temperature") < 100) &
        (col("humidity") >= 0) &
        (col("humidity") <= 100)
    )
    
    # Fill null values cho các field optional
    cleaned_df = cleaned_df.fillna({
        "feels_like": 0.0,
        "wind_speed": 0.0,
        "wind_deg": 0,
        "clouds": 0,
        "visibility": 0,
        "rain_1h": 0.0,
        "rain_3h": 0.0
    })
    
    return cleaned_df


def add_derived_columns(df: DataFrame) -> DataFrame:
    """
    Thêm các cột derived/calculated
    
    Args:
        df: Weather DataFrame
    
    Returns:
        DataFrame với các cột mới
    """
    # Thêm temperature category
    df = df.withColumn(
        "temp_category",
        when(col("temperature") < 10, "Cold")
        .when((col("temperature") >= 10) & (col("temperature") < 25), "Moderate")
        .when(col("temperature") >= 25, "Hot")
        .otherwise("Unknown")
    )
    
    # Thêm humidity level
    df = df.withColumn(
        "humidity_level",
        when(col("humidity") < 30, "Low")
        .when((col("humidity") >= 30) & (col("humidity") < 60), "Normal")
        .when(col("humidity") >= 60, "High")
        .otherwise("Unknown")
    )
    
    # Temperature range
    df = df.withColumn(
        "temp_range",
        col("temp_max") - col("temp_min")
    )
    
    return df


def aggregate_by_window(df: DataFrame, window_duration: str = "10 minutes") -> DataFrame:
    """
    Aggregate data theo time window
    
    Args:
        df: Weather DataFrame
        window_duration: Độ dài của window (e.g., "5 minutes", "1 hour")
    
    Returns:
        Aggregated DataFrame
    """
    aggregated_df = df.groupBy(
        window(col("timestamp"), window_duration),
        col("city")
    ).agg(
        spark_round(avg("temperature"), 2).alias("avg_temperature"),
        spark_round(max("temperature"), 2).alias("max_temperature"),
        spark_round(min("temperature"), 2).alias("min_temperature"),
        spark_round(avg("humidity"), 2).alias("avg_humidity"),
        spark_round(avg("wind_speed"), 2).alias("avg_wind_speed"),
        count("*").alias("record_count")
    )
    
    # Extract window start and end
    aggregated_df = aggregated_df.select(
        col("city"),
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("avg_temperature"),
        col("max_temperature"),
        col("min_temperature"),
        col("avg_humidity"),
        col("avg_wind_speed"),
        col("record_count")
    )
    
    return aggregated_df


def prepare_for_mysql(df: DataFrame) -> DataFrame:
    """
    Chuẩn bị DataFrame để write vào MySQL
    
    Args:
        df: Weather DataFrame
    
    Returns:
        DataFrame ready for MySQL insert
    """
    # Select và rename columns theo database schema
    mysql_df = df.select(
        col("city"),
        col("timestamp"),
        spark_round(col("temperature"), 2).alias("temperature"),
        spark_round(col("feels_like"), 2).alias("feels_like"),
        spark_round(col("temp_min"), 2).alias("temp_min"),
        spark_round(col("temp_max"), 2).alias("temp_max"),
        col("pressure"),
        col("humidity"),
        col("weather_main"),
        col("weather_description"),
        spark_round(col("wind_speed"), 2).alias("wind_speed"),
        col("wind_deg"),
        col("clouds"),
        col("country"),
        col("sunrise"),
        col("sunset"),
        col("timezone"),
        col("visibility"),
        spark_round(col("rain_1h"), 2).alias("rain_1h"),
        spark_round(col("rain_3h"), 2).alias("rain_3h")
    )
    
    return mysql_df


# Import when để tránh lỗi
from pyspark.sql.functions import when
