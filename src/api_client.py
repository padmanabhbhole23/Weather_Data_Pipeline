import requests
from datetime import datetime, timezone
from src.config import OPENWEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city_name, country_code):
    params = {
        "q": f"{city_name},{country_code}",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    rain_1h = None
    if "rain" in data and "1h" in data["rain"]:
        rain_1h = data["rain"]["1h"]

    return {
        "city_name": city_name,
        "country": country_code,
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "temperature_c": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure_hpa": data["main"]["pressure"],
        "wind_speed_mps": data["wind"]["speed"],
        "condition_text": data["weather"][0]["description"],
        "rain_1h_mm": rain_1h
    }
