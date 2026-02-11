"""
Helper Functions Module
Các hàm tiện ích chung
"""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import hashlib


def format_timestamp(timestamp: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime object thành string
    
    Args:
        timestamp: Datetime object
        format_str: Format string
    
    Returns:
        Formatted timestamp string
    """
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    return timestamp.strftime(format_str)


def parse_timestamp(timestamp_str: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    """
    Parse timestamp string thành datetime object
    
    Args:
        timestamp_str: Timestamp string
        format_str: Format string
    
    Returns:
        Datetime object
    """
    return datetime.strptime(timestamp_str, format_str)


def get_time_ago(hours: int) -> datetime:
    """
    Lấy timestamp của thời điểm X giờ trước
    
    Args:
        hours: Số giờ
    
    Returns:
        Datetime object
    """
    return datetime.now() - timedelta(hours=hours)


def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Chuyển đổi Celsius sang Fahrenheit
    
    Args:
        celsius: Nhiệt độ Celsius
    
    Returns:
        Nhiệt độ Fahrenheit
    """
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Chuyển đổi Fahrenheit sang Celsius
    
    Args:
        fahrenheit: Nhiệt độ Fahrenheit
    
    Returns:
        Nhiệt độ Celsius
    """
    return (fahrenheit - 32) * 5/9


def kelvin_to_celsius(kelvin: float) -> float:
    """
    Chuyển đổi Kelvin sang Celsius
    
    Args:
        kelvin: Nhiệt độ Kelvin
    
    Returns:
        Nhiệt độ Celsius
    """
    return kelvin - 273.15


def mps_to_kmh(mps: float) -> float:
    """
    Chuyển đổi m/s sang km/h
    
    Args:
        mps: Tốc độ m/s
    
    Returns:
        Tốc độ km/h
    """
    return mps * 3.6


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    Safely parse JSON string
    
    Args:
        json_str: JSON string
        default: Default value nếu parse fail
    
    Returns:
        Parsed object hoặc default
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: str = '{}') -> str:
    """
    Safely convert object to JSON string
    
    Args:
        obj: Object cần convert
        default: Default string nếu convert fail
    
    Returns:
        JSON string
    """
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        return default


def validate_city_name(city: str) -> bool:
    """
    Validate city name
    
    Args:
        city: Tên thành phố
    
    Returns:
        True nếu valid
    """
    if not city or not isinstance(city, str):
        return False
    
    # City name phải có ít nhất 2 ký tự
    if len(city.strip()) < 2:
        return False
    
    return True


def round_number(number: float, decimals: int = 2) -> float:
    """
    Round số với số chữ số thập phân chỉ định
    
    Args:
        number: Số cần round
        decimals: Số chữ số thập phân
    
    Returns:
        Rounded number
    """
    try:
        return round(float(number), decimals)
    except (TypeError, ValueError):
        return 0.0


def generate_hash(data: str) -> str:
    """
    Generate MD5 hash của string
    
    Args:
        data: Input string
    
    Returns:
        MD5 hash
    """
    return hashlib.md5(data.encode()).hexdigest()


def chunks(lst: list, n: int):
    """
    Chia list thành các chunks nhỏ
    
    Args:
        lst: List cần chia
        n: Kích thước mỗi chunk
    
    Yields:
        Chunks of list
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_weather_emoji(weather_main: str) -> str:
    """
    Lấy emoji tương ứng với weather condition
    
    Args:
        weather_main: Weather condition (Clear, Clouds, Rain, etc.)
    
    Returns:
        Weather emoji
    """
    emoji_map = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Fog': '🌫️',
        'Haze': '🌫️',
    }
    
    return emoji_map.get(weather_main, '🌤️')


def get_temperature_level(temp: float) -> str:
    """
    Phân loại mức nhiệt độ
    
    Args:
        temp: Nhiệt độ Celsius
    
    Returns:
        Temperature level
    """
    if temp < 0:
        return 'Freezing'
    elif temp < 10:
        return 'Cold'
    elif temp < 20:
        return 'Cool'
    elif temp < 25:
        return 'Moderate'
    elif temp < 30:
        return 'Warm'
    elif temp < 35:
        return 'Hot'
    else:
        return 'Very Hot'


if __name__ == "__main__":
    # Test helper functions
    print(f"30°C = {celsius_to_fahrenheit(30):.1f}°F")
    print(f"100 m/s = {mps_to_kmh(100):.1f} km/h")
    print(f"Weather emoji for Rain: {get_weather_emoji('Rain')}")
    print(f"25°C is: {get_temperature_level(25)}")
