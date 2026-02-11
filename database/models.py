"""
Database Models Module
SQLAlchemy models cho weather database
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, 
    BigInteger, Boolean, Text, DECIMAL, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class WeatherData(Base):
    """Model cho bảng weather_data"""
    
    __tablename__ = 'weather_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    temperature = Column(DECIMAL(5, 2), nullable=False)
    feels_like = Column(DECIMAL(5, 2))
    temp_min = Column(DECIMAL(5, 2))
    temp_max = Column(DECIMAL(5, 2))
    pressure = Column(Integer)
    humidity = Column(Integer)
    weather_main = Column(String(50))
    weather_description = Column(String(100))
    wind_speed = Column(DECIMAL(5, 2))
    wind_deg = Column(Integer)
    clouds = Column(Integer)
    country = Column(String(10))
    sunrise = Column(BigInteger)
    sunset = Column(BigInteger)
    timezone = Column(Integer)
    visibility = Column(Integer)
    rain_1h = Column(DECIMAL(5, 2), default=0)
    rain_3h = Column(DECIMAL(5, 2), default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<WeatherData(city={self.city}, temp={self.temperature}, timestamp={self.timestamp})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'city': self.city,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'temperature': float(self.temperature) if self.temperature else None,
            'feels_like': float(self.feels_like) if self.feels_like else None,
            'humidity': self.humidity,
            'weather_main': self.weather_main,
            'weather_description': self.weather_description,
            'wind_speed': float(self.wind_speed) if self.wind_speed else None,
        }


class WeatherAggregated(Base):
    """Model cho bảng weather_aggregated"""
    
    __tablename__ = 'weather_aggregated'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False)
    window_start = Column(DateTime, nullable=False, index=True)
    window_end = Column(DateTime, nullable=False)
    avg_temperature = Column(DECIMAL(5, 2))
    max_temperature = Column(DECIMAL(5, 2))
    min_temperature = Column(DECIMAL(5, 2))
    avg_humidity = Column(DECIMAL(5, 2))
    avg_wind_speed = Column(DECIMAL(5, 2))
    record_count = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<WeatherAggregated(city={self.city}, window={self.window_start})>"


class City(Base):
    """Model cho bảng cities"""
    
    __tablename__ = 'cities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(100), nullable=False)
    country_code = Column(String(10), nullable=False)
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    timezone = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<City(name={self.city_name}, country={self.country_code})>"


class WeatherAlert(Base):
    """Model cho bảng weather_alerts"""
    
    __tablename__ = 'weather_alerts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)
    alert_level = Column(String(20), nullable=False)
    message = Column(Text)
    threshold_value = Column(DECIMAL(10, 2))
    actual_value = Column(DECIMAL(10, 2))
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<WeatherAlert(city={self.city}, type={self.alert_type}, level={self.alert_level})>"


# Helper functions
def get_engine(connection_string):
    """Create database engine"""
    return create_engine(connection_string, echo=False)


def create_tables(engine):
    """Create all tables"""
    Base.metadata.create_all(engine)


def drop_tables(engine):
    """Drop all tables"""
    Base.metadata.drop_all(engine)
