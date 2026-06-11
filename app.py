import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from src.database import setup_database, get_connection
from src.etl_pipeline import run_etl
from src.config import TEMP_ALERT_THRESHOLD, HUMIDITY_ALERT_THRESHOLD

app = Flask(__name__)

def get_dashboard_data():
    conn = get_connection()
    cur = conn.cursor()

    # Latest record per city
    cur.execute("""
        SELECT c.city_name, w.temperature_c, w.humidity, wc.condition_text,
               w.wind_speed_mps, w.pressure_hpa, w.rain_1h_mm, w.timestamp_utc
        FROM weather_data w
        JOIN cities c ON w.city_id = c.city_id
        LEFT JOIN weather_conditions wc ON w.condition_id = wc.condition_id
        WHERE w.record_id IN (
            SELECT MAX(record_id) FROM weather_data GROUP BY city_id
        )
        ORDER BY c.city_name
    """)
    latest = cur.fetchall()

    # All records for history (last 20)
    cur.execute("""
        SELECT c.city_name, w.temperature_c, w.humidity, wc.condition_text, w.timestamp_utc
        FROM weather_data w
        JOIN cities c ON w.city_id = c.city_id
        LEFT JOIN weather_conditions wc ON w.condition_id = wc.condition_id
        ORDER BY w.record_id DESC
        LIMIT 20
    """)
    history = cur.fetchall()

    # Run summary stats
    cur.execute("SELECT COUNT(*) FROM weather_data")
    total_records = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT city_id) FROM weather_data")
    total_cities = cur.fetchone()[0]

    conn.close()

    alerts = []
    for city, temp, hum, cond, wind, pres, rain, ts in latest:
        if temp is not None and temp > TEMP_ALERT_THRESHOLD:
            alerts.append({"type": "temperature", "city": city,
                           "msg": f"High temperature: {temp:.1f}°C > {TEMP_ALERT_THRESHOLD}°C"})
        if hum is not None and hum > HUMIDITY_ALERT_THRESHOLD:
            alerts.append({"type": "humidity", "city": city,
                           "msg": f"High humidity: {hum}% > {HUMIDITY_ALERT_THRESHOLD}%"})

    return {
        "latest": latest,
        "history": history,
        "alerts": alerts,
        "total_records": total_records,
        "total_cities": total_cities,
        "temp_threshold": TEMP_ALERT_THRESHOLD,
        "hum_threshold": HUMIDITY_ALERT_THRESHOLD,
    }


@app.route("/")
def index():
    setup_database()
    data = get_dashboard_data()
    return render_template("index.html", **data)


@app.route("/api/fetch-city", methods=["POST"])
def fetch_city():
    city_name = request.json.get("city", "").strip()
    if not city_name:
        return jsonify({"success": False, "error": "City name is required"}), 400

    # Try to detect country code if provided as "City, CC"
    parts = [p.strip() for p in city_name.split(",")]
    name = parts[0]
    country = parts[1].upper() if len(parts) > 1 else "IN"

    try:
        result = run_etl([(name, country)])
        if result["failed"] > 0:
            return jsonify({"success": False, "error": f"Could not fetch weather for '{name}'. Check city name and try again."})
        if result["validation_failed"] > 0:
            return jsonify({"success": False, "error": f"Data validation failed for '{name}'."})

        # Get the just-inserted record
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.city_name, w.temperature_c, w.humidity, wc.condition_text,
                   w.wind_speed_mps, w.pressure_hpa, w.rain_1h_mm, w.timestamp_utc
            FROM weather_data w
            JOIN cities c ON w.city_id = c.city_id
            LEFT JOIN weather_conditions wc ON w.condition_id = wc.condition_id
            WHERE c.city_name = ? ORDER BY w.record_id DESC LIMIT 1
        """, (name,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return jsonify({"success": False, "error": "Data fetched but could not retrieve record."})

        city, temp, hum, cond, wind, pres, rain, ts = row
        alerts = []
        if temp is not None and temp > TEMP_ALERT_THRESHOLD:
            alerts.append(f"High temperature: {temp:.1f}°C > {TEMP_ALERT_THRESHOLD}°C")
        if hum is not None and hum > HUMIDITY_ALERT_THRESHOLD:
            alerts.append(f"High humidity: {hum}% > {HUMIDITY_ALERT_THRESHOLD}%")

        return jsonify({
            "success": True,
            "city": city,
            "temperature": round(temp, 2) if temp else None,
            "humidity": hum,
            "condition": cond,
            "wind_speed": round(wind, 2) if wind else None,
            "pressure": round(pres, 1) if pres else None,
            "rain_1h": rain,
            "timestamp": ts,
            "alerts": alerts
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/refresh", methods=["POST"])
def refresh():
    """Re-run ETL for default cities."""
    from src.config import DEFAULT_CITIES
    try:
        result = run_etl(DEFAULT_CITIES)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    setup_database()
    app.run(debug=True, port=5000)
