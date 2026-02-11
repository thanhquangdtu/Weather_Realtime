"""
Kafka Configuration Module
Cấu hình kết nối và tương tác với Apache Kafka
"""

import os
from dotenv import load_dotenv

load_dotenv()


class KafkaConfig:
    """Kafka configuration settings"""
    
    # Kafka broker connection
    BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
    
    # Topic configuration
    TOPIC_NAME = os.getenv('KAFKA_TOPIC', 'weather_data')
    
    # Producer configuration
    PRODUCER_CONFIG = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'client.id': 'weather-producer',
        'acks': 'all',  # Wait for all replicas to acknowledge
        'retries': 3,
        'compression.type': 'gzip',
        'max.in.flight.requests.per.connection': 1,
        'enable.idempotence': True,
    }
    
    # Consumer configuration
    CONSUMER_CONFIG = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': 'weather-consumer-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'max.poll.records': 500,
    }
    
    # Topic settings
    TOPIC_CONFIG = {
        'num_partitions': 3,
        'replication_factor': 1,
        'retention.ms': 604800000,  # 7 days
    }
    
    @classmethod
    def get_producer_config(cls):
        """Get producer configuration dictionary"""
        return cls.PRODUCER_CONFIG
    
    @classmethod
    def get_consumer_config(cls):
        """Get consumer configuration dictionary"""
        return cls.CONSUMER_CONFIG
    
    @classmethod
    def get_topic_name(cls):
        """Get Kafka topic name"""
        return cls.TOPIC_NAME
