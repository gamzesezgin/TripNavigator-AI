"""
TripAdvisor API Handler Modülü
RapidAPI üzerinden TripAdvisor verilerini çeker
"""

import os
import requests
import streamlit as st
from typing import List, Dict, Any, Optional
import json

def get_rapidapi_key() -> Optional[str]:
    """
    RapidAPI anahtarını alır
    """
    # Önce environment variable'dan dene
    api_key = os.getenv('RAPIDAPI_KEY')
    
    # Eğer yoksa Streamlit secrets'tan dene
    if not api_key:
        try:
            api_key = st.secrets["RAPIDAPI_KEY"]
        except:
            pass
    
    return api_key

def search_tripadvisor_locations(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    TripAdvisor'da lokasyon arama
    """
    api_key = get_rapidapi_key()
    
    if not api_key:
        st.warning("⚠️ RapidAPI anahtarı bulunamadı. Fallback veriler kullanılıyor.")
        return []
    
    try:
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
        }
        
        params = {
            "query": query,
            "limit": limit
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            st.error(f"❌ TripAdvisor API hatası: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:
        st.error("❌ API'den cevap alınamadı (Zaman aşımı).")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API isteği sırasında hata: {e}")
        return []
    except Exception as e:
        st.error(f"❌ Beklenmeyen hata: {e}")
        return []

def get_tripadvisor_attractions(location_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    TripAdvisor'dan turistik yerler getirir
    """
    api_key = get_rapidapi_key()
    
    if not api_key:
        st.warning("⚠️ RapidAPI anahtarı bulunamadı. Fallback veriler kullanılıyor.")
        return []
    
    try:
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/attractions/searchAttractions"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
        }
        
        params = {
            "locationId": location_id,
            "language": "tr",
            "currencyCode": "TRY",
            "limit": limit
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            attractions = data.get('data', [])
            
            # Sonuçları formatla
            formatted_attractions = []
            for attraction in attractions:
                formatted_attraction = {
                    'name': attraction.get('name', 'İsimsiz'),
                    'kind': attraction.get('category', {}).get('name', 'Turistik Yer'),
                    'city': attraction.get('location', {}).get('city', ''),
                    'neighborhood': attraction.get('location', {}).get('address', ''),
                    'description': attraction.get('description', '')[:200] if attraction.get('description') else '',
                    'short_reason': f"TripAdvisor'da {attraction.get('rating', 0)}/5 puanlı popüler yer",
                    'rating': attraction.get('rating', 0),
                    'website': attraction.get('website', ''),
                    'phone': attraction.get('phone', ''),
                    'address': attraction.get('location', {}).get('address', ''),
                    'price_level': '💰💰' if attraction.get('priceLevel', 0) > 2 else '💰',
                    'review_count': attraction.get('numReviews', 0),
                    'tripadvisor_url': f"https://www.tripadvisor.com{attraction.get('url', '')}",
                    'image_url': attraction.get('photo', {}).get('images', {}).get('original', {}).get('url', '')
                }
                formatted_attractions.append(formatted_attraction)
            
            return formatted_attractions
        else:
            st.error(f"❌ TripAdvisor API hatası: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:
        st.error("❌ API'den cevap alınamadı (Zaman aşımı).")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API isteği sırasında hata: {e}")
        return []
    except Exception as e:
        st.error(f"❌ Beklenmeyen hata: {e}")
        return []

def get_tripadvisor_restaurants(location_id: str, cuisine: str = "genel", limit: int = 10) -> List[Dict[str, Any]]:
    """
    TripAdvisor'dan restoranlar getirir
    """
    api_key = get_rapidapi_key()
    
    if not api_key:
        st.warning("⚠️ RapidAPI anahtarı bulunamadı. Fallback veriler kullanılıyor.")
        return []
    
    try:
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurants/searchRestaurants"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
        }
        
        # Mutfak türüne göre filtreleme
        cuisine_mapping = {
            "genel": "",
            "balık ekmek": "seafood",
            "kebap": "bbq",
            "lahmacun": "turkish",
            "kahve": "cafe",
            "çay": "cafe",
            "tatlı": "dessert",
            "dondurma": "ice_cream",
            "pizza": "pizza",
            "sushi": "sushi",
            "burger": "burger",
            "çorba": "soup"
        }
        
        cuisine_filter = cuisine_mapping.get(cuisine.lower(), "")
        
        params = {
            "locationId": location_id,
            "language": "tr",
            "currencyCode": "TRY",
            "limit": limit
        }
        
        if cuisine_filter:
            params["cuisine"] = cuisine_filter
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('data', [])
            
            # Sonuçları formatla
            formatted_restaurants = []
            for restaurant in restaurants:
                formatted_restaurant = {
                    'name': restaurant.get('name', 'İsimsiz'),
                    'category': restaurant.get('category', {}).get('name', 'Restoran'),
                    'cuisine': cuisine.title(),
                    'neighborhood': restaurant.get('location', {}).get('address', ''),
                    'city': restaurant.get('location', {}).get('city', ''),
                    'description': restaurant.get('description', '')[:200] if restaurant.get('description') else '',
                    'rating': restaurant.get('rating', 0),
                    'website': restaurant.get('website', ''),
                    'phone': restaurant.get('phone', ''),
                    'address': restaurant.get('location', {}).get('address', ''),
                    'price_level': '💰💰💰' if restaurant.get('priceLevel', 0) > 3 else ('💰💰' if restaurant.get('priceLevel', 0) > 1 else '💰'),
                    'review_count': restaurant.get('numReviews', 0),
                    'tripadvisor_url': f"https://www.tripadvisor.com{restaurant.get('url', '')}",
                    'image_url': restaurant.get('photo', {}).get('images', {}).get('original', {}).get('url', ''),
                    'cuisine_types': [cuisine.get('name', '') for cuisine in restaurant.get('cuisines', [])]
                }
                formatted_restaurants.append(formatted_restaurant)
            
            return formatted_restaurants
        else:
            st.error(f"❌ TripAdvisor API hatası: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:
        st.error("❌ API'den cevap alınamadı (Zaman aşımı).")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API isteği sırasında hata: {e}")
        return []
    except Exception as e:
        st.error(f"❌ Beklenmeyen hata: {e}")
        return []

def get_attractions_by_city(city: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Şehir adına göre turistik yerler getirir
    """
    # Önce şehri ara
    locations = search_tripadvisor_locations(city, 1)
    
    if not locations:
        st.warning(f"⚠️ '{city}' şehri TripAdvisor'da bulunamadı.")
        return []
    
    # İlk lokasyonu al
    location_id = locations[0].get('locationId')
    
    if not location_id:
        st.warning(f"⚠️ '{city}' için location ID bulunamadı.")
        return []
    
    # Turistik yerleri getir
    return get_tripadvisor_attractions(location_id, limit)

def get_restaurants_by_city(city: str, cuisine: str = "genel", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Şehir adına göre restoranlar getirir
    """
    # Önce şehri ara
    locations = search_tripadvisor_locations(city, 1)
    
    if not locations:
        st.warning(f"⚠️ '{city}' şehri TripAdvisor'da bulunamadı.")
        return []
    
    # İlk lokasyonu al
    location_id = locations[0].get('locationId')
    
    if not location_id:
        st.warning(f"⚠️ '{city}' için location ID bulunamadı.")
        return []
    
    # Restoranları getir
    return get_tripadvisor_restaurants(location_id, cuisine, limit)

# Fallback fonksiyonlar (API çalışmazsa)
def get_fallback_attractions(city: str) -> List[Dict[str, Any]]:
    """
    API çalışmadığında kullanılacak fallback veriler
    """
    fallback_data = {
        "roma": [
            {"name": "Colosseum", "kind": "Historic", "description": "Antik Roma'nın en büyük amfitiyatrosu", "rating": 4.8, "review_count": 50000},
            {"name": "Vatican Museums", "kind": "Museum", "description": "Dünyanın en büyük sanat koleksiyonlarından biri", "rating": 4.7, "review_count": 45000},
            {"name": "Trevi Fountain", "kind": "Monument", "description": "Roma'nın en ünlü çeşmesi", "rating": 4.6, "review_count": 40000},
            {"name": "Pantheon", "kind": "Historic", "description": "Antik Roma tapınağı", "rating": 4.5, "review_count": 35000}
        ],
        "paris": [
            {"name": "Eiffel Tower", "kind": "Monument", "description": "Paris'in sembolü", "rating": 4.8, "review_count": 60000},
            {"name": "Louvre Museum", "kind": "Museum", "description": "Dünyanın en büyük sanat müzesi", "rating": 4.7, "review_count": 55000},
            {"name": "Notre-Dame Cathedral", "kind": "Historic", "description": "Gotik mimarinin şaheseri", "rating": 4.6, "review_count": 50000},
            {"name": "Arc de Triomphe", "kind": "Monument", "description": "Zafer takı", "rating": 4.5, "review_count": 45000}
        ],
        "istanbul": [
            {"name": "Hagia Sophia", "kind": "Historic", "description": "Bizans mimarisinin başyapıtı", "rating": 4.8, "review_count": 40000},
            {"name": "Blue Mosque", "kind": "Historic", "description": "Sultanahmet Camii", "rating": 4.7, "review_count": 35000},
            {"name": "Topkapi Palace", "kind": "Historic", "description": "Osmanlı sarayı", "rating": 4.6, "review_count": 30000},
            {"name": "Grand Bazaar", "kind": "Shopping", "description": "Dünyanın en büyük kapalı çarşısı", "rating": 4.5, "review_count": 25000}
        ]
    }
    
    city_lower = city.lower()
    for key in fallback_data:
        if key in city_lower:
            return fallback_data[key]
    
    # Genel fallback
    return [
        {"name": "City Center", "kind": "Tourism", "description": "Şehir merkezi", "rating": 4.0, "review_count": 1000},
        {"name": "Main Square", "kind": "Tourism", "description": "Ana meydan", "rating": 4.0, "review_count": 1000},
        {"name": "Local Museum", "kind": "Museum", "description": "Yerel müze", "rating": 4.0, "review_count": 1000},
        {"name": "Historic District", "kind": "Historic", "description": "Tarihi bölge", "rating": 4.0, "review_count": 1000}
    ]

def get_fallback_restaurants(city: str, cuisine: str) -> List[Dict[str, Any]]:
    """
    API çalışmadığında kullanılacak fallback restoran verileri
    """
    return [
        {
            "name": f"Local {cuisine.title()} Restaurant",
            "category": "Restoran",
            "cuisine": cuisine.title(),
            "neighborhood": "Şehir Merkezi",
            "city": city,
            "description": f"Yerel {cuisine} mutfağının en iyi örnekleri",
            "rating": 4.2,
            "review_count": 500,
            "website": "",
            "phone": "",
            "address": f"{city} Merkez",
            "price_level": "💰💰"
        },
        {
            "name": f"Traditional {cuisine.title()} Place",
            "category": "Restoran",
            "cuisine": cuisine.title(),
            "neighborhood": "Eski Şehir",
            "city": city,
            "description": f"Geleneksel {cuisine} lezzetleri",
            "rating": 4.0,
            "review_count": 300,
            "website": "",
            "phone": "",
            "address": f"{city} Eski Şehir",
            "price_level": "💰"
        }
    ]
