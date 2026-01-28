from src.config import TEMP_ALERT_THRESHOLD, HUMIDITY_ALERT_THRESHOLD
from src.database import get_connection

def generate_daily_report():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT c.city_name, w.temperature_c, w.humidity, wc.condition_text, w.timestamp_utc
    FROM weather_data w
    JOIN cities c ON w.city_id = c.city_id
    LEFT JOIN weather_conditions wc ON w.condition_id = wc.condition_id
    ORDER BY w.record_id DESC
    LIMIT 10
    """)

    rows = cur.fetchall()
    conn.close()

    alerts = []
    for city, temp, hum, cond, ts in rows:
        if temp is not None and temp > TEMP_ALERT_THRESHOLD:
            alerts.append(f"High temperature alert: {city} ({temp}°C > {TEMP_ALERT_THRESHOLD}°C)")
        if hum is not None and hum > HUMIDITY_ALERT_THRESHOLD:
            alerts.append(f"High humidity alert: {city} ({hum}% > {HUMIDITY_ALERT_THRESHOLD}%)")

    return rows, alerts
