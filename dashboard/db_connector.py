"""
Database Connector Module
Kết nối và query database cho dashboard
"""

import sys
import os
from typing import List, Dict, Optional
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.mysql_config import MySQLConfig
from database.models import WeatherData, WeatherAggregated, City


class DatabaseConnector:
    """Database connector cho dashboard"""
    
    def __init__(self):
        """Initialize database connection"""
        self.connection_string = MySQLConfig.get_connection_string()
        self.engine = create_engine(
            self.connection_string,
            pool_size=MySQLConfig.POOL_SIZE,
            pool_recycle=MySQLConfig.POOL_RECYCLE,
            echo=False
        )
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_latest_weather(self, limit: int = 100) -> List[Dict]:
        """
        Lấy dữ liệu thời tiết mới nhất
        
        Args:
            limit: Số lượng records tối đa
        
        Returns:
            List of weather dictionaries
        """
        query = f"""
        SELECT 
            city,
            timestamp,
            temperature,
            feels_like,
            humidity,
            weather_main,
            weather_description,
            wind_speed,
            pressure,
            clouds
        FROM weather_data
        ORDER BY timestamp DESC
        LIMIT {limit}
        """
        
        result = self.session.execute(text(query))
        rows = result.fetchall()
        
        return [dict(row._mapping) for row in rows]
    
    def get_weather_by_city(self, city: str, hours: int = 24) -> List[Dict]:
        """
        Lấy dữ liệu thời tiết theo city trong khoảng thời gian
        
        Args:
            city: Tên thành phố
            hours: Số giờ lấy data về trước
        
        Returns:
            List of weather dictionaries
        """
        time_ago = datetime.now() - timedelta(hours=hours)
        
        query = """
        SELECT *
        FROM weather_data
        WHERE city = :city 
        AND timestamp >= :time_ago
        ORDER BY timestamp ASC
        """
        
        result = self.session.execute(
            text(query),
            {"city": city, "time_ago": time_ago}
        )
        rows = result.fetchall()
        
        return [dict(row._mapping) for row in rows]
    
    def get_all_cities(self) -> List[str]:
        """
        Lấy danh sách tất cả cities có trong database
        
        Returns:
            List of city names
        """
        query = """
        SELECT DISTINCT city
        FROM weather_data
        ORDER BY city
        """
        
        result = self.session.execute(text(query))
        rows = result.fetchall()
        
        return [row[0] for row in rows]
    
    def get_weather_statistics(self, city: str, hours: int = 24) -> Dict:
        """
        Lấy thống kê dữ liệu thời tiết
        
        Args:
            city: Tên thành phố
            hours: Số giờ tính thống kê
        
        Returns:
            Dictionary chứa statistics
        """
        time_ago = datetime.now() - timedelta(hours=hours)
        
        query = """
        SELECT 
            COUNT(*) as record_count,
            AVG(temperature) as avg_temp,
            MAX(temperature) as max_temp,
            MIN(temperature) as min_temp,
            AVG(humidity) as avg_humidity,
            AVG(wind_speed) as avg_wind_speed,
            AVG(pressure) as avg_pressure
        FROM weather_data
        WHERE city = :city 
        AND timestamp >= :time_ago
        """
        
        result = self.session.execute(
            text(query),
            {"city": city, "time_ago": time_ago}
        )
        row = result.fetchone()
        
        if row:
            return dict(row._mapping)
        return {}
    
    def get_temperature_trend(self, city: str, hours: int = 24) -> List[Dict]:
        """
        Lấy xu hướng nhiệt độ theo thời gian
        
        Args:
            city: Tên thành phố
            hours: Số giờ lấy data
        
        Returns:
            List of {timestamp, temperature} dictionaries
        """
        time_ago = datetime.now() - timedelta(hours=hours)
        
        query = """
        SELECT 
            timestamp,
            temperature,
            humidity,
            wind_speed
        FROM weather_data
        WHERE city = :city 
        AND timestamp >= :time_ago
        ORDER BY timestamp ASC
        """
        
        result = self.session.execute(
            text(query),
            {"city": city, "time_ago": time_ago}
        )
        rows = result.fetchall()
        
        return [dict(row._mapping) for row in rows]
    
    def get_comparison_data(self, cities: List[str]) -> List[Dict]:
        """
        Lấy dữ liệu để so sánh giữa các cities
        
        Args:
            cities: List tên các thành phố
        
        Returns:
            List of comparison data
        """
        if not cities:
            return []
        
        placeholders = ', '.join([f':city{i}' for i in range(len(cities))])
        params = {f'city{i}': city for i, city in enumerate(cities)}
        
        query = f"""
        SELECT 
            city,
            AVG(temperature) as avg_temp,
            AVG(humidity) as avg_humidity,
            AVG(wind_speed) as avg_wind_speed,
            COUNT(*) as data_points
        FROM weather_data
        WHERE city IN ({placeholders})
        AND timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
        GROUP BY city
        """
        
        result = self.session.execute(text(query), params)
        rows = result.fetchall()
        
        return [dict(row._mapping) for row in rows]
    
    def close(self):
        """Close database connection"""
        self.session.close()
        self.engine.dispose()


if __name__ == "__main__":
    # Test database connector
    db = DatabaseConnector()
    
    print("Available cities:")
    cities = db.get_all_cities()
    print(cities)
    
    if cities:
        city = cities[0]
        print(f"\nLatest weather for {city}:")
        weather = db.get_weather_by_city(city, hours=1)
        if weather:
            print(f"Temperature: {weather[0]['temperature']}°C")
            print(f"Humidity: {weather[0]['humidity']}%")
    
    db.close()
