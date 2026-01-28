from src.validators import validate_weather_payload

def test_valid_temperature():
    payload = {
        "temperature_c": 25,
        "humidity": 50,
        "pressure_hpa": 1013,
        "wind_speed_mps": 5
    }
    assert validate_weather_payload(payload) == []
