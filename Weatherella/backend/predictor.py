"""Umbrella recommendation logic using principled indicators.

Algorithm summary:
- Compute dew point from temperature and humidity (Magnus formula).
- Create independent indicator probabilities (weights) for factors:
  - direct precipitation (weather id in 2xx/3xx/5xx/6xx)
  - observed rain/snow volume
  - dew point proximity to temperature
  - relative humidity
  - cloudiness
  - low pressure
  - low visibility
- Combine indicators using union formula: P = 1 - Π(1 - p_i)

This yields a probabilistic, explainable score in [0,1]. Recommend umbrella if score >= 0.5.
"""
from typing import Dict, Any, List
import math


def _dew_point(temp_c: float, rh: float) -> float:
    """Calculate dew point (°C) from temperature (°C) and relative humidity (%) using Magnus formula."""
    # Magnus constants for water
    a = 17.27
    b = 237.7
    if rh <= 0:
        return -999.0
    # avoid errors
    try:
        f = (a * temp_c) / (b + temp_c) + math.log(rh / 100.0)
        dew = (b * f) / (a - f)
        return round(dew, 2)
    except Exception:
        return -999.0


def should_bring_umbrella(weather: Dict[str, Any]) -> Dict[str, Any]:
    reasons: List[str] = []
    probs: List[float] = []

    # Direct precipitation indicators (weather id groups)
    w = weather.get('weather') or {}
    wid = w.get('id')
    desc = (w.get('description') or '').lower()
    main = (w.get('main') or '').lower()

    # If explicit rain/snow in description or weather id -> strong
    if isinstance(wid, int):
        if 200 <= wid < 300:  # thunderstorm
            probs.append(0.95); reasons.append('thunderstorm reported')
        elif 300 <= wid < 400:  # drizzle
            probs.append(0.6); reasons.append('drizzle reported')
        elif 500 <= wid < 600:  # rain
            probs.append(0.9); reasons.append('rain reported')
        elif 600 <= wid < 700:  # snow
            probs.append(0.9); reasons.append('snow reported')

    # Direct measured precipitation volume (if present)
    # OpenWeather may include rain: {'1h': x}
    rain_vol = None
    if isinstance(weather.get('rain'), dict):
        rain_vol = weather['rain'].get('1h')
    elif weather.get('rain') is not None:
        rain_vol = weather.get('rain')
    if rain_vol is not None:
        try:
            rv = float(rain_vol)
            if rv > 0:
                # map volume to probability (weak-to-strong)
                p = min(1.0, 0.5 + (rv / 10.0))
                probs.append(p)
                reasons.append(f'rain volume {rv} mm/h')
        except Exception:
            pass

    # Similar for snow
    snow_vol = None
    if isinstance(weather.get('snow'), dict):
        snow_vol = weather['snow'].get('1h')
    elif weather.get('snow') is not None:
        snow_vol = weather.get('snow')
    if snow_vol is not None:
        try:
            sv = float(snow_vol)
            if sv > 0:
                p = min(1.0, 0.6 + (sv / 10.0))
                probs.append(p)
                reasons.append(f'snow volume {sv} mm/h')
        except Exception:
            pass

    # Dew point proximity: compute dew point and difference
    temp = weather.get('temp')
    hum = weather.get('humidity')
    if temp is not None and hum is not None:
        try:
            dp = _dew_point(float(temp), float(hum))
            if dp > -100:
                delta = float(temp) - dp
                # smaller delta => more likely precipitation
                if delta <= 2:
                    probs.append(0.6); reasons.append(f'Dew point close to temperature ({dp}°C)')
                elif delta <= 4:
                    probs.append(0.35); reasons.append(f'Dew point moderately close ({dp}°C)')
                elif delta <= 6:
                    probs.append(0.15); reasons.append(f'Dew point somewhat close ({dp}°C)')
        except Exception:
            pass

    # Humidity
    if hum is not None:
        try:
            h = float(hum)
            if h >= 90:
                probs.append(0.5); reasons.append('very high humidity')
            elif h >= 75:
                probs.append(0.25); reasons.append('high humidity')
        except Exception:
            pass

    # Cloudiness
    clouds = weather.get('clouds')
    if clouds is not None:
        try:
            c = int(clouds)
            if c >= 90:
                probs.append(0.3); reasons.append('overcast clouds')
            elif c >= 60:
                probs.append(0.15); reasons.append('considerable cloudiness')
        except Exception:
            pass

    # Low pressure (sea-level) -- relative to standard ~1013 hPa
    pressure = weather.get('pressure')
    if pressure is not None:
        try:
            p_val = float(pressure)
            if p_val <= 1000:
                probs.append(0.2); reasons.append('low atmospheric pressure')
            elif p_val <= 1005:
                probs.append(0.1); reasons.append('slightly low pressure')
        except Exception:
            pass

    # Low visibility
    vis = weather.get('visibility')
    if vis is not None:
        try:
            v = int(vis)
            if v <= 2000:
                probs.append(0.25); reasons.append('low visibility')
        except Exception:
            pass

    # If no indicators were added, return low probability
    if not probs:
        return {'recommend': False, 'score': 0.0, 'reasons': ['no precipitation indicators found']}

    # Combine independent indicator probabilities using union formula
    prod = 1.0
    for p in probs:
        prod *= (1 - p)
    prob = 1 - prod
    prob = max(0.0, min(1.0, prob))

    recommend = prob >= 0.5

    return {'recommend': recommend, 'score': round(prob, 3), 'reasons': reasons}

