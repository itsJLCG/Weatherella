"""Simple Flask API to serve the frontend and expose weather endpoints."""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

# ensure we can import the backend package from project root
from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from backend.openweather_client import get_current_weather_for_city
from backend.predictor import should_bring_umbrella

app = Flask(__name__, static_folder=str(project_root.parent / 'frontend'), static_url_path='/')
CORS(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/cities')
def cities():
    # curated list of Philippine cities (id is what frontend will send)
    cities = [
        {"id": "Manila,PH", "name": "Manila"},
        {"id": "Quezon City,PH", "name": "Quezon City"},
        {"id": "Davao,PH", "name": "Davao"},
        {"id": "Cebu,PH", "name": "Cebu"},
        {"id": "Taguig,PH", "name": "Taguig"},
        {"id": "Makati,PH", "name": "Makati"},
        {"id": "Pasig,PH", "name": "Pasig"},
        {"id": "Iloilo,PH", "name": "Iloilo"},
        {"id": "Baguio,PH", "name": "Baguio"},
    ]
    return jsonify(cities)


@app.route('/api/weather')
def weather():
    city = request.args.get('city') or request.args.get('q')
    if not city:
        return jsonify({"error": "city parameter is required"}), 400
    try:
        data = get_current_weather_for_city(city)
        # add umbrella recommendation
        recommendation = should_bring_umbrella(data)
        data['umbrella_recommendation'] = recommendation
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Load .env if present
    from dotenv import load_dotenv
    load_dotenv(str(project_root.parent / '.env'))
    app.run(debug=True)
