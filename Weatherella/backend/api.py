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
from backend.auth import register_user, login_user, token_required, get_user_by_id
from backend.uv_health import get_uv_recommendations
from backend.clothing import get_clothing_recommendations
from backend.user_data import (
    get_user_preferences, save_user_preferences,
    add_favorite_city, remove_favorite_city, get_favorite_cities, is_favorite_city,
    save_weather_search, get_search_history, get_user_statistics, clear_search_history
)

app = Flask(__name__, static_folder=str(project_root.parent / 'frontend'), static_url_path='/')
CORS(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        result = register_user(email, password, name)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred during registration"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        result = login_user(email, password)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "An error occurred during login"}), 500


@app.route('/api/me')
@token_required
def get_current_user():
    """Get current user information."""
    try:
        user = get_user_by_id(request.user['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500


@app.route('/api/cities')
def cities():
    # curated list of Philippine cities (id is what frontend will send)
    cities = [
        {"id": "Manila,PH", "name": "Manila", "lat": 14.5995, "lng": 120.9842},
        {"id": "Quezon City,PH", "name": "Quezon City", "lat": 14.6760, "lng": 121.0437},
        {"id": "Davao,PH", "name": "Davao", "lat": 7.1907, "lng": 125.4553},
        {"id": "Cebu,PH", "name": "Cebu", "lat": 10.3157, "lng": 123.8854},
        {"id": "Taguig,PH", "name": "Taguig", "lat": 14.5176, "lng": 121.0509},
        {"id": "Makati,PH", "name": "Makati", "lat": 14.5547, "lng": 121.0244},
        {"id": "Pasig,PH", "name": "Pasig", "lat": 14.5764, "lng": 121.0851},
        {"id": "Caloocan,PH", "name": "Caloocan", "lat": 14.6488, "lng": 120.9830},
        {"id": "Antipolo,PH", "name": "Antipolo", "lat": 14.5862, "lng": 121.1759},
        {"id": "Baguio,PH", "name": "Baguio", "lat": 16.4023, "lng": 120.5960},
        {"id": "Iloilo,PH", "name": "Iloilo", "lat": 10.7202, "lng": 122.5621},
        {"id": "Zamboanga,PH", "name": "Zamboanga", "lat": 6.9214, "lng": 122.0790},
        {"id": "Cagayan de Oro,PH", "name": "Cagayan de Oro", "lat": 8.4542, "lng": 124.6319},
        {"id": "Bacolod,PH", "name": "Bacolod", "lat": 10.6770, "lng": 122.9500},
        {"id": "General Santos,PH", "name": "General Santos", "lat": 6.1164, "lng": 125.1716},
        {"id": "Parañaque,PH", "name": "Parañaque", "lat": 14.4793, "lng": 121.0198},
        {"id": "Las Piñas,PH", "name": "Las Piñas", "lat": 14.4463, "lng": 120.9832},
        {"id": "Mandaluyong,PH", "name": "Mandaluyong", "lat": 14.5794, "lng": 121.0359},
        {"id": "Muntinlupa,PH", "name": "Muntinlupa", "lat": 14.4081, "lng": 121.0425},
        {"id": "San Juan,PH", "name": "San Juan", "lat": 14.6019, "lng": 121.0355},
        {"id": "Valenzuela,PH", "name": "Valenzuela", "lat": 14.6937, "lng": 120.9830},
        {"id": "Marikina,PH", "name": "Marikina", "lat": 14.6507, "lng": 121.1029},
        {"id": "Navotas,PH", "name": "Navotas", "lat": 14.6628, "lng": 120.9409},
        {"id": "Malabon,PH", "name": "Malabon", "lat": 14.6620, "lng": 120.9604},
        {"id": "Angeles,PH", "name": "Angeles", "lat": 15.1450, "lng": 120.5887},
        {"id": "Olongapo,PH", "name": "Olongapo", "lat": 14.8294, "lng": 120.2825},
        {"id": "Tacloban,PH", "name": "Tacloban", "lat": 11.2447, "lng": 125.0036},
        {"id": "Naga,PH", "name": "Naga", "lat": 13.6218, "lng": 123.1948},
        {"id": "Butuan,PH", "name": "Butuan", "lat": 8.9475, "lng": 125.5406},
        {"id": "Iligan,PH", "name": "Iligan", "lat": 8.2280, "lng": 124.2452},
    ]
    return jsonify(cities)


@app.route('/api/weather')
@token_required
def weather():
    city = request.args.get('city') or request.args.get('q')
    if not city:
        return jsonify({"error": "city parameter is required"}), 400
    try:
        data = get_current_weather_for_city(city)
        
        # Add umbrella recommendation
        recommendation = should_bring_umbrella(data)
        data['umbrella_recommendation'] = recommendation
        
        # Add UV Index recommendations
        uv_index = data.get('uvi')
        if uv_index is not None:
            uv_recommendations = get_uv_recommendations(uv_index)
            data['uv_recommendations'] = uv_recommendations
        else:
            # If UV data not available, provide fallback
            data['uv_recommendations'] = get_uv_recommendations(-1)
        
        # Add clothing recommendations
        clothing_recommendations = get_clothing_recommendations(data)
        data['clothing_recommendations'] = clothing_recommendations
        
        # Save to search history
        try:
            save_weather_search(
                request.user['user_id'],
                city,
                data.get('city_name', city),
                data
            )
        except Exception as e:
            print(f"Error saving search history: {e}")
        
        # Check if city is favorited
        try:
            data['is_favorite'] = is_favorite_city(request.user['user_id'], city)
        except Exception as e:
            print(f"Error checking favorite status: {e}")
            data['is_favorite'] = False
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Preferences Endpoints
@app.route('/api/preferences', methods=['GET'])
@token_required
def get_preferences():
    """Get user preferences."""
    try:
        prefs = get_user_preferences(request.user['user_id'])
        if not prefs:
            # Return default preferences
            prefs = {
                "default_view": "map",
                "default_city": None,
                "temperature_unit": "celsius"
            }
        return jsonify(prefs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/preferences', methods=['POST'])
@token_required
def update_preferences():
    """Update user preferences."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    try:
        success = save_user_preferences(request.user['user_id'], data)
        if success:
            return jsonify({"message": "Preferences updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update preferences"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Favorite Cities Endpoints
@app.route('/api/favorites', methods=['GET'])
@token_required
def get_favorites():
    """Get user's favorite cities."""
    try:
        favorites = get_favorite_cities(request.user['user_id'])
        return jsonify(favorites), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/favorites', methods=['POST'])
@token_required
def add_favorite():
    """Add a city to favorites."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    city_id = data.get('city_id')
    city_name = data.get('city_name')
    lat = data.get('lat')
    lng = data.get('lng')
    
    if not all([city_id, city_name, lat, lng]):
        return jsonify({"error": "city_id, city_name, lat, and lng are required"}), 400
    
    try:
        success = add_favorite_city(
            request.user['user_id'],
            city_id,
            city_name,
            float(lat),
            float(lng)
        )
        if success:
            return jsonify({"message": "City added to favorites"}), 200
        else:
            return jsonify({"error": "Failed to add favorite"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/favorites/<city_id>', methods=['DELETE'])
@token_required
def remove_favorite(city_id):
    """Remove a city from favorites."""
    try:
        success = remove_favorite_city(request.user['user_id'], city_id)
        if success:
            return jsonify({"message": "City removed from favorites"}), 200
        else:
            return jsonify({"error": "Failed to remove favorite"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Search History Endpoints
@app.route('/api/history', methods=['GET'])
@token_required
def get_history():
    """Get user's search history."""
    limit = request.args.get('limit', 20, type=int)
    try:
        history = get_search_history(request.user['user_id'], limit)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/history', methods=['DELETE'])
@token_required
def clear_history():
    """Clear user's search history."""
    try:
        success = clear_search_history(request.user['user_id'])
        if success:
            return jsonify({"message": "Search history cleared"}), 200
        else:
            return jsonify({"error": "Failed to clear history"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User Statistics Endpoint
@app.route('/api/statistics', methods=['GET'])
@token_required
def get_statistics():
    """Get user statistics."""
    try:
        stats = get_user_statistics(request.user['user_id'])
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Load .env if present
    from dotenv import load_dotenv
    load_dotenv(str(project_root.parent / '.env'))
    load_dotenv(str(project_root / 'backend' / '.env'))
    app.run(debug=True)
