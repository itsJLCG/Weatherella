import React, { useEffect, useState } from 'react'
import WeatherCard from './WeatherCard'
import Login from './Login'
import Register from './Register'
import PhilippineMap from './PhilippineMap'
import Header from './Header'
import Footer from './Footer'
import About from './About'
import UVIndexView from './UVIndexView'
import ClothingView from './ClothingView'

export default function App() {
  const [user, setUser] = useState(null)
  const [showRegister, setShowRegister] = useState(false)
  const [cities, setCities] = useState([])
  const [selected, setSelected] = useState('')
  const [weather, setWeather] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [currentView, setCurrentView] = useState('map') // 'map', 'list', or 'uv'
  const [showAbout, setShowAbout] = useState(false)

  // Check if user is already logged in
  useEffect(() => {
    const token = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    if (token && savedUser) {
      setUser(JSON.parse(savedUser))
    }
  }, [])

  // Fetch cities when user is logged in
  useEffect(() => {
    if (!user) return
    fetch('/api/cities')
      .then(r => r.json())
      .then(setCities)
      .catch(e => console.error(e))
  }, [user])

  // Fetch weather when city is selected
  useEffect(() => {
    if (!selected || !user) return
    setLoading(true)
    setError(null)
    
    const token = localStorage.getItem('token')
    fetch(`/api/weather?city=${encodeURIComponent(selected)}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(r => r.json())
      .then(data => {
        if (data.error) throw new Error(data.error)
        setWeather(data)
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [selected, user])

  const handleLogin = (userData) => {
    setUser(userData)
  }

  const handleRegister = (userData) => {
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    setWeather(null)
    setSelected('')
  }

  const handleCitySelect = (cityId) => {
    setSelected(cityId)
  }

  const handleToggleFavorite = async (weatherData) => {
    const token = localStorage.getItem('token')
    const cityInfo = cities.find(c => c.id === selected)
    
    if (!cityInfo) return null

    try {
      if (weatherData.is_favorite) {
        // Remove from favorites
        const response = await fetch(`/api/favorites/${encodeURIComponent(selected)}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        if (response.ok) {
          setWeather({...weather, is_favorite: false})
          return false
        }
      } else {
        // Add to favorites
        const response = await fetch('/api/favorites', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            city_id: cityInfo.id,
            city_name: cityInfo.name,
            lat: cityInfo.lat,
            lng: cityInfo.lng
          })
        })
        
        if (response.ok) {
          setWeather({...weather, is_favorite: true})
          return true
        }
      }
    } catch (e) {
      console.error('Error toggling favorite:', e)
    }
    
    return null
  }

  const handleViewChange = (view) => {
    setCurrentView(view)
  }

  const handleShowAbout = () => {
    setShowAbout(true)
  }

  const handleCloseAbout = () => {
    setShowAbout(false)
  }

  // Show login/register screen if not authenticated
  if (!user) {
    return showRegister ? (
      <Register 
        onRegister={handleRegister}
        onSwitchToLogin={() => setShowRegister(false)}
      />
    ) : (
      <Login 
        onLogin={handleLogin}
        onSwitchToRegister={() => setShowRegister(true)}
      />
    )
  }

  // Show main app when authenticated
  return (
    <div className="app">
      <Header 
        user={user} 
        onLogout={handleLogout}
        currentView={currentView}
        onViewChange={handleViewChange}
        onShowAbout={handleShowAbout}
      />

      {showAbout && <About onClose={handleCloseAbout} />}

      <main className="main-content">
        {currentView === 'map' ? (
          <div className="split-view">
            <div className="map-panel">
              <div className="map-container">
                <PhilippineMap 
                  onCitySelect={handleCitySelect}
                  selectedCity={selected}
                />
              </div>
            </div>
            <div className="weather-panel">
              {!selected && !weather && (
                <div className="placeholder">
                  <div className="placeholder-icon">🗺️</div>
                  <h3>Select a City</h3>
                  <p>Click any marker on the map to view weather details and umbrella recommendations</p>
                </div>
              )}
              {loading && <div className="loading">Loading weather data...</div>}
              {error && <div className="error">{error}</div>}
              {weather && <WeatherCard data={weather} onToggleFavorite={handleToggleFavorite} />}
            </div>
          </div>
        ) : currentView === 'list' ? (
          <div className="list-view">
            <div className="controls">
              <label htmlFor="city">Choose a city</label>
              <select id="city" value={selected} onChange={e => setSelected(e.target.value)}>
                <option value="">-- Select a city --</option>
                {cities.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
            {loading && <div className="loading">Loading...</div>}
            {error && <div className="error">{error}</div>}
            {weather && <WeatherCard data={weather} onToggleFavorite={handleToggleFavorite} />}
          </div>
        ) : currentView === 'uv' ? (
          <UVIndexView 
            weather={weather}
            loading={loading}
            error={error}
            selected={selected}
          />
        ) : (
          <ClothingView 
            weather={weather}
            loading={loading}
            error={error}
            selected={selected}
          />
        )}
      </main>

      <Footer />
    </div>
  )
}
