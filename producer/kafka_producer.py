"""
Kafka Producer Module
Producer để gửi weather data vào Kafka
"""

import sys
import os
import json
from typing import Dict, Optional
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.kafka_config import KafkaConfig
from utils.logger import get_logger

logger = get_logger(__name__)


class WeatherKafkaProducer:
    """Kafka Producer cho weather data"""
    
    def __init__(self):
        """Initialize Kafka producer"""
        self.config = KafkaConfig.get_producer_config()
        self.topic = KafkaConfig.get_topic_name()
        self.producer = Producer(self.config)
        
        # Create topic nếu chưa có
        self._create_topic_if_not_exists()
        
        logger.info(f"Kafka producer initialized. Topic: {self.topic}")
    
    def _create_topic_if_not_exists(self):
        """Tạo Kafka topic nếu chưa tồn tại"""
        try:
            admin_client = AdminClient({'bootstrap.servers': self.config['bootstrap.servers']})
            
            # Check if topic exists
            metadata = admin_client.list_topics(timeout=10)
            
            if self.topic not in metadata.topics:
                logger.info(f"Creating topic: {self.topic}")
                
                new_topic = NewTopic(
                    self.topic,
                    num_partitions=KafkaConfig.TOPIC_CONFIG['num_partitions'],
                    replication_factor=KafkaConfig.TOPIC_CONFIG['replication_factor']
                )
                
                fs = admin_client.create_topics([new_topic])
                
                # Wait for operation to finish
                for topic, f in fs.items():
                    try:
                        f.result()
                        logger.info(f"Topic {topic} created successfully")
                    except Exception as e:
                        logger.error(f"Failed to create topic {topic}: {e}")
            else:
                logger.info(f"Topic {self.topic} already exists")
                
        except Exception as e:
            logger.warning(f"Could not create topic (may already exist): {e}")
    
    def delivery_callback(self, err, msg):
        """
        Callback được gọi khi message được delivered hoặc failed
        
        Args:
            err: Error nếu có
            msg: Message object
        """
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
    
    def send_weather_data(self, weather_data: Dict) -> bool:
        """
        Gửi weather data vào Kafka topic
        
        Args:
            weather_data: Dictionary chứa weather data
        
        Returns:
            True nếu gửi thành công, False nếu có lỗi
        """
        try:
            # Convert to JSON
            message_value = json.dumps(weather_data, ensure_ascii=False)
            
            # Sử dụng city làm key để partition theo city
            message_key = weather_data.get('city', 'unknown')
            
            # Send message
            self.producer.produce(
                topic=self.topic,
                key=message_key.encode('utf-8'),
                value=message_value.encode('utf-8'),
                callback=self.delivery_callback
            )
            
            # Trigger delivery reports
            self.producer.poll(0)
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {str(e)}")
            return False
    
    def flush(self):
        """Flush tất cả messages đang pending"""
        self.producer.flush()
    
    def close(self):
        """Close producer và flush remaining messages"""
        logger.info("Flushing and closing Kafka producer...")
        self.producer.flush()
        logger.info("Kafka producer closed successfully")


if __name__ == "__main__":
    # Test producer
    producer = WeatherKafkaProducer()
    
    # Test message
    test_data = {
        'city': 'Hanoi',
        'temperature': 25.5,
        'humidity': 70,
        'timestamp': '2024-02-11T10:00:00'
    }
    
    success = producer.send_weather_data(test_data)
    if success:
        print("✓ Test message sent successfully")
    else:
        print("✗ Failed to send test message")
    
    producer.close()
