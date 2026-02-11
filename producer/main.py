"""
Main Producer Application
Ứng dụng chính để thu thập và gửi dữ liệu thời tiết vào Kafka
"""

import sys
import os
import time
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_api import WeatherAPI
from kafka_producer import WeatherKafkaProducer
from configs.settings import Settings
from utils.logger import get_logger

logger = get_logger(__name__)


class WeatherProducerApp:
    """Main application để produce weather data vào Kafka"""
    
    def __init__(self):
        """Initialize producer application"""
        self.weather_api = WeatherAPI()
        self.kafka_producer = WeatherKafkaProducer()
        self.cities = Settings.get_cities()
        self.interval = Settings.COLLECTION_INTERVAL
        
        logger.info(f"Weather Producer initialized for cities: {', '.join(self.cities)}")
        logger.info(f"Collection interval: {self.interval} seconds")
    
    def collect_and_send(self):
        """Thu thập dữ liệu và gửi vào Kafka"""
        try:
            logger.info("Starting data collection...")
            
            for city in self.cities:
                # Lấy dữ liệu thời tiết
                weather_data = self.weather_api.get_weather(city)
                
                if weather_data:
                    # Gửi vào Kafka
                    success = self.kafka_producer.send_weather_data(weather_data)
                    
                    if success:
                        logger.info(f"✓ Sent weather data for {city} - Temp: {weather_data['temperature']}°C")
                    else:
                        logger.error(f"✗ Failed to send data for {city}")
                else:
                    logger.warning(f"✗ No weather data received for {city}")
                
                # Delay nhỏ giữa các requests
                time.sleep(1)
            
            logger.info(f"Data collection completed for {len(self.cities)} cities")
            
        except Exception as e:
            logger.error(f"Error in collect_and_send: {str(e)}", exc_info=True)
    
    def run(self):
        """Chạy producer liên tục"""
        logger.info("=" * 60)
        logger.info("Starting Weather Producer Application")
        logger.info("=" * 60)
        
        try:
            iteration = 0
            while True:
                iteration += 1
                logger.info(f"\n--- Iteration {iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
                
                # Thu thập và gửi dữ liệu
                self.collect_and_send()
                
                # Chờ interval trước khi thu thập tiếp
                logger.info(f"Waiting {self.interval} seconds before next collection...\n")
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            logger.info("\n" + "=" * 60)
            logger.info("Shutting down Weather Producer...")
            logger.info("=" * 60)
            self.shutdown()
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}", exc_info=True)
            self.shutdown()
    
    def shutdown(self):
        """Cleanup resources"""
        try:
            self.kafka_producer.close()
            logger.info("Producer shut down successfully")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")


def main():
    """Main entry point"""
    try:
        app = WeatherProducerApp()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
