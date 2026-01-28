import sqlite3
from src.config import DB_PATH
from src.logger import logger

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    conn = get_connection()
    cur = conn.cursor()
    logger.info("Setting up database and tables")


    cur.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT NOT NULL,
        country TEXT,
        latitude REAL,
        longitude REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(city_name, country)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_conditions (
        condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition_text TEXT NOT NULL UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER NOT NULL,
        condition_id INTEGER,
        timestamp_utc TEXT NOT NULL,
        temperature_c REAL,
        humidity INTEGER,
        pressure_hpa REAL,
        wind_speed_mps REAL,
        rain_1h_mm REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(city_id) REFERENCES cities(city_id),
        FOREIGN KEY(condition_id) REFERENCES weather_conditions(condition_id)
    )
    """)

    conn.commit()
    conn.close()

def upsert_city(city_name, country, lat, lon):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO cities(city_name, country, latitude, longitude)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(city_name, country) DO UPDATE SET
        latitude=excluded.latitude,
        longitude=excluded.longitude
    """, (city_name, country, lat, lon))

    conn.commit()

    cur.execute("SELECT city_id FROM cities WHERE city_name=? AND country=?", (city_name, country))
    city_id = cur.fetchone()[0]

    conn.close()
    return city_id

def get_or_create_condition(condition_text):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO weather_conditions(condition_text) VALUES (?)", (condition_text,))
    conn.commit()

    cur.execute("SELECT condition_id FROM weather_conditions WHERE condition_text=?", (condition_text,))
    condition_id = cur.fetchone()[0]

    conn.close()
    return condition_id

def insert_weather_record(city_id, condition_id, timestamp_utc, temp, humidity, pressure, wind, rain_1h):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO weather_data(city_id, condition_id, timestamp_utc, temperature_c, humidity, pressure_hpa, wind_speed_mps, rain_1h_mm)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (city_id, condition_id, timestamp_utc, temp, humidity, pressure, wind, rain_1h))

    conn.commit()
    conn.close()
