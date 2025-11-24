# Weatherella - Weather Application System

## Overview
Weatherella is a comprehensive weather application designed for the Philippines, providing real-time weather information, personalized recommendations, and user-friendly features to help users plan their day effectively.

## Core Features

### 🗺️ Interactive Map View
- Visual map of 30 major Philippine cities
- Click any city marker to view instant weather data
- Split-screen layout with map on the left, weather details on the right

### 📋 List View
- Complete list of all 30 supported cities
- Quick access to weather information for any location
- Clean, organized presentation of weather data

### ☀️ UV Index & Health Recommendations
- Real-time UV Index levels (Low to Extreme)
- WHO-standard health recommendations
- SPF suggestions and safe exposure times
- Protection tips for outdoor activities

### 👔 Clothing Recommendations
- Smart outfit suggestions based on current weather
- Temperature-appropriate clothing items
- Fabric type recommendations
- Color palette suggestions with visual swatches
- Layering advice for comfort

### ⭐ Favorite Cities
- Save frequently checked cities for quick access
- One-click favorite toggle with star button
- Persistent favorites across sessions

### 📊 User Features
- Automatic search history tracking (last 50 searches)
- User statistics (total searches, most searched city)
- Personalized user preferences
- Secure authentication with JWT tokens

## Technical Stack

**Frontend:**
- React 18.2 with Vite
- Leaflet.js for interactive maps
- Modern responsive design with glassmorphism effects

**Backend:**
- Flask REST API
- MongoDB for data persistence
- OpenWeather API integration
- bcrypt encryption and JWT authentication

**Database Collections:**
- `users` - User accounts and authentication
- `user_preferences` - Default settings and preferences
- `favorite_cities` - User's saved cities
- `search_history` - Weather search tracking

## Weather Intelligence

### Umbrella Predictor
Probabilistic recommendation system that analyzes:
- Precipitation levels
- Weather conditions
- Cloud coverage
- Humidity levels

### Smart Recommendations
- UV protection based on intensity levels
- Clothing suggestions for 6 temperature categories
- Weather-appropriate accessories and fabrics

## Security
- Password hashing with bcrypt
- JWT token-based authentication
- Protected API endpoints
- Secure MongoDB connection

## Supported Cities
30 major Philippine cities including Manila, Quezon City, Cebu, Davao, Makati, Taguig, and more across Luzon, Visayas, and Mindanao.

---

Built with ❤️ for the Philippines 🇵🇭






cd Weatherella
cd backend
python api.py



cd frontend
npm run dev
