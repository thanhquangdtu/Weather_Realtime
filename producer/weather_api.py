"""
Weather API Module
Kết nối và lấy dữ liệu từ OpenWeatherMap API
"""

import requests
import sys
import os
from typing import Dict, Optional
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.settings import Settings
from utils.logger import get_logger

logger = get_logger(__name__)


class WeatherAPI:
    """Weather API client for OpenWeatherMap"""
    
    def __init__(self, api_key: str = None, api_url: str = None):
        """
        Initialize Weather API client
        
        Args:
            api_key: OpenWeatherMap API key
            api_url: Base URL for weather API
        """
        self.api_key = api_key or Settings.WEATHER_API_KEY
        self.api_url = api_url or Settings.WEATHER_API_URL
        
        if not self.api_key:
            raise ValueError("Weather API key is required")
        
        logger.info("Weather API client initialized")
    
    def get_weather(self, city: str, units: str = 'metric') -> Optional[Dict]:
        """
        Lấy dữ liệu thời tiết cho một thành phố
        
        Args:
            city: Tên thành phố
            units: Đơn vị đo (metric/imperial/standard)
        
        Returns:
            Dictionary chứa dữ liệu thời tiết hoặc None nếu lỗi
        """
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units
            }
            
            logger.info(f"Fetching weather data for {city}")
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            weather_data = self._parse_weather_data(data, city)
            
            logger.info(f"Successfully fetched weather data for {city}")
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather for {city}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {city}: {str(e)}")
            return None
    
    def _parse_weather_data(self, raw_data: Dict, city: str) -> Dict:
        """
        Parse và chuẩn hóa dữ liệu thời tiết
        
        Args:
            raw_data: Dữ liệu thô từ API
            city: Tên thành phố
        
        Returns:
            Dictionary chứa dữ liệu đã được chuẩn hóa
        """
        try:
            parsed_data = {
                'city': city,
                'timestamp': datetime.utcnow().isoformat(),
                'temperature': raw_data['main']['temp'],
                'feels_like': raw_data['main']['feels_like'],
                'temp_min': raw_data['main']['temp_min'],
                'temp_max': raw_data['main']['temp_max'],
                'pressure': raw_data['main']['pressure'],
                'humidity': raw_data['main']['humidity'],
                'weather_main': raw_data['weather'][0]['main'],
                'weather_description': raw_data['weather'][0]['description'],
                'wind_speed': raw_data['wind']['speed'],
                'wind_deg': raw_data['wind'].get('deg', 0),
                'clouds': raw_data['clouds']['all'],
                'country': raw_data['sys']['country'],
                'sunrise': raw_data['sys']['sunrise'],
                'sunset': raw_data['sys']['sunset'],
                'timezone': raw_data['timezone'],
                'visibility': raw_data.get('visibility', 0),
            }
            
            # Thêm rain data nếu có
            if 'rain' in raw_data:
                parsed_data['rain_1h'] = raw_data['rain'].get('1h', 0)
                parsed_data['rain_3h'] = raw_data['rain'].get('3h', 0)
            else:
                parsed_data['rain_1h'] = 0
                parsed_data['rain_3h'] = 0
            
            return parsed_data
            
        except KeyError as e:
            logger.error(f"Missing key in weather data: {str(e)}")
            raise
    
    def get_multiple_cities(self, cities: list) -> list:
        """
        Lấy dữ liệu thời tiết cho nhiều thành phố
        
        Args:
            cities: List tên các thành phố
        
        Returns:
            List các dictionary chứa dữ liệu thời tiết
        """
        weather_data_list = []
        
        for city in cities:
            weather_data = self.get_weather(city)
            if weather_data:
                weather_data_list.append(weather_data)
        
        logger.info(f"Fetched weather for {len(weather_data_list)}/{len(cities)} cities")
        return weather_data_list


if __name__ == "__main__":
    # Test the API
    api = WeatherAPI()
    
    # Test single city
    weather = api.get_weather("Hanoi")
    if weather:
        print(f"Weather in Hanoi: {weather['temperature']}°C, {weather['weather_description']}")
    
    # Test multiple cities
    cities = Settings.get_cities()
    all_weather = api.get_multiple_cities(cities)
    print(f"\nFetched weather for {len(all_weather)} cities")
