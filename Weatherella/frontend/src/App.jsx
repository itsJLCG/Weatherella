import React, { useEffect, useState } from 'react'
import WeatherCard from './WeatherCard'

export default function App() {
  const [cities, setCities] = useState([])
  const [selected, setSelected] = useState('')
  const [weather, setWeather] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/cities')
      .then(r => r.json())
      .then(setCities)
      .catch(e => console.error(e))
  }, [])

  useEffect(() => {
    if (!selected) return
    setLoading(true)
    setError(null)
    fetch(`/api/weather?city=${encodeURIComponent(selected)}`)
      .then(r => r.json())
      .then(data => {
        if (data.error) throw new Error(data.error)
        setWeather(data)
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [selected])

  return (
    <div className="app">
      <header className="header">
        <h1>Weatherella</h1>
        <p>Philippine real-time weather powered by OpenWeather</p>
      </header>

      <main className="container">
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
        {weather && <WeatherCard data={weather} />}
      </main>

      <footer className="footer">© 2025 Weatherella</footer>
    </div>
  )
}
