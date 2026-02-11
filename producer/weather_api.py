import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Da Nang")

URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather():
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "timestamp": data["dt"]
        }

    else:
        print("Error fetching weather:", response.text)
        return None
