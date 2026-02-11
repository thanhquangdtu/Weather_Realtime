"""
Spark Streaming Module
Xử lý streaming data từ Kafka và ghi vào MySQL
"""

import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.kafka_config import KafkaConfig
from configs.mysql_config import MySQLConfig
from configs.settings import Settings
from transform import (
    parse_kafka_message,
    clean_weather_data,
    prepare_for_mysql
)


def create_spark_session():
    """
    Tạo Spark Session với cấu hình cần thiết
    
    Returns:
        SparkSession
    """
    spark = SparkSession.builder \
        .appName(Settings.SPARK_APP_NAME) \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                "mysql:mysql-connector-java:8.0.33") \
        .config("spark.sql.streaming.checkpointLocation", Settings.CHECKPOINT_DIR) \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    return spark


def read_from_kafka(spark: SparkSession):
    """
    Đọc streaming data từ Kafka
    
    Args:
        spark: SparkSession
    
    Returns:
        Streaming DataFrame từ Kafka
    """
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KafkaConfig.BOOTSTRAP_SERVERS) \
        .option("subscribe", KafkaConfig.TOPIC_NAME) \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()
    
    return kafka_df


def write_to_mysql(df, epoch_id):
    """
    Ghi batch data vào MySQL
    
    Args:
        df: Batch DataFrame
        epoch_id: Batch ID
    """
    try:
        df.write \
            .format("jdbc") \
            .option("url", MySQLConfig.get_jdbc_url()) \
            .option("dbtable", "weather_data") \
            .option("user", MySQLConfig.USER) \
            .option("password", MySQLConfig.PASSWORD) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .mode("append") \
            .save()
        
        print(f"✓ Batch {epoch_id}: Successfully wrote {df.count()} records to MySQL")
        
    except Exception as e:
        print(f"✗ Batch {epoch_id}: Error writing to MySQL: {str(e)}")


def process_stream(spark: SparkSession):
    """
    Xử lý streaming pipeline
    
    Args:
        spark: SparkSession
    """
    # Đọc từ Kafka
    kafka_df = read_from_kafka(spark)
    
    # Parse và transform
    weather_df = parse_kafka_message(kafka_df)
    cleaned_df = clean_weather_data(weather_df)
    mysql_df = prepare_for_mysql(cleaned_df)
    
    # Ghi vào MySQL với foreachBatch
    query = mysql_df.writeStream \
        .outputMode("append") \
        .foreachBatch(write_to_mysql) \
        .option("checkpointLocation", f"{Settings.CHECKPOINT_DIR}/weather_stream") \
        .trigger(processingTime=f"{Settings.BATCH_INTERVAL} seconds") \
        .start()
    
    # Console output để debug (optional)
    console_query = cleaned_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .option("numRows", 5) \
        .trigger(processingTime=f"{Settings.BATCH_INTERVAL} seconds") \
        .start()
    
    return query, console_query


def main():
    """Main entry point"""
    print("=" * 70)
    print("Starting Spark Streaming Application")
    print("=" * 70)
    print(f"App Name: {Settings.SPARK_APP_NAME}")
    print(f"Kafka Topic: {KafkaConfig.TOPIC_NAME}")
    print(f"Kafka Brokers: {KafkaConfig.BOOTSTRAP_SERVERS}")
    print(f"MySQL Database: {MySQLConfig.DATABASE}")
    print(f"Batch Interval: {Settings.BATCH_INTERVAL} seconds")
    print("=" * 70)
    
    try:
        # Tạo Spark session
        spark = create_spark_session()
        print("✓ Spark session created successfully")
        
        # Process streaming data
        print("\n✓ Starting stream processing...")
        mysql_query, console_query = process_stream(spark)
        
        print("✓ Streaming queries started successfully")
        print("\n ⏳ Waiting for data... (Press Ctrl+C to stop)\n")
        
        # Wait for termination
        mysql_query.awaitTermination()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("Shutting down Spark Streaming...")
        print("=" * 70)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if 'spark' in locals():
            spark.stop()
            print("✓ Spark session stopped")


if __name__ == "__main__":
    main()
