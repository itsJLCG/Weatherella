from backend.openweather_client import map_current


def sample_current():
    return {
        "dt": 1697625600,
        "sunrise": 1697584800,
        "sunset": 1697625600,
        "temp": 30.5,
        "feels_like": 33.1,
        "pressure": 1008,
        "humidity": 74,
        "dew_point": 24.0,
        "clouds": 75,
        "uvi": 6.2,
        "visibility": 10000,
        "wind_speed": 3.6,
        "wind_gust": 5.2,
        "wind_deg": 180,
        "rain": {"1h": 0.25},
        "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}],
    }


def test_map_current():
    cur = sample_current()
    mapped = map_current(cur)
    assert mapped.dt == cur["dt"]
    assert mapped.temp == cur["temp"]
    assert mapped.rain_1h == 0.25
    assert mapped.weather["main"] == "Rain"
