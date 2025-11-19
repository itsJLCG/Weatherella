import React from 'react'

export default function About({ onClose }) {
  return (
    <div className="about-overlay" onClick={onClose}>
      <div className="about-modal" onClick={(e) => e.stopPropagation()}>
        <button className="about-close" onClick={onClose}>×</button>
        
        <div className="about-content">
          <div className="about-header">
            <div className="about-icon">☂️</div>
            <h2>About Weatherella</h2>
            <p className="about-subtitle">Your Smart Weather Companion</p>
          </div>

          <div className="about-section">
            <h3>🌦️ What is Weatherella?</h3>
            <p>
              Weatherella is an intelligent weather application designed specifically for the Philippines, 
              providing real-time weather data and smart umbrella recommendations for over 30 major cities 
              across the country.
            </p>
          </div>

          <div className="about-section">
            <h3>✨ Key Features</h3>
            <ul className="feature-list">
              <li>
                <strong>Real-Time Weather Data:</strong> Powered by OpenWeather API for accurate, 
                up-to-date weather information
              </li>
              <li>
                <strong>Interactive Map View:</strong> Explore weather across 30+ Philippine cities 
                with an intuitive, clickable map interface
              </li>
              <li>
                <strong>Smart Umbrella Predictor:</strong> Advanced algorithm analyzes multiple weather 
                indicators to recommend whether you should bring an umbrella
              </li>
              <li>
                <strong>UV Index & Health Recommendations:</strong> Real-time UV index monitoring with 
                personalized sun protection advice and safety warnings based on WHO guidelines
              </li>
              <li>
                <strong>Clothing Recommendations:</strong> Smart outfit suggestions based on temperature, 
                weather conditions, wind, and humidity with fabric and color guidance
              </li>
              <li>
                <strong>Multiple View Modes:</strong> Switch between interactive map view and 
                traditional list view
              </li>
              <li>
                <strong>Secure Authentication:</strong> MongoDB-powered user accounts with encrypted 
                password storage
              </li>
            </ul>
          </div>

          <div className="about-section">
            <h3>🧮 Umbrella Prediction Algorithm</h3>
            <p>
              Our sophisticated umbrella recommendation system analyzes multiple weather factors:
            </p>
            <ul className="tech-list">
              <li>Direct precipitation indicators (rain, drizzle, thunderstorms)</li>
              <li>Measured rain and snow volume</li>
              <li>Dew point calculation using Magnus formula</li>
              <li>Relative humidity levels</li>
              <li>Cloud coverage percentage</li>
              <li>Atmospheric pressure</li>
              <li>Visibility conditions</li>
            </ul>
            <p className="tech-note">
              These indicators are combined using probabilistic union formula to generate an 
              explainable recommendation score.
            </p>
          </div>

          <div className="about-section">
            <h3>☀️ UV Index & Health Protection</h3>
            <p>
              Our UV Index feature provides real-time sun exposure monitoring and personalized protection advice:
            </p>
            <ul className="tech-list">
              <li>WHO-standard UV Index categories (Low, Moderate, High, Very High, Extreme)</li>
              <li>Color-coded risk visualization with 5-tier scale</li>
              <li>Personalized sunscreen SPF recommendations</li>
              <li>Safe exposure time calculations</li>
              <li>Detailed protection guidelines (hat, sunglasses, clothing)</li>
              <li>Real-time warnings for dangerous UV levels</li>
            </ul>
            <p className="tech-note">
              UV data is fetched from OpenWeather API and analyzed using WHO International UV Index guidelines 
              to provide accurate health recommendations.
            </p>
          </div>

          <div className="about-section">
            <h3>👔 Clothing Recommendations</h3>
            <p>
              Our intelligent clothing recommendation system helps you dress appropriately for the weather:
            </p>
            <ul className="tech-list">
              <li>Temperature-based outfit suggestions (Very Hot to Cold categories)</li>
              <li>Layering guides based on effective temperature</li>
              <li>Weather-specific accessories (umbrella, windbreaker, sun protection)</li>
              <li>Fabric recommendations (cotton, linen, wool, waterproof materials)</li>
              <li>Color guidance (light colors for hot weather, dark for cool)</li>
              <li>Context-aware tips considering humidity, wind, and precipitation</li>
            </ul>
            <p className="tech-note">
              The system analyzes temperature, feels-like temperature, weather conditions, wind speed, 
              and humidity to provide personalized clothing suggestions for maximum comfort.
            </p>
          </div>

          <div className="about-section">
            <h3>🛠️ Technology Stack</h3>
            <div className="tech-grid">
              <div className="tech-item">
                <div className="tech-category">Frontend</div>
                <div className="tech-tags">
                  <span>React</span>
                  <span>Vite</span>
                  <span>Leaflet.js</span>
                </div>
              </div>
              <div className="tech-item">
                <div className="tech-category">Backend</div>
                <div className="tech-tags">
                  <span>Flask</span>
                  <span>Python</span>
                  <span>JWT Auth</span>
                </div>
              </div>
              <div className="tech-item">
                <div className="tech-category">Database</div>
                <div className="tech-tags">
                  <span>MongoDB</span>
                  <span>bcrypt</span>
                </div>
              </div>
              <div className="tech-item">
                <div className="tech-category">APIs</div>
                <div className="tech-tags">
                  <span>OpenWeather</span>
                  <span>OpenStreetMap</span>
                </div>
              </div>
            </div>
          </div>

          <div className="about-section">
            <h3>📍 Coverage</h3>
            <p>
              Weatherella provides weather data for <strong>30 major Philippine cities</strong> including:
            </p>
            <div className="city-coverage">
              <div className="city-group">
                <strong>Metro Manila:</strong> Manila, Quezon City, Makati, Taguig, Pasig, 
                Caloocan, Parañaque, Las Piñas, Mandaluyong, Muntinlupa, San Juan, 
                Valenzuela, Marikina, Navotas, Malabon
              </div>
              <div className="city-group">
                <strong>Major Cities:</strong> Davao, Cebu, Baguio, Iloilo, Zamboanga, 
                Cagayan de Oro, Bacolod, General Santos, Antipolo, Angeles, Olongapo, 
                Tacloban, Naga, Butuan, Iligan
              </div>
            </div>
          </div>

          <div className="about-section">
            <h3>👨‍💻 Development</h3>
            <p>
              Weatherella is built with modern web technologies and follows best practices 
              for security, performance, and user experience. The application features 
              responsive design, smooth animations, and an intuitive interface optimized 
              for both desktop and mobile devices.
            </p>
          </div>

          <div className="about-footer">
            <p>Made with ❤️ for the Philippines</p>
            <p className="version">Version 1.0.0 | © 2025 Weatherella</p>
          </div>
        </div>
      </div>
    </div>
  )
}
