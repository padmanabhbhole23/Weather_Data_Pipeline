import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_PATH = os.getenv("DB_PATH", "database/weather_data.db")

DEFAULT_CITIES = [
    ("Mumbai", "IN"),
    ("Delhi", "IN"),
    ("Bangalore", "IN"),
    ("Chennai", "IN"),
    ("Kolkata", "IN")
]

TEMP_ALERT_THRESHOLD = 30.0
HUMIDITY_ALERT_THRESHOLD = 75
