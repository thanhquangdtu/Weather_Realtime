"""
Application Settings Module
Cấu hình chung cho toàn bộ ứng dụng
"""

import os
from dotenv import load_dotenv
from typing import List

load_dotenv()


class Settings:
    """General application settings"""
    
    # Application metadata
    APP_NAME = "Weather Real-time Data Pipeline"
    APP_VERSION = "1.0.0"
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Weather API settings
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'https://api.openweathermap.org/data/2.5/weather')
    
    # Cities to monitor
    CITIES = os.getenv('CITIES', 'Hanoi,Ho Chi Minh City,Da Nang').split(',')
    
    # Data collection interval (seconds)
    COLLECTION_INTERVAL = int(os.getenv('COLLECTION_INTERVAL', 300))  # 5 minutes
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'logs/app.log'
    
    # Spark configuration
    SPARK_APP_NAME = os.getenv('SPARK_APP_NAME', 'WeatherStreamProcessing')
    SPARK_MASTER_URL = os.getenv('SPARK_MASTER_URL', 'spark://localhost:7077')
    
    # Batch processing settings
    BATCH_INTERVAL = int(os.getenv('BATCH_INTERVAL', 60))  # Process every 60 seconds
    CHECKPOINT_DIR = 'checkpoints/spark'
    
    # Dashboard settings
    DASHBOARD_HOST = os.getenv('DASHBOARD_HOST', '0.0.0.0')
    DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', 8050))
    DASHBOARD_DEBUG = os.getenv('DASHBOARD_DEBUG', 'False').lower() == 'true'
    
    # Data retention
    DATA_RETENTION_DAYS = int(os.getenv('DATA_RETENTION_DAYS', 30))
    
    @classmethod
    def get_cities(cls) -> List[str]:
        """Get list of cities to monitor"""
        return [city.strip() for city in cls.CITIES]
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() == 'production'
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration"""
        if not cls.WEATHER_API_KEY:
            print("WARNING: WEATHER_API_KEY is not set!")
            return False
        
        if not cls.CITIES:
            raise ValueError("At least one city must be specified")
        
        return True


# Validate configuration on import
try:
    Settings.validate_config()
except Exception as e:
    print(f"Configuration validation warning: {e}")
