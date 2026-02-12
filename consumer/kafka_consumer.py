"""
Kafka Consumer Module
Đọc dữ liệu từ Kafka và insert vào MySQL
"""

import json
import sys
import os
from datetime import datetime
from kafka import KafkaConsumer
import pymysql
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeatherConsumer:
    """Kafka Consumer for weather data"""
    
    def __init__(self):
        """Initialize Kafka Consumer and MySQL connection"""
        # Kafka configuration
        self.kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        self.kafka_topic = os.getenv('KAFKA_TOPIC', 'weather_data')
        
        # MySQL configuration
        self.mysql_config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3307)),
            'user': os.getenv('MYSQL_USER', 'weather_user'),
            'password': os.getenv('MYSQL_PASSWORD', 'weather_pass'),
            'database': os.getenv('MYSQL_DATABASE', 'weather_db'),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        
        self.consumer = None
        self.db_connection = None
        
    def connect_mysql(self):
        """Kết nối đến MySQL database"""
        try:
            self.db_connection = pymysql.connect(**self.mysql_config)
            logger.info("✓ Connected to MySQL successfully")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to connect to MySQL: {str(e)}")
            return False
    
    def create_kafka_consumer(self):
        """Tạo Kafka consumer"""
        try:
            self.consumer = KafkaConsumer(
                self.kafka_topic,
                bootstrap_servers=[self.kafka_servers],
                auto_offset_reset='earliest',  # Đọc từ đầu topic
                enable_auto_commit=True,
                group_id='weather_consumer_group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                consumer_timeout_ms=10000,  # Timeout sau 10 giây không có message
                api_version=(0, 10, 1),  # Kafka API version
                request_timeout_ms=30000,  # Request timeout 30 giây
                session_timeout_ms=30000,  # Session timeout 30 giây
                heartbeat_interval_ms=10000,  # Heartbeat interval 10 giây
                max_poll_interval_ms=300000  # Max poll interval 5 phút
            )
            logger.info(f"✓ Connected to Kafka ({self.kafka_servers})")
            logger.info(f"✓ Subscribed to topic: {self.kafka_topic}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to create Kafka consumer: {str(e)}")
            return False
    
    def insert_weather_data(self, data):
        """
        Insert weather data vào MySQL
        
        Args:
            data: Dictionary chứa weather data
        """
        try:
            with self.db_connection.cursor() as cursor:
                sql = """
                INSERT INTO weather_data (
                    city, timestamp, temperature, feels_like, temp_min, temp_max,
                    pressure, humidity, weather_main, weather_description,
                    wind_speed, wind_deg, clouds, country, sunrise, sunset,
                    timezone, visibility, rain_1h, rain_3h
                ) VALUES (
                    %(city)s, %(timestamp)s, %(temperature)s, %(feels_like)s, 
                    %(temp_min)s, %(temp_max)s, %(pressure)s, %(humidity)s,
                    %(weather_main)s, %(weather_description)s, %(wind_speed)s,
                    %(wind_deg)s, %(clouds)s, %(country)s, %(sunrise)s, %(sunset)s,
                    %(timezone)s, %(visibility)s, %(rain_1h)s, %(rain_3h)s
                )
                """
                
                # Prepare data
                insert_data = {
                    'city': data.get('city'),
                    'timestamp': data.get('timestamp'),
                    'temperature': data.get('temperature'),
                    'feels_like': data.get('feels_like'),
                    'temp_min': data.get('temp_min'),
                    'temp_max': data.get('temp_max'),
                    'pressure': data.get('pressure'),
                    'humidity': data.get('humidity'),
                    'weather_main': data.get('weather_main'),
                    'weather_description': data.get('weather_description'),
                    'wind_speed': data.get('wind_speed'),
                    'wind_deg': data.get('wind_deg'),
                    'clouds': data.get('clouds'),
                    'country': data.get('country'),
                    'sunrise': data.get('sunrise'),
                    'sunset': data.get('sunset'),
                    'timezone': data.get('timezone'),
                    'visibility': data.get('visibility'),
                    'rain_1h': data.get('rain_1h', 0),
                    'rain_3h': data.get('rain_3h', 0)
                }
                
                cursor.execute(sql, insert_data)
                self.db_connection.commit()
                
                logger.info(f"✓ Inserted data for {data.get('city')} at {data.get('timestamp')}")
                return True
                
        except Exception as e:
            logger.error(f"✗ Failed to insert data: {str(e)}")
            self.db_connection.rollback()
            return False
    
    def consume_messages(self):
        """Đọc messages từ Kafka và insert vào MySQL"""
        logger.info("=" * 70)
        logger.info("Starting Weather Data Consumer")
        logger.info("=" * 70)
        logger.info("⏳ Waiting for messages from Kafka... (Press Ctrl+C to stop)")
        logger.info("=" * 70)
        
        message_count = 0
        
        try:
            for message in self.consumer:
                message_count += 1
                data = message.value
                
                logger.info(f"\n📨 Message #{message_count} received:")
                logger.info(f"   City: {data.get('city')}")
                logger.info(f"   Temperature: {data.get('temperature')}°C")
                logger.info(f"   Humidity: {data.get('humidity')}%")
                
                # Insert vào database
                success = self.insert_weather_data(data)
                
                if success:
                    logger.info(f"   ✓ Total messages processed: {message_count}")
                else:
                    logger.warning(f"   ✗ Failed to process message #{message_count}")
                
        except KeyboardInterrupt:
            logger.info("\n" + "=" * 70)
            logger.info(f"Shutting down consumer... Total messages processed: {message_count}")
            logger.info("=" * 70)
        except Exception as e:
            logger.error(f"Error consuming messages: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def close(self):
        """Đóng connections"""
        if self.consumer:
            self.consumer.close()
            logger.info("✓ Kafka consumer closed")
        
        if self.db_connection:
            self.db_connection.close()
            logger.info("✓ MySQL connection closed")
    
    def run(self):
        """Main run method"""
        try:
            # Kết nối MySQL
            if not self.connect_mysql():
                return False
            
            # Tạo Kafka consumer
            if not self.create_kafka_consumer():
                self.close()
                return False
            
            # Bắt đầu consume messages
            self.consume_messages()
            
        finally:
            self.close()
        
        return True


def main():
    """Main entry point"""
    consumer = WeatherConsumer()
    consumer.run()


if __name__ == "__main__":
    main()
