# Weather Data Pipeline System

## 📌 Project Overview
This project implements an end-to-end Weather Data Pipeline using Python and SQLite.
The system extracts real-time weather data from the OpenWeatherMap API, transforms and validates the data, loads it into a relational database, and generates automated reports and alerts.

## 🎯 Objectives
- Build a complete ETL pipeline
- Store historical weather data in a normalized SQL database
- Perform automated data collection and validation
- Generate analytical reports and alerts
- Demonstrate database and API integration skills

## 🏗️ Architecture Overview
API → ETL Pipeline → SQLite Database → Reports & Alerts

## ⚙️ Tech Stack
- Python
- SQLite
- OpenWeatherMap API
- Requests, Pandas, Schedule

## 🚀 Setup Instructions

### 1. Clone Repository
```bash
git clone <repo-url>
cd Weather_Data_Pipeline


Structure:
weather_pipeline/
│
├── README.md
├── requirements.txt
├── .env
│
├── src/
│   ├── config.py
│   ├── database.py
│   ├── api_client.py
│   ├── validators.py
│   ├── etl_pipeline.py
│   ├── scheduler.py
│   ├── reporter.py
│   ├── monitor.py
│   └── main.py
│
├── logs/
├── reports/
└── database/
    └── weather_data.db



Steps to run:
python -m venv venv
venv\Scripts\activate

1. pip install -r requirements.txt

Change: OPENWEATHER_API_KEY=your_api_key_here
python -m src.main
python -m src.scheduler


---

# 🧾 2️⃣ Database Schema (`database/schema.sql`)

```sql
CREATE TABLE cities (
    city_id INTEGER PRIMARY KEY,
    city_name TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL
);

CREATE TABLE weather_conditions (
    condition_id INTEGER PRIMARY KEY,
    condition_text TEXT UNIQUE
);

CREATE TABLE weather_data (
    record_id INTEGER PRIMARY KEY,
    city_id INTEGER,
    condition_id INTEGER,
    timestamp_utc TEXT,
    temperature_c REAL,
    humidity INTEGER,
    pressure_hpa REAL,
    wind_speed_mps REAL,
    rain_1h_mm REAL,
    FOREIGN KEY(city_id) REFERENCES cities(city_id),
    FOREIGN KEY(condition_id) REFERENCES weather_conditions(condition_id)
);
