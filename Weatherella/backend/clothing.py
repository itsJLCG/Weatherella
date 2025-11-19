"""Clothing recommendation logic based on weather conditions.

Provides personalized clothing suggestions based on:
- Temperature and feels-like temperature
- Weather conditions (rain, clouds, sun)
- Wind speed
- Time of day
"""
from typing import Dict, Any, List


def get_clothing_recommendations(weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate clothing recommendations based on weather data.
    
    Args:
        weather_data: Weather data dictionary with temp, feels_like, weather, etc.
        
    Returns:
        Dictionary with clothing suggestions, layers, and accessories
    """
    temp = weather_data.get('temp', 25)
    feels_like = weather_data.get('feels_like', temp)
    humidity = weather_data.get('humidity', 50)
    wind_speed = weather_data.get('wind_speed', 0)
    weather = weather_data.get('weather', {})
    weather_main = weather.get('main', '').lower()
    weather_desc = weather.get('description', '').lower()
    clouds = weather_data.get('clouds', 0)
    rain = weather_data.get('rain')
    
    # Determine effective temperature (considering feels_like)
    effective_temp = (temp + feels_like) / 2
    
    # Temperature categories
    if effective_temp >= 32:
        category = "Very Hot"
        color = "#dc2626"
        icon = "🔥"
        comfort_level = "Extreme Heat"
    elif effective_temp >= 28:
        category = "Hot"
        color = "#f97316"
        icon = "☀️"
        comfort_level = "Warm & Humid"
    elif effective_temp >= 24:
        category = "Warm"
        color = "#fbbf24"
        icon = "🌤️"
        comfort_level = "Pleasant"
    elif effective_temp >= 20:
        category = "Mild"
        color = "#22c55e"
        icon = "🌥️"
        comfort_level = "Comfortable"
    elif effective_temp >= 16:
        category = "Cool"
        color = "#3b82f6"
        icon = "🌬️"
        comfort_level = "Cool"
    else:
        category = "Cold"
        color = "#6366f1"
        icon = "❄️"
        comfort_level = "Cold"
    
    # Base clothing recommendations
    clothing_items = []
    layers = []
    accessories = []
    tips = []
    
    # Temperature-based recommendations
    if effective_temp >= 32:
        clothing_items = [
            "Light cotton shirt or tank top",
            "Shorts or light skirt",
            "Sandals or breathable shoes"
        ]
        layers = ["Single layer - minimal clothing"]
        accessories = [
            "Wide-brimmed hat for sun protection",
            "Sunglasses (UV protection)",
            "Cooling towel",
            "Water bottle (stay hydrated)"
        ]
        tips = [
            "Wear light-colored, loose-fitting clothes",
            "Choose breathable, moisture-wicking fabrics",
            "Avoid dark colors that absorb heat",
            "Stay indoors during peak heat hours"
        ]
    
    elif effective_temp >= 28:
        clothing_items = [
            "Light t-shirt or blouse",
            "Shorts, skirt, or light pants",
            "Sandals or canvas shoes"
        ]
        layers = ["Single light layer"]
        accessories = [
            "Hat or cap",
            "Sunglasses",
            "Light scarf (for sun protection)",
            "Reusable water bottle"
        ]
        tips = [
            "Choose breathable cotton or linen fabrics",
            "Light colors help reflect heat",
            "Wear loose-fitting clothes for air circulation",
            "Carry a small towel for perspiration"
        ]
    
    elif effective_temp >= 24:
        clothing_items = [
            "T-shirt or casual shirt",
            "Jeans, chinos, or casual pants",
            "Comfortable walking shoes"
        ]
        layers = ["Single layer or light layering"]
        accessories = [
            "Light jacket (optional, for air-conditioned spaces)",
            "Sunglasses",
            "Cap or hat (optional)"
        ]
        tips = [
            "Perfect weather for most activities",
            "Light jacket for indoor air conditioning",
            "Comfortable clothing for all-day wear"
        ]
    
    elif effective_temp >= 20:
        clothing_items = [
            "Long-sleeve shirt or light sweater",
            "Full-length pants or jeans",
            "Closed-toe shoes or sneakers"
        ]
        layers = ["1-2 layers recommended"]
        accessories = [
            "Light jacket or cardigan",
            "Scarf (optional)",
            "Bag for extra layer"
        ]
        tips = [
            "Layer clothing for temperature changes",
            "Bring a light jacket for evening",
            "Comfortable for outdoor activities"
        ]
    
    elif effective_temp >= 16:
        clothing_items = [
            "Sweater or hoodie",
            "Long pants or jeans",
            "Closed shoes with socks"
        ]
        layers = ["2-3 layers recommended"]
        accessories = [
            "Jacket or windbreaker",
            "Scarf",
            "Light gloves (optional)"
        ]
        tips = [
            "Multiple layers for warmth",
            "Windproof outer layer recommended",
            "Cover extremities (neck, hands)"
        ]
    
    else:  # < 16°C
        clothing_items = [
            "Warm sweater or thermal top",
            "Heavy pants or lined jeans",
            "Warm boots or closed shoes"
        ]
        layers = ["3+ layers recommended"]
        accessories = [
            "Warm jacket or coat",
            "Scarf and beanie",
            "Gloves",
            "Warm socks"
        ]
        tips = [
            "Dress in layers to trap warmth",
            "Cover all exposed skin",
            "Insulated, windproof outer layer essential"
        ]
    
    # Add rain-specific items
    if rain or 'rain' in weather_main or 'rain' in weather_desc:
        accessories.insert(0, "☂️ Umbrella (essential)")
        accessories.insert(1, "Waterproof jacket or raincoat")
        if "sandal" in str(clothing_items).lower():
            clothing_items.append("Water-resistant footwear recommended")
        tips.insert(0, "Waterproof or water-resistant clothing recommended")
    
    # Add wind-specific recommendations
    if wind_speed > 5:
        accessories.append("Windbreaker or wind-resistant jacket")
        tips.append(f"Windy conditions ({wind_speed} m/s) - secure loose items")
    
    # Add sun protection for clear/partly cloudy days
    if clouds < 50 and effective_temp > 24:
        if "Sunglasses" not in accessories:
            accessories.append("Sunglasses for sun protection")
        tips.append("High UV exposure - apply sunscreen")
    
    # High humidity adjustments
    if humidity > 75:
        tips.append(f"High humidity ({humidity}%) - choose moisture-wicking fabrics")
    
    return {
        "category": category,
        "color": color,
        "icon": icon,
        "comfort_level": comfort_level,
        "temperature": {
            "actual": round(temp, 1),
            "feels_like": round(feels_like, 1),
            "effective": round(effective_temp, 1)
        },
        "clothing_items": clothing_items,
        "layers": layers,
        "accessories": accessories,
        "tips": tips,
        "conditions": {
            "rain": bool(rain or 'rain' in weather_main),
            "windy": wind_speed > 5,
            "humid": humidity > 75,
            "sunny": clouds < 50
        }
    }


def get_outfit_suggestion(weather_data: Dict[str, Any]) -> str:
    """
    Get a simple outfit suggestion sentence.
    
    Args:
        weather_data: Weather data dictionary
        
    Returns:
        String with outfit suggestion
    """
    temp = weather_data.get('temp', 25)
    feels_like = weather_data.get('feels_like', temp)
    effective_temp = (temp + feels_like) / 2
    rain = weather_data.get('rain')
    weather = weather_data.get('weather', {})
    weather_main = weather.get('main', '').lower()
    
    if effective_temp >= 32:
        outfit = "Wear minimal, light-colored clothing. Stay cool and hydrated!"
    elif effective_temp >= 28:
        outfit = "Light, breathable clothes recommended. Stay comfortable in the heat."
    elif effective_temp >= 24:
        outfit = "Casual comfortable clothing is perfect for today's weather."
    elif effective_temp >= 20:
        outfit = "Long sleeves recommended. Bring a light jacket just in case."
    elif effective_temp >= 16:
        outfit = "Layer up with a sweater and jacket. It's getting cool!"
    else:
        outfit = "Bundle up with warm layers, coat, and accessories."
    
    if rain or 'rain' in weather_main:
        outfit += " Don't forget your umbrella and raincoat!"
    
    return outfit
