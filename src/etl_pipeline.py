from src.api_client import fetch_weather
from src.logger import logger
from src.validators import validate_weather_payload
from src.database import upsert_city, get_or_create_condition, insert_weather_record

def run_etl(cities):
    results = {
        "processed": 0,
        "failed": 0,
        "validation_failed": 0,
        "errors": []
    }
    logger.info("ETL pipeline started")

    for city_name, country_code in cities:
        try:
            logger.info(f"Fetching data for {city_name}")
            payload = fetch_weather(city_name, country_code)

            validation_errors = validate_weather_payload(payload)
            if validation_errors:
                logger.warning(f"Validation failed for {city_name}: {validation_errors}")
                results["validation_failed"] += 1
                results["errors"].append((city_name, "validation", validation_errors))
                continue

            logger.info(f"Data valid for {city_name}, inserting into DB")


            city_id = upsert_city(payload["city_name"], payload["country"], payload["lat"], payload["lon"])
            condition_id = get_or_create_condition(payload["condition_text"])

            insert_weather_record(
                city_id=city_id,
                condition_id=condition_id,
                timestamp_utc=payload["timestamp_utc"],
                temp=payload["temperature_c"],
                humidity=payload["humidity"],
                pressure=payload["pressure_hpa"],
                wind=payload["wind_speed_mps"],
                rain_1h=payload["rain_1h_mm"]
            )

            results["processed"] += 1

        except Exception as e:
            results["failed"] += 1
            results["errors"].append((city_name, "api_or_db", str(e)))
            logger.error(f"Error processing {city_name}: {e}")

    logger.info("ETL pipeline completed")
    return results
