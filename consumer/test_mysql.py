"""
Test script để kiểm tra data trong MySQL
"""

import pymysql
import os
from dotenv import load_dotenv

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
    # Kết nối
    connection = pymysql.connect(**mysql_config)
    print("✓ Connected to MySQL successfully\n")
    
    with connection.cursor() as cursor:
        # Đếm số records
        cursor.execute("SELECT COUNT(*) as count FROM weather_data")
        result = cursor.fetchone()
        print(f"📊 Total records in weather_data: {result['count']}")
        
        # Lấy 5 records mới nhất
        cursor.execute("""
            SELECT city, timestamp, temperature, humidity, weather_main 
            FROM weather_data 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        records = cursor.fetchall()
        
        if records:
            print("\n📝 Latest 5 records:")
            print("-" * 80)
            for i, record in enumerate(records, 1):
                print(f"{i}. {record['city']} - {record['timestamp']} - "
                      f"{record['temperature']}°C - {record['humidity']}% - "
                      f"{record['weather_main']}")
            print("-" * 80)
        else:
            print("\n⚠️  No records found in database yet.")
            print("   The consumer is running and waiting for data from Kafka.")
            print(f"   Producer sends data every {os.getenv('COLLECTION_INTERVAL', 300)} seconds.")
    
    connection.close()
    print("\n✓ Database connection closed")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
