"""CLI to fetch and display current weather for a Philippine city."""
import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).resolve().parents[2]

# Add project root to sys.path for imports
sys.path.insert(0, str(project_root))

# Load .env file from project root
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from backend.openweather_client import get_current_weather_for_city


def print_weather_data(weather_data):
    """Print weather data in a formatted way"""
    print(f"\nCurrent Weather for {weather_data.get('city_name', 'Unknown')}, {weather_data.get('country', '')}")
    print("-" * 50)
    print(f"Temperature: {weather_data.get('temp', 'N/A')}°C")
    print(f"Feels like: {weather_data.get('feels_like', 'N/A')}°C")
    print(f"Weather: {weather_data.get('weather', {}).get('description', 'N/A').title()}")
    print(f"Humidity: {weather_data.get('humidity', 'N/A')}%")
    print(f"Wind: {weather_data.get('wind_speed', 'N/A')} m/s, {weather_data.get('wind_deg', 'N/A')}°")
    print(f"Pressure: {weather_data.get('pressure', 'N/A')} hPa")
    print(f"Visibility: {weather_data.get('visibility', 'N/A')} meters")
    print(f"Cloudiness: {weather_data.get('clouds', 'N/A')}%")

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backend.scripts.get_weather <CityName>")
        return
    
    city_name = sys.argv[1]
    try:
        weather_data = get_current_weather_for_city(city_name)
        print_weather_data(weather_data)
    except Exception as e:
        print(f"Error fetching weather: {e}")

if __name__ == "__main__":
    main()
