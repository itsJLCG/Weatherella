"""Database helper functions for user data beyond authentication.

This module handles:
- User preferences (default view, temperature units, etc.)
- Favorite cities
- Weather search history
- User statistics
"""
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = client.Weatherella if client else None


def get_user_preferences(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get user preferences from database.
    
    Args:
        user_id: User ID
        
    Returns:
        User preferences dictionary or None
    """
    if db is None:
        return None
    
    prefs = db.user_preferences.find_one({"user_id": user_id})
    if prefs:
        prefs['_id'] = str(prefs['_id'])
    return prefs


def save_user_preferences(user_id: str, preferences: Dict[str, Any]) -> bool:
    """
    Save or update user preferences.
    
    Args:
        user_id: User ID
        preferences: Dictionary of preferences
        
    Returns:
        True if successful
    """
    if not db:
        return False
    
    prefs_data = {
        "user_id": user_id,
        "default_view": preferences.get("default_view", "map"),
        "default_city": preferences.get("default_city"),
        "temperature_unit": preferences.get("temperature_unit", "celsius"),
        "updated_at": datetime.utcnow()
    }
    
    db.user_preferences.update_one(
        {"user_id": user_id},
        {"$set": prefs_data},
        upsert=True
    )
    return True


def add_favorite_city(user_id: str, city_id: str, city_name: str, lat: float, lng: float) -> bool:
    """
    Add a city to user's favorites.
    
    Args:
        user_id: User ID
        city_id: City identifier (e.g., "Manila,PH")
        city_name: Display name
        lat: Latitude
        lng: Longitude
        
    Returns:
        True if successful
    """
    if db is None:
        return False
    
    favorite = {
        "user_id": user_id,
        "city_id": city_id,
        "city_name": city_name,
        "lat": lat,
        "lng": lng,
        "added_at": datetime.utcnow()
    }
    
    # Check if already exists
    existing = db.favorite_cities.find_one({
        "user_id": user_id,
        "city_id": city_id
    })
    
    if existing:
        return True  # Already favorited
    
    db.favorite_cities.insert_one(favorite)
    return True


def remove_favorite_city(user_id: str, city_id: str) -> bool:
    """
    Remove a city from user's favorites.
    
    Args:
        user_id: User ID
        city_id: City identifier
        
    Returns:
        True if successful
    """
    if db is None:
        return False
    
    db.favorite_cities.delete_one({
        "user_id": user_id,
        "city_id": city_id
    })
    return True


def get_favorite_cities(user_id: str) -> List[Dict[str, Any]]:
    """
    Get user's favorite cities.
    
    Args:
        user_id: User ID
        
    Returns:
        List of favorite cities
    """
    if db is None:
        return []
    
    favorites = list(db.favorite_cities.find(
        {"user_id": user_id}
    ).sort("added_at", DESCENDING))
    
    for fav in favorites:
        fav['_id'] = str(fav['_id'])
    
    return favorites


def is_favorite_city(user_id: str, city_id: str) -> bool:
    """
    Check if a city is in user's favorites.
    
    Args:
        user_id: User ID
        city_id: City identifier
        
    Returns:
        True if favorited
    """
    if db is None:
        return False
    
    return db.favorite_cities.find_one({
        "user_id": user_id,
        "city_id": city_id
    }) is not None


def save_weather_search(user_id: str, city_id: str, city_name: str, weather_data: Dict[str, Any]) -> bool:
    """
    Save a weather search to history.
    
    Args:
        user_id: User ID
        city_id: City identifier
        city_name: Display name
        weather_data: Weather data snapshot
        
    Returns:
        True if successful
    """
    if db is None:
        return False
    
    search = {
        "user_id": user_id,
        "city_id": city_id,
        "city_name": city_name,
        "temperature": weather_data.get("temp"),
        "weather_main": weather_data.get("weather", {}).get("main"),
        "weather_description": weather_data.get("weather", {}).get("description"),
        "searched_at": datetime.utcnow()
    }
    
    db.search_history.insert_one(search)
    
    # Keep only last 50 searches per user
    searches = list(db.search_history.find(
        {"user_id": user_id}
    ).sort("searched_at", DESCENDING).skip(50))
    
    if searches:
        ids_to_delete = [s['_id'] for s in searches]
        db.search_history.delete_many({"_id": {"$in": ids_to_delete}})
    
    return True


def get_search_history(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get user's search history.
    
    Args:
        user_id: User ID
        limit: Maximum number of results
        
    Returns:
        List of search history entries
    """
    if db is None:
        return []
    
    history = list(db.search_history.find(
        {"user_id": user_id}
    ).sort("searched_at", DESCENDING).limit(limit))
    
    for entry in history:
        entry['_id'] = str(entry['_id'])
    
    return history


def get_user_statistics(user_id: str) -> Dict[str, Any]:
    """
    Get user statistics.
    
    Args:
        user_id: User ID
        
    Returns:
        Dictionary with user stats
    """
    if db is None:
        return {}
    
    # Count favorites
    favorite_count = db.favorite_cities.count_documents({"user_id": user_id})
    
    # Count searches
    search_count = db.search_history.count_documents({"user_id": user_id})
    
    # Get most searched city
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id": "$city_id",
            "city_name": {"$first": "$city_name"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    
    most_searched = list(db.search_history.aggregate(pipeline))
    most_searched_city = most_searched[0] if most_searched else None
    
    # Get first search date
    first_search = db.search_history.find_one(
        {"user_id": user_id},
        sort=[("searched_at", 1)]
    )
    
    return {
        "favorite_cities_count": favorite_count,
        "total_searches": search_count,
        "most_searched_city": {
            "city_id": most_searched_city["_id"],
            "city_name": most_searched_city["city_name"],
            "count": most_searched_city["count"]
        } if most_searched_city else None,
        "member_since": first_search["searched_at"] if first_search else None
    }


def clear_search_history(user_id: str) -> bool:
    """
    Clear user's search history.
    
    Args:
        user_id: User ID
        
    Returns:
        True if successful
    """
    if db is None:
        return False
    
    db.search_history.delete_many({"user_id": user_id})
    return True
