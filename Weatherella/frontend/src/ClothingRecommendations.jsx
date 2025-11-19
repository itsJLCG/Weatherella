import React from 'react';

export default function ClothingRecommendations({ clothingData }) {
  if (!clothingData) {
    return null;
  }

  const {
    category,
    color,
    icon,
    comfort_level,
    temperature,
    clothing_items,
    layers,
    accessories,
    tips,
    conditions
  } = clothingData;

  return (
    <div className="clothing-container">
      <div className="clothing-header">
        <div className="clothing-title">
          <span className="clothing-icon">{icon}</span>
          <h3>What to Wear</h3>
        </div>
      </div>

      <div className="clothing-temp-gauge">
        <div 
          className="temp-badge" 
          style={{ 
            background: color,
            boxShadow: `0 4px 12px ${color}40`
          }}
        >
          <div className="temp-category">{category}</div>
          <div className="temp-value">{temperature.effective}°C</div>
          <div className="temp-comfort">{comfort_level}</div>
        </div>
      </div>

      <div className="clothing-conditions-badges">
        {conditions.rain && (
          <span className="condition-badge rain">☂️ Rainy</span>
        )}
        {conditions.windy && (
          <span className="condition-badge windy">🌬️ Windy</span>
        )}
        {conditions.humid && (
          <span className="condition-badge humid">💧 Humid</span>
        )}
        {conditions.sunny && (
          <span className="condition-badge sunny">☀️ Sunny</span>
        )}
      </div>

      <div className="clothing-section">
        <h4>👕 Recommended Clothing</h4>
        <ul className="clothing-list">
          {clothing_items.map((item, index) => (
            <li key={index}>
              <span className="item-bullet">•</span>
              {item}
            </li>
          ))}
        </ul>
      </div>

      <div className="clothing-section">
        <h4>🧥 Layering Guide</h4>
        <div className="layers-info">
          {layers.map((layer, index) => (
            <div key={index} className="layer-item">
              <span className="layer-icon">📐</span>
              <span>{layer}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="clothing-section">
        <h4>🎒 Accessories & Extras</h4>
        <div className="accessories-grid">
          {accessories.map((accessory, index) => (
            <div key={index} className="accessory-item">
              <span className="accessory-check">✓</span>
              <span>{accessory}</span>
            </div>
          ))}
        </div>
      </div>

      {tips && tips.length > 0 && (
        <div className="clothing-tips">
          <h4>💡 Style Tips & Advice</h4>
          <ul className="tips-list">
            {tips.map((tip, index) => (
              <li key={index}>
                <span className="tip-bullet">→</span>
                {tip}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="temp-details">
        <div className="temp-detail-item">
          <span className="detail-label">Actual Temp</span>
          <span className="detail-value">{temperature.actual}°C</span>
        </div>
        <div className="temp-detail-item">
          <span className="detail-label">Feels Like</span>
          <span className="detail-value">{temperature.feels_like}°C</span>
        </div>
      </div>
    </div>
  );
}
