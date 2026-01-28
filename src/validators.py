def validate_weather_payload(p):
    errors = []

    if p["temperature_c"] < -80 or p["temperature_c"] > 60:
        errors.append("temperature_out_of_range")

    if p["humidity"] < 0 or p["humidity"] > 100:
        errors.append("humidity_out_of_range")

    if p["pressure_hpa"] < 800 or p["pressure_hpa"] > 1200:
        errors.append("pressure_out_of_range")

    if p["wind_speed_mps"] < 0 or p["wind_speed_mps"] > 100:
        errors.append("wind_out_of_range")

    return errors

