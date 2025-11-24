import React from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

// Philippine cities with coordinates - fetched from API
const philippineCities = [
  { id: 'Manila,PH', name: 'Manila', lat: 14.5995, lng: 120.9842 },
  { id: 'Quezon City,PH', name: 'Quezon City', lat: 14.6760, lng: 121.0437 },
  { id: 'Davao,PH', name: 'Davao', lat: 7.1907, lng: 125.4553 },
  { id: 'Cebu,PH', name: 'Cebu', lat: 10.3157, lng: 123.8854 },
  { id: 'Taguig,PH', name: 'Taguig', lat: 14.5176, lng: 121.0509 },
  { id: 'Makati,PH', name: 'Makati', lat: 14.5547, lng: 121.0244 },
  { id: 'Pasig,PH', name: 'Pasig', lat: 14.5764, lng: 121.0851 },
  { id: 'Caloocan,PH', name: 'Caloocan', lat: 14.6488, lng: 120.9830 },
  { id: 'Antipolo,PH', name: 'Antipolo', lat: 14.5862, lng: 121.1759 },
  { id: 'Baguio,PH', name: 'Baguio', lat: 16.4023, lng: 120.5960 },
  { id: 'Iloilo,PH', name: 'Iloilo', lat: 10.7202, lng: 122.5621 },
  { id: 'Zamboanga,PH', name: 'Zamboanga', lat: 6.9214, lng: 122.0790 },
  { id: 'Cagayan de Oro,PH', name: 'Cagayan de Oro', lat: 8.4542, lng: 124.6319 },
  { id: 'Bacolod,PH', name: 'Bacolod', lat: 10.6770, lng: 122.9500 },
  { id: 'General Santos,PH', name: 'General Santos', lat: 6.1164, lng: 125.1716 },
  { id: 'Parañaque,PH', name: 'Parañaque', lat: 14.4793, lng: 121.0198 },
  { id: 'Las Piñas,PH', name: 'Las Piñas', lat: 14.4463, lng: 120.9832 },
  { id: 'Mandaluyong,PH', name: 'Mandaluyong', lat: 14.5794, lng: 121.0359 },
  { id: 'Muntinlupa,PH', name: 'Muntinlupa', lat: 14.4081, lng: 121.0425 },
  { id: 'San Juan,PH', name: 'San Juan', lat: 14.6019, lng: 121.0355 },
  { id: 'Valenzuela,PH', name: 'Valenzuela', lat: 14.6937, lng: 120.9830 },
  { id: 'Marikina,PH', name: 'Marikina', lat: 14.6507, lng: 121.1029 },
  { id: 'Navotas,PH', name: 'Navotas', lat: 14.6628, lng: 120.9409 },
  { id: 'Malabon,PH', name: 'Malabon', lat: 14.6620, lng: 120.9604 },
  { id: 'Angeles,PH', name: 'Angeles', lat: 15.1450, lng: 120.5887 },
  { id: 'Olongapo,PH', name: 'Olongapo', lat: 14.8294, lng: 120.2825 },
  { id: 'Tacloban,PH', name: 'Tacloban', lat: 11.2447, lng: 125.0036 },
  { id: 'Naga,PH', name: 'Naga', lat: 13.6218, lng: 123.1948 },
  { id: 'Butuan,PH', name: 'Butuan', lat: 8.9475, lng: 125.5406 },
  { id: 'Iligan,PH', name: 'Iligan', lat: 8.2280, lng: 124.2452 },
]

// Custom marker icon with city highlight
const createCustomIcon = (isSelected) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `<div class="marker-pin ${isSelected ? 'selected' : ''}">
            <div class="marker-dot"></div>
           </div>`,
    iconSize: [30, 42],
    iconAnchor: [15, 42],
    popupAnchor: [0, -42]
  })
}

export default function PhilippineMap({ onCitySelect, selectedCity }) {
  const selectedCityData = philippineCities.find(c => c.id === selectedCity)

  return (
    <div className="map-wrapper">
      <MapContainer
        center={[12.8797, 121.7740]}
        zoom={6}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {philippineCities.map((city) => (
          <Marker
            key={city.id}
            position={[city.lat, city.lng]}
            icon={createCustomIcon(selectedCity === city.id)}
            eventHandlers={{
              click: () => onCitySelect(city.id)
            }}
          >
            <Popup>
              <div className="map-popup">
                <h3>{city.name}</h3>
                <p>Click marker to view weather</p>
              </div>
            </Popup>
          </Marker>
        ))}
        
        {selectedCityData && <MapFlyTo city={selectedCityData} />}
      </MapContainer>
    </div>
  )
}

// Component to handle flying to selected city
function MapFlyTo({ city }) {
  const map = useMap()
  
  React.useEffect(() => {
    if (city) {
      map.flyTo([city.lat, city.lng], 10, {
        duration: 1.5
      })
    }
  }, [city, map])
  
  return null
}
