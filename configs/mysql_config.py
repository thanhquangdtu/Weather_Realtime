"""
MySQL Configuration Module
Cấu hình kết nối và tương tác với MySQL database
"""

import os
from dotenv import load_dotenv

load_dotenv()


class MySQLConfig:
    """MySQL database configuration settings"""
    
    # Connection parameters
    HOST = os.getenv('MYSQL_HOST', 'localhost')
    PORT = int(os.getenv('MYSQL_PORT', 3307))
    DATABASE = os.getenv('MYSQL_DATABASE', 'weather_db')
    USER = os.getenv('MYSQL_USER', 'weather_user')
    PASSWORD = os.getenv('MYSQL_PASSWORD', 'weather_pass')
    
    # Connection pool settings
    POOL_SIZE = 5
    POOL_RECYCLE = 3600  # Recycle connections after 1 hour
    POOL_TIMEOUT = 30
    MAX_OVERFLOW = 10
    
    # Connection string
    @classmethod
    def get_connection_string(cls):
        """Get MySQL connection string for SQLAlchemy"""
        return f"mysql+pymysql://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}"
    
    @classmethod
    def get_connection_params(cls):
        """Get connection parameters as dictionary"""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
        }
    
    @classmethod
    def get_pool_config(cls):
        """Get connection pool configuration"""
        return {
            'pool_size': cls.POOL_SIZE,
            'pool_recycle': cls.POOL_RECYCLE,
            'pool_timeout': cls.POOL_TIMEOUT,
            'max_overflow': cls.MAX_OVERFLOW,
        }
    
    # JDBC URL for Spark
    @classmethod
    def get_jdbc_url(cls):
        """Get JDBC URL for Spark connections"""
        return f"jdbc:mysql://{cls.HOST}:{cls.PORT}/{cls.DATABASE}"
    
    @classmethod
    def get_jdbc_properties(cls):
        """Get JDBC connection properties"""
        return {
            'user': cls.USER,
            'password': cls.PASSWORD,
            'driver': 'com.mysql.cj.jdbc.Driver',
        }
