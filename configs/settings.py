import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Weather API
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_URL = os.getenv("WEATHER_API_URL")
    CITY = os.getenv("CITY")

    # Kafka
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    # MySQL
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    # Spark
    SPARK_APP_NAME = os.getenv("SPARK_APP_NAME")
    SPARK_MASTER = os.getenv("SPARK_MASTER")


settings = Settings()
