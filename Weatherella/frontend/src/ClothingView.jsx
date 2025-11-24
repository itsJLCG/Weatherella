import React from 'react';
import ClothingRecommendations from './ClothingRecommendations';

export default function ClothingView({ weather, loading, error, selected }) {
  if (!selected && !weather) {
    return (
      <div className="clothing-view-container">
        <div className="placeholder">
          <div className="placeholder-icon">👔</div>
          <h3>Clothing Recommendations</h3>
          <p>Select a city from Map View or List View to get personalized clothing suggestions based on current weather</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="clothing-view-container">
        <div className="loading">Loading clothing recommendations...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="clothing-view-container">
        <div className="error">
          <h3>⚠️ Error Loading Data</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!weather) {
    return null;
  }

  const clothingData = weather.clothing_recommendations;

  return (
    <div className="clothing-view-container">
      <div className="clothing-view-header">
        <div className="clothing-view-title">
          <h2>Clothing Recommendations</h2>
          <p className="clothing-view-subtitle">
            {weather.city_name}, {weather.country} • {new Date(weather.dt * 1000).toLocaleString()}
          </p>
        </div>
      </div>

      {clothingData ? (
        <div className="clothing-view-content">
          <ClothingRecommendations clothingData={clothingData} />
          
          <div className="clothing-additional-info">
            <div className="info-card outfit-card">
              <h4>🎯 Quick Outfit Suggestion</h4>
              <p className="outfit-suggestion">
                {clothingData.category === "Very Hot" && "Keep it minimal! Wear light, breathable fabrics in light colors. Stay cool and protect yourself from the sun."}
                {clothingData.category === "Hot" && "Dress light and comfortable. Choose breathable materials like cotton or linen to stay cool throughout the day."}
                {clothingData.category === "Warm" && "Perfect weather for casual wear! Comfortable t-shirts and jeans are ideal. Bring a light jacket for air-conditioned spaces."}
                {clothingData.category === "Mild" && "Layer up lightly. Long sleeves recommended with an optional light jacket for changing temperatures."}
                {clothingData.category === "Cool" && "Bundle up with layers! A sweater and jacket combination will keep you comfortable in this cool weather."}
                {clothingData.category === "Cold" && "Dress warmly in multiple layers. Don't forget your coat, scarf, and gloves to stay cozy!"}
              </p>
            </div>

            <div className="info-card weather-context-card">
              <h4>🌡️ Weather Context</h4>
              <div className="weather-context-grid">
                <div className="context-item">
                  <span className="context-icon">🌡️</span>
                  <div className="context-details">
                    <span className="context-label">Temperature</span>
                    <span className="context-value">{Math.round(weather.temp)}°C</span>
                  </div>
                </div>
                <div className="context-item">
                  <span className="context-icon">💨</span>
                  <div className="context-details">
                    <span className="context-label">Wind Speed</span>
                    <span className="context-value">{weather.wind_speed} m/s</span>
                  </div>
                </div>
                <div className="context-item">
                  <span className="context-icon">💧</span>
                  <div className="context-details">
                    <span className="context-label">Humidity</span>
                    <span className="context-value">{weather.humidity}%</span>
                  </div>
                </div>
                <div className="context-item">
                  <span className="context-icon">☁️</span>
                  <div className="context-details">
                    <span className="context-label">Cloud Cover</span>
                    <span className="context-value">{weather.clouds}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="info-card fabric-guide-card">
              <h4>🧵 Fabric Guide for Current Weather</h4>
              <div className="fabric-recommendations">
                {clothingData.temperature.effective >= 28 && (
                  <div className="fabric-item recommended">
                    <span className="fabric-name">✓ Cotton & Linen</span>
                    <span className="fabric-desc">Breathable and moisture-wicking</span>
                  </div>
                )}
                {clothingData.temperature.effective >= 28 && (
                  <div className="fabric-item recommended">
                    <span className="fabric-name">✓ Light Synthetics</span>
                    <span className="fabric-desc">Quick-drying athletic fabrics</span>
                  </div>
                )}
                {clothingData.temperature.effective < 28 && clothingData.temperature.effective >= 20 && (
                  <div className="fabric-item recommended">
                    <span className="fabric-name">✓ Cotton Blends</span>
                    <span className="fabric-desc">Comfortable for all-day wear</span>
                  </div>
                )}
                {clothingData.temperature.effective < 20 && (
                  <div className="fabric-item recommended">
                    <span className="fabric-name">✓ Wool & Fleece</span>
                    <span className="fabric-desc">Warm and insulating</span>
                  </div>
                )}
                {clothingData.conditions.rain && (
                  <div className="fabric-item recommended">
                    <span className="fabric-name">✓ Waterproof Materials</span>
                    <span className="fabric-desc">Stay dry in rainy conditions</span>
                  </div>
                )}
                {clothingData.temperature.effective >= 28 && (
                  <div className="fabric-item avoid">
                    <span className="fabric-name">✗ Heavy Fabrics</span>
                    <span className="fabric-desc">Avoid denim, wool, thick materials</span>
                  </div>
                )}
              </div>
            </div>

            <div className="info-card color-guide-card">
              <h4>🎨 Color Recommendations</h4>
              <div className="color-recommendations">
                {clothingData.temperature.effective >= 28 ? (
                  <>
                    <div className="color-swatch-group">
                      <span className="color-label">Recommended:</span>
                      <div className="color-swatches">
                        <div className="color-swatch" style={{background: '#ffffff'}} title="White"></div>
                        <div className="color-swatch" style={{background: '#f0f0f0'}} title="Light Gray"></div>
                        <div className="color-swatch" style={{background: '#fef3c7'}} title="Cream"></div>
                        <div className="color-swatch" style={{background: '#dbeafe'}} title="Light Blue"></div>
                      </div>
                    </div>
                    <p className="color-note">Light colors reflect heat and keep you cooler</p>
                  </>
                ) : (
                  <>
                    <div className="color-swatch-group">
                      <span className="color-label">Versatile:</span>
                      <div className="color-swatches">
                        <div className="color-swatch" style={{background: '#1f2937'}} title="Dark Gray"></div>
                        <div className="color-swatch" style={{background: '#1e40af'}} title="Navy"></div>
                        <div className="color-swatch" style={{background: '#059669'}} title="Green"></div>
                        <div className="color-swatch" style={{background: '#7c2d12'}} title="Brown"></div>
                      </div>
                    </div>
                    <p className="color-note">Darker colors provide warmth in cooler weather</p>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="clothing-unavailable">
          <div className="unavailable-icon">👔</div>
          <h3>Recommendations Not Available</h3>
          <p>Clothing recommendations are currently unavailable. Please try again later.</p>
        </div>
      )}
    </div>
  );
}
