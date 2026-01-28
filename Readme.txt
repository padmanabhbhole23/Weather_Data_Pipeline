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

1. pip install -r requirements.txt

