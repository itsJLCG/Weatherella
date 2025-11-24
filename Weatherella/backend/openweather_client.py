"""OpenWeatherMap client for current weather data (Philippines-focused helpers).

This module provides:
- geocode_city(name, country='PH') -> (lat, lon)
- get_current_weather(lat, lon, units='metric') -> dict with mapped fields

It expects an environment variable OPENWEATHER_API_KEY to be set.
"""
import os
import requests
from typing import Dict, Any, Optional, List, Tuple

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    API_KEY = None

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def _require_api_key():
    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is not set in environment")


def geocode_city(name: str, country: str = "PH", limit: int = 1) -> Tuple[float, float]:
    _require_api_key()
    params = {"q": f"{name},{country}", "limit": limit, "appid": API_KEY}
    r = requests.get(GEOCODE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data:
        raise ValueError(f"Location not found: {name}, {country}")
    first = data[0]
    return float(first["lat"]), float(first["lon"])


def _safe_get(d: Dict, *keys, default=None):
    cur = d
    for k in keys:
        if cur is None:
            return default
        cur = cur.get(k) if isinstance(cur, dict) else None
    return cur if cur is not None else default


def get_coordinates_for_city(city_name: str) -> Tuple[float, float]:
    """Get latitude and longitude for a city name"""
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY is not set in environment")
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    if not data:
        raise ValueError(f"No location found for {city_name}")
    
    return data[0]["lat"], data[0]["lon"]


def get_uv_index(lat: float, lon: float) -> Optional[float]:
    """Get UV index for coordinates"""
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return None
    
    try:
        # UV Index endpoint (free for current UV)
        url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("value")
    except Exception as e:
        print(f"UV Index fetch error: {e}")
        return None


def get_current_weather_for_city(city_name: str) -> Dict[str, Any]:
    """Get current weather for a city"""
    lat, lon = get_coordinates_for_city(city_name)
    
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY is not set in environment")
    
    # Use the free Current Weather API endpoint
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Fetch UV index separately
    uv_index = get_uv_index(lat, lon)
    
    # Map the free API structure to match the expected fields
    weather_data = {
        "dt": data.get("dt"),
        "sunrise": data.get("sys", {}).get("sunrise"),
        "sunset": data.get("sys", {}).get("sunset"),
        "temp": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "pressure": data.get("main", {}).get("pressure"),
        "humidity": data.get("main", {}).get("humidity"),
        "dew_point": None,  # Not available in free API
        "clouds": data.get("clouds", {}).get("all"),
        "uvi": uv_index,  # Fetched from UV Index endpoint
        "visibility": data.get("visibility"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "wind_gust": data.get("wind", {}).get("gust"),
        "wind_deg": data.get("wind", {}).get("deg"),
        "rain": data.get("rain", {}).get("1h") if "rain" in data else None,
        "snow": data.get("snow", {}).get("1h") if "snow" in data else None,
        "weather": data.get("weather", [{}])[0] if data.get("weather") else {},
        "city_name": data.get("name"),
        "country": data.get("sys", {}).get("country")
    }
    
    return weather_data
