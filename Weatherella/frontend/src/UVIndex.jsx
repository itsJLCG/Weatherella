import React from 'react';

const UVIndex = ({ uvData }) => {
  if (!uvData) {
    return null;
  }

  const { index, category, color, risk_level, recommendations, protection_needed, safe_exposure, sunscreen, warning } = uvData;

  // Color mapping for UV categories
  const colorStyles = {
    green: {
      background: 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)',
      border: '#22c55e',
      shadow: 'rgba(34, 197, 94, 0.3)'
    },
    yellow: {
      background: 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)',
      border: '#f59e0b',
      shadow: 'rgba(245, 158, 11, 0.3)'
    },
    orange: {
      background: 'linear-gradient(135deg, #fb923c 0%, #f97316 100%)',
      border: '#f97316',
      shadow: 'rgba(249, 115, 22, 0.3)'
    },
    red: {
      background: 'linear-gradient(135deg, #f87171 0%, #ef4444 100%)',
      border: '#ef4444',
      shadow: 'rgba(239, 68, 68, 0.3)'
    },
    purple: {
      background: 'linear-gradient(135deg, #c084fc 0%, #a855f7 100%)',
      border: '#a855f7',
      shadow: 'rgba(168, 85, 247, 0.3)'
    },
    gray: {
      background: 'linear-gradient(135deg, #9ca3af 0%, #6b7280 100%)',
      border: '#6b7280',
      shadow: 'rgba(107, 114, 128, 0.3)'
    }
  };

  const currentColor = colorStyles[color] || colorStyles.gray;

  // UV index icon based on category
  const getUVIcon = () => {
    if (index <= 2) return '🌤️';
    if (index <= 5) return '☀️';
    if (index <= 7) return '🌞';
    if (index <= 10) return '🔥';
    return '⚠️';
  };

  return (
    <div className="uv-index-container">
      <div className="uv-header">
        <div className="uv-title">
          <span className="uv-icon">{getUVIcon()}</span>
          <h3>UV Index & Sun Protection</h3>
        </div>
      </div>

      <div className="uv-gauge-container">
        <div className="uv-gauge" style={{
          background: currentColor.background,
          borderColor: currentColor.border,
          boxShadow: `0 4px 12px ${currentColor.shadow}`
        }}>
          <div className="uv-value">{index}</div>
          <div className="uv-category">{category}</div>
          <div className="uv-risk">{risk_level.replace('_', ' ')}</div>
        </div>
      </div>

      {warning && (
        <div className="uv-warning" style={{ borderLeftColor: currentColor.border }}>
          <strong>⚠️ Warning:</strong> {warning}
        </div>
      )}

      <div className="uv-recommendations">
        <h4>Protection Recommendations:</h4>
        <ul>
          {recommendations.map((rec, index) => (
            <li key={index}>
              <span className="rec-bullet">•</span>
              {rec}
            </li>
          ))}
        </ul>
      </div>

      {safe_exposure && (
        <div className="uv-info-row">
          <div className="uv-info-item">
            <span className="info-label">Safe Exposure:</span>
            <span className="info-value">{safe_exposure}</span>
          </div>
          {sunscreen && (
            <div className="uv-info-item">
              <span className="info-label">Sunscreen:</span>
              <span className="info-value">{sunscreen}</span>
            </div>
          )}
        </div>
      )}

      <div className="uv-protection-badges">
        {protection_needed ? (
          <>
            <span className="protection-badge needed">
              🧴 Sunscreen Required
            </span>
            <span className="protection-badge needed">
              🕶️ Sunglasses Needed
            </span>
            {index > 5 && (
              <span className="protection-badge needed">
                👒 Hat Recommended
              </span>
            )}
            {index > 7 && (
              <span className="protection-badge needed">
                👕 Cover Up
              </span>
            )}
          </>
        ) : (
          <span className="protection-badge safe">
            ✅ No Protection Required
          </span>
        )}
      </div>

      <div className="uv-scale">
        <div className="uv-scale-title">UV Index Scale</div>
        <div className="uv-scale-bar">
          <div className="scale-segment green">0-2<br/>Low</div>
          <div className="scale-segment yellow">3-5<br/>Moderate</div>
          <div className="scale-segment orange">6-7<br/>High</div>
          <div className="scale-segment red">8-10<br/>Very High</div>
          <div className="scale-segment purple">11+<br/>Extreme</div>
        </div>
      </div>
    </div>
  );
};

export default UVIndex;
