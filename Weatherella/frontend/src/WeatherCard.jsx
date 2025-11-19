import React from 'react'

function formatTime(ts) {
  if (!ts) return 'N/A'
  return new Date(ts * 1000).toLocaleTimeString()
}

function UmbrellaIcon({ filled = true }) {
  // Inline umbrella SVG — filled for recommend, outline for not
  if (filled) {
    return (
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
        <path d="M12 3C7 3 3.3 5.8 2 9.5 3.3 9.5 4.8 10 6.1 10c.9 0 1.7.1 2.4.3.6.2 1.1.6 1.6 1 .5.4 1 .8 1.9.8s1.4-.4 1.9-.8c.5-.4 1-0.8 1.6-1 .7-.2 1.5-.3 2.4-.3 1.3 0 2.8-.5 4.1-1.5C20.7 5.8 17 3 12 3z" fill="currentColor" />
        <path d="M12 13v6a2 2 0 0 1-4 0" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    )
  }
  return (
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
      <path d="M12 3C7 3 3.3 5.8 2 9.5 3.3 9.5 4.8 10 6.1 10c.9 0 1.7.1 2.4.3.6.2 1.1.6 1.6 1 .5.4 1 .8 1.9.8s1.4-.4 1.9-.8c.5-.4 1-0.8 1.6-1 .7-.2 1.5-.3 2.4-.3 1.3 0 2.8-.5 4.1-1.5C20.7 5.8 17 3 12 3z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 13v6a2 2 0 0 1-4 0" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

export default function WeatherCard({ data, onToggleFavorite }) {
  const rec = data.umbrella_recommendation || null
  const scorePct = rec ? Math.round((rec.score || 0) * 100) : null
  const [isFavorite, setIsFavorite] = React.useState(data.is_favorite || false)
  const [isTogglingFavorite, setIsTogglingFavorite] = React.useState(false)

  const handleToggleFavorite = async () => {
    setIsTogglingFavorite(true)
    const newFavoriteState = await onToggleFavorite(data)
    if (newFavoriteState !== null) {
      setIsFavorite(newFavoriteState)
    }
    setIsTogglingFavorite(false)
  }

  // Determine banner style
  let bannerClass = 'recommend-neutral'
  let bannerText = 'No umbrella info'
  if (rec) {
    if (rec.recommend) {
      bannerClass = 'recommend-yes'
      bannerText = 'Bring an umbrella'
    } else if (rec.score >= 0.35) {
      bannerClass = 'recommend-maybe'
      bannerText = 'Consider an umbrella'
    } else {
      bannerClass = 'recommend-no'
      bannerText = 'No umbrella needed'
    }
  }

  return (
    <section className="card umbrella-card">
      <div className={`recommend-banner ${bannerClass}`} aria-live="polite">
        <div className="banner-left">
          <div className="umbrella-icon" aria-hidden>
            <UmbrellaIcon filled={rec ? rec.recommend : false} />
          </div>
          <div className="banner-text">
            <div className="banner-title">{bannerText}</div>
            {rec && <div className="banner-sub">Probability: {scorePct}%</div>}
          </div>
        </div>
        {rec && (
          <div className="banner-reasons">{rec.reasons.slice(0,2).join(' · ')}</div>
        )}
      </div>

      <div className="card-header compact">
        <div className="header-with-favorite">
          <div>
            <h2>{data.city_name}, {data.country}</h2>
            <div className="meta small">{new Date(data.dt * 1000).toLocaleString()}</div>
          </div>
          <button 
            className={`favorite-btn ${isFavorite ? 'favorited' : ''}`}
            onClick={handleToggleFavorite}
            disabled={isTogglingFavorite}
            title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
          >
            {isFavorite ? '★' : '☆'}
          </button>
        </div>
      </div>

      <div className="card-main compact">
        <div className="temp small">
          <div className="value big">{Math.round(data.temp)}°C</div>
          <div className="desc">Feels like {Math.round(data.feels_like)}°C</div>
        </div>

        <div className="icon small">
          <img src={`https://openweathermap.org/img/wn/${data.weather.icon}@2x.png`} alt="icon" />
          <div className="weather-desc">{data.weather.description}</div>
        </div>
      </div>

      <div className="details subdued">
        <div>Humidity: {data.humidity}%</div>
        <div>Wind: {data.wind_speed} m/s</div>
        <div>Pressure: {data.pressure} hPa</div>
        <div>Visibility: {(data.visibility/1000).toFixed(1)} km</div>
        <div>Clouds: {data.clouds}%</div>
        <div>Sunrise: {formatTime(data.sunrise)}</div>
        <div>Sunset: {formatTime(data.sunset)}</div>
      </div>
    </section>
  )
}
