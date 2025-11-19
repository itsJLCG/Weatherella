import React from 'react';
import UVIndex from './UVIndex';

export default function UVIndexView({ weather, loading, error, selected }) {
  if (!selected && !weather) {
    return (
      <div className="uv-view-container">
        <div className="placeholder">
          <div className="placeholder-icon">☀️</div>
          <h3>UV Index Monitor</h3>
          <p>Select a city from Map View or List View to see real-time UV Index and sun protection recommendations</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="uv-view-container">
        <div className="loading">Loading UV Index data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="uv-view-container">
        <div className="error">
          <h3>⚠️ Error Loading UV Data</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!weather) {
    return null;
  }

  const uvData = weather.uv_recommendations;

  return (
    <div className="uv-view-container">
      <div className="uv-view-header">
        <div className="uv-view-title">
          <h2>UV Index & Health Recommendations</h2>
          <p className="uv-view-subtitle">
            {weather.city_name}, {weather.country} • {new Date(weather.dt * 1000).toLocaleString()}
          </p>
        </div>
      </div>

      {uvData ? (
        <div className="uv-view-content">
          <UVIndex uvData={uvData} />
          
          <div className="uv-additional-info">
            <div className="info-card">
              <h4>🌡️ Current Conditions</h4>
              <div className="info-grid">
                <div className="info-item">
                  <span className="label">Temperature:</span>
                  <span className="value">{Math.round(weather.temp)}°C</span>
                </div>
                <div className="info-item">
                  <span className="label">Feels Like:</span>
                  <span className="value">{Math.round(weather.feels_like)}°C</span>
                </div>
                <div className="info-item">
                  <span className="label">Humidity:</span>
                  <span className="value">{weather.humidity}%</span>
                </div>
                <div className="info-item">
                  <span className="label">Cloud Cover:</span>
                  <span className="value">{weather.clouds}%</span>
                </div>
              </div>
            </div>

            <div className="info-card">
              <h4>🕐 Sun Schedule</h4>
              <div className="info-grid">
                <div className="info-item">
                  <span className="label">Sunrise:</span>
                  <span className="value">{new Date(weather.sunrise * 1000).toLocaleTimeString()}</span>
                </div>
                <div className="info-item">
                  <span className="label">Sunset:</span>
                  <span className="value">{new Date(weather.sunset * 1000).toLocaleTimeString()}</span>
                </div>
              </div>
              <p className="sun-note">
                ⚠️ UV levels are highest between 10 AM - 4 PM. Plan outdoor activities accordingly.
              </p>
            </div>

            <div className="info-card tips-card">
              <h4>💡 Quick Sun Safety Tips</h4>
              <ul className="tips-list">
                <li>Reapply sunscreen every 2 hours, or after swimming/sweating</li>
                <li>Seek shade during peak UV hours (10 AM - 4 PM)</li>
                <li>Wear UV-blocking sunglasses to protect your eyes</li>
                <li>Protect your skin even on cloudy days - UV rays penetrate clouds</li>
                <li>Children need extra protection - their skin is more sensitive</li>
                <li>Use broad-spectrum sunscreen that protects against both UVA and UVB rays</li>
              </ul>
            </div>
          </div>
        </div>
      ) : (
        <div className="uv-unavailable">
          <div className="unavailable-icon">📊</div>
          <h3>UV Data Not Available</h3>
          <p>UV Index information is currently unavailable for this location. Please try again later.</p>
        </div>
      )}
    </div>
  );
}
