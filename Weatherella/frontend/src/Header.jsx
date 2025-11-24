import React, { useState } from 'react'

export default function Header({ user, onLogout, currentView, onViewChange, onShowAbout }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen)
  }

  return (
    <header className="main-header">
      <div className="header-container">
        <div className="header-left">
          <div className="logo">
            <span className="logo-icon">☂️</span>
            <div className="logo-text">
              <h1>Weatherella</h1>
              <span className="tagline">Smart Weather Insights</span>
            </div>
          </div>
        </div>

        {user && (
          <>
            <nav className={`header-nav ${mobileMenuOpen ? 'mobile-open' : ''}`}>
              <button 
                className={`nav-item ${currentView === 'map' ? 'active' : ''}`}
                onClick={() => {
                  onViewChange('map')
                  setMobileMenuOpen(false)
                }}
              >
                <span className="nav-icon">🗺️</span>
                <span>Map View</span>
              </button>
              <button 
                className={`nav-item ${currentView === 'list' ? 'active' : ''}`}
                onClick={() => {
                  onViewChange('list')
                  setMobileMenuOpen(false)
                }}
              >
                <span className="nav-icon">📋</span>
                <span>List View</span>
              </button>
              <button 
                className={`nav-item ${currentView === 'uv' ? 'active' : ''}`}
                onClick={() => {
                  onViewChange('uv')
                  setMobileMenuOpen(false)
                }}
              >
                <span className="nav-icon">☀️</span>
                <span>UV Index</span>
              </button>
              <button 
                className={`nav-item ${currentView === 'clothing' ? 'active' : ''}`}
                onClick={() => {
                  onViewChange('clothing')
                  setMobileMenuOpen(false)
                }}
              >
                <span className="nav-icon">👔</span>
                <span>Clothing</span>
              </button>
              <button
                className="nav-item info"
                onClick={() => {
                  onShowAbout()
                  setMobileMenuOpen(false)
                }}
              >
                <span className="nav-icon">ℹ️</span>
                <span>About</span>
              </button>
            </nav>

            <div className="header-right">
              <div className="user-profile">
                <div className="user-avatar">
                  {user.name ? user.name.charAt(0).toUpperCase() : user.email ? user.email.charAt(0).toUpperCase() : '👤'}
                </div>
                <div className="user-details">
                  <span className="user-greeting">Welcome back</span>
                  <span className="user-name">{user.name || user.email || 'User'}</span>
                </div>
              </div>
              <button onClick={onLogout} className="logout-btn">
                <span>Logout</span>
                <span className="logout-icon">🚪</span>
              </button>
            </div>

            <button className="mobile-menu-toggle" onClick={toggleMobileMenu}>
              <span className={`hamburger ${mobileMenuOpen ? 'open' : ''}`}>
                <span></span>
                <span></span>
                <span></span>
              </span>
            </button>
          </>
        )}
      </div>
    </header>
  )
}
