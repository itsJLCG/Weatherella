Backend for Weatherella — OpenWeatherMap client

This package provides a small Python client to fetch current weather data for cities in the Philippines using OpenWeatherMap APIs (Geocoding + One Call / Current). It maps the returned JSON into a friendly structure that includes the fields requested.

Usage:

- Copy `.env.example` to `.env` and set `OPENWEATHER_API_KEY`.
- Install requirements: `pip install -r requirements.txt`.
- Run CLI: `python -m backend.scripts.get_weather Manila` (or use the module path shown below).

Files:
- `backend/openweather_client.py` - the core client
- `backend/scripts/get_weather.py` - simple CLI
- `requirements.txt` - Python deps
- `tests/test_parser.py` - unit tests for response mapping
