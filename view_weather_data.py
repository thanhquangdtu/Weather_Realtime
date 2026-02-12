"""
Script hiển thị đầy đủ thông tin thời tiết từ MySQL
"""

import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# MySQL configuration
mysql_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3307)),
    'user': os.getenv('MYSQL_USER', 'weather_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'weather_pass'),
    'database': os.getenv('MYSQL_DATABASE', 'weather_db'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

try:
    connection = pymysql.connect(**mysql_config)
    print("=" * 100)
    print("WEATHER DATA - FULL INFORMATION")
    print("=" * 100)
    
    with connection.cursor() as cursor:
        # Lấy 5 records mới nhất
        cursor.execute("""
            SELECT 
                city, 
                timestamp,
                temperature, 
                feels_like,
                humidity, 
                pressure,
                wind_speed,
                wind_deg,
                clouds,
                weather_main,
                weather_description,
                visibility,
                rain_1h,
                rain_3h
            FROM weather_data 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        records = cursor.fetchall()
        
        if records:
            for i, record in enumerate(records, 1):
                print(f"\n{'='*100}")
                print(f"RECORD #{i} - {record['city']} ({record['timestamp']})")
                print(f"{'='*100}")
                print(f"  Temperature:    {record['temperature']}C (Feels like: {record['feels_like']}C)")
                print(f"  Humidity:       {record['humidity']}%")
                print(f"  Pressure:       {record['pressure']} hPa")
                print(f"  Wind:           {record['wind_speed']} m/s (Direction: {record['wind_deg']} degrees)")
                print(f"  Clouds:         {record['clouds']}%")
                print(f"  Visibility:     {record['visibility']} meters")
                print(f"  Weather:        {record['weather_main']} - {record['weather_description']}")
                if record['rain_1h'] and record['rain_1h'] > 0:
                    print(f"  Rain (1h):      {record['rain_1h']} mm")
                if record['rain_3h'] and record['rain_3h'] > 0:
                    print(f"  Rain (3h):      {record['rain_3h']} mm")
            
            print(f"\n{'='*100}")
            print("SUMMARY BY CITY")
            print(f"{'='*100}")
            
            # Statistics by city
            cursor.execute("""
                SELECT 
                    city,
                    COUNT(*) as total_records,
                    ROUND(AVG(temperature), 2) as avg_temp,
                    ROUND(MAX(temperature), 2) as max_temp,
                    ROUND(MIN(temperature), 2) as min_temp,
                    ROUND(AVG(humidity), 0) as avg_humidity,
                    ROUND(AVG(wind_speed), 2) as avg_wind,
                    MAX(timestamp) as latest_update
                FROM weather_data 
                GROUP BY city
                ORDER BY city
            """)
            stats = cursor.fetchall()
            
            for stat in stats:
                print(f"\n{stat['city']}:")
                print(f"  Records: {stat['total_records']}")
                print(f"  Temperature: {stat['avg_temp']}C (Min: {stat['min_temp']}C, Max: {stat['max_temp']}C)")
                print(f"  Avg Humidity: {stat['avg_humidity']}%")
                print(f"  Avg Wind: {stat['avg_wind']} m/s")
                print(f"  Latest Update: {stat['latest_update']}")
        
        else:
            print("\nNo data found in database.")
    
    connection.close()
    print(f"\n{'='*100}")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
