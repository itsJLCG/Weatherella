"""UV Index health recommendation logic.

UV Index Categories (WHO Standard):
- 0-2: Low (Green)
- 3-5: Moderate (Yellow)
- 6-7: High (Orange)
- 8-10: Very High (Red)
- 11+: Extreme (Violet)
"""
from typing import Dict, Any


def get_uv_recommendations(uv_index: float) -> Dict[str, Any]:
    """
    Generate health recommendations based on UV index.
    
    Args:
        uv_index: UV index value (0-15+)
        
    Returns:
        Dictionary with category, color, recommendations, and warnings
    """
    if uv_index < 0:
        return {
            'index': 0,
            'category': 'Unknown',
            'color': 'gray',
            'risk_level': 'unknown',
            'recommendations': ['UV data not available'],
            'protection_needed': False
        }
    
    # Low (0-2)
    if uv_index <= 2:
        return {
            'index': round(uv_index, 1),
            'category': 'Low',
            'color': 'green',
            'risk_level': 'minimal',
            'recommendations': [
                'No protection required',
                'You can safely stay outside',
                'Wear sunglasses on bright days',
            ],
            'protection_needed': False,
            'safe_exposure': 'Unlimited for most people'
        }
    
    # Moderate (3-5)
    elif uv_index <= 5:
        return {
            'index': round(uv_index, 1),
            'category': 'Moderate',
            'color': 'yellow',
            'risk_level': 'moderate',
            'recommendations': [
                'Take precautions during midday hours (10 AM - 4 PM)',
                'Seek shade when sun is strongest',
                'Wear sunglasses and use sunscreen SPF 30+',
                'Cover up with clothing if outside for extended periods',
            ],
            'protection_needed': True,
            'safe_exposure': '2-3 hours without protection',
            'sunscreen': 'SPF 30+ recommended'
        }
    
    # High (6-7)
    elif uv_index <= 7:
        return {
            'index': round(uv_index, 1),
            'category': 'High',
            'color': 'orange',
            'risk_level': 'high',
            'recommendations': [
                'Protection essential - reduce sun exposure 10 AM - 4 PM',
                'Seek shade during midday hours',
                'Wear protective clothing, hat, and sunglasses',
                'Apply sunscreen SPF 30+ every 2 hours',
                'Surfaces like sand and water increase UV exposure',
            ],
            'protection_needed': True,
            'safe_exposure': '1-2 hours without protection',
            'sunscreen': 'SPF 30-50+ required',
            'warning': 'Burns possible in less than 30 minutes'
        }
    
    # Very High (8-10)
    elif uv_index <= 10:
        return {
            'index': round(uv_index, 1),
            'category': 'Very High',
            'color': 'red',
            'risk_level': 'very_high',
            'recommendations': [
                'Extra protection needed - avoid sun exposure 10 AM - 4 PM',
                'Stay in shade whenever possible',
                'Wear long-sleeved shirt, pants, and wide-brimmed hat',
                'Apply sunscreen SPF 50+ every 2 hours',
                'Wear UV-blocking sunglasses',
                'Unprotected skin will burn quickly',
            ],
            'protection_needed': True,
            'safe_exposure': '15-30 minutes without protection',
            'sunscreen': 'SPF 50+ required',
            'warning': 'Serious sunburn risk - skin damage occurs rapidly'
        }
    
    # Extreme (11+)
    else:
        return {
            'index': round(uv_index, 1),
            'category': 'Extreme',
            'color': 'purple',
            'risk_level': 'extreme',
            'recommendations': [
                'Take all precautions - avoid outdoor activities',
                'Stay indoors during midday hours if possible',
                'If outside, stay in shade and cover all exposed skin',
                'Wear long-sleeved shirt, pants, and wide-brimmed hat',
                'Apply sunscreen SPF 50+ every 1-2 hours',
                'Wear wrap-around UV-blocking sunglasses',
            ],
            'protection_needed': True,
            'safe_exposure': 'Less than 15 minutes without protection',
            'sunscreen': 'SPF 50+ required, reapply frequently',
            'warning': 'Extreme risk - unprotected skin can burn in minutes'
        }


def get_protection_items(uv_index: float) -> Dict[str, bool]:
    """
    Get recommended protection items based on UV index.
    
    Returns:
        Dictionary indicating which protection items are recommended
    """
    if uv_index <= 2:
        return {
            'sunscreen': False,
            'sunglasses': True,
            'hat': False,
            'long_sleeves': False,
            'shade': False,
            'stay_indoors': False
        }
    elif uv_index <= 5:
        return {
            'sunscreen': True,
            'sunglasses': True,
            'hat': False,
            'long_sleeves': False,
            'shade': True,
            'stay_indoors': False
        }
    elif uv_index <= 7:
        return {
            'sunscreen': True,
            'sunglasses': True,
            'hat': True,
            'long_sleeves': True,
            'shade': True,
            'stay_indoors': False
        }
    elif uv_index <= 10:
        return {
            'sunscreen': True,
            'sunglasses': True,
            'hat': True,
            'long_sleeves': True,
            'shade': True,
            'stay_indoors': False
        }
    else:  # 11+
        return {
            'sunscreen': True,
            'sunglasses': True,
            'hat': True,
            'long_sleeves': True,
            'shade': True,
            'stay_indoors': True
        }


def get_skin_type_advice(uv_index: float, skin_type: int = 3) -> str:
    """
    Get personalized advice based on skin type (1-6, Fitzpatrick scale).
    
    Skin Types:
    1-2: Very fair to fair (burns easily)
    3-4: Medium (sometimes burns)
    5-6: Dark to very dark (rarely burns)
    """
    if uv_index <= 2:
        return "Safe for all skin types with minimal precautions"
    
    if skin_type <= 2:  # Fair skin
        if uv_index <= 5:
            return "Fair skin: Use SPF 50+, reapply every 2 hours"
        elif uv_index <= 7:
            return "Fair skin: High risk - Use SPF 50+, seek shade, wear protective clothing"
        else:
            return "Fair skin: Very high risk - Minimize outdoor exposure, full protection required"
    elif skin_type <= 4:  # Medium skin
        if uv_index <= 5:
            return "Medium skin: Use SPF 30+, take precautions during peak hours"
        elif uv_index <= 7:
            return "Medium skin: Use SPF 50+, wear hat and sunglasses"
        else:
            return "Medium skin: High risk - Full sun protection required"
    else:  # Dark skin
        if uv_index <= 5:
            return "Dark skin: Use SPF 15-30, basic precautions recommended"
        elif uv_index <= 7:
            return "Dark skin: Use SPF 30+, take precautions during peak hours"
        else:
            return "Dark skin: Use SPF 30-50+, avoid prolonged exposure"
