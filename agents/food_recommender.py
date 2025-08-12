import requests
import streamlit as st
from typing import List, Dict, Optional
import json

class FoodRecommender:
    """OpenTripMap API kullanarak yemek mekanları öneren sistem"""
    
    def __init__(self):
        # OpenTripMap API - ücretsiz, günlük 1000 istek
        self.api_key = "5ae2e3f221c38a28845f05b6e1f72c6e6f4b8a6c8b8c8b8c8b8c8b8c8b8c8b8c"  # Demo key
        self.base_url = "https://api.opentripmap.com/0.1/en/places"
        
        # Yemek kategorileri
        self.food_categories = {
            "restaurant": "Restoran",
            "cafe": "Kafe",
            "bar": "Bar",
            "fast_food": "Fast Food",
            "bakery": "Fırın",
            "ice_cream": "Dondurma",
            "confectionery": "Tatlıcı"
        }
    
    def search_food_places(self, location: str, category: str = "restaurant", limit: int = 10) -> List[Dict]:
        """
        Belirli bir konumda yemek mekanları arar
        
        Args:
            location: Konum (şehir, mahalle, vb.)
            category: Yemek kategorisi
            limit: Maksimum sonuç sayısı
        
        Returns:
            Yemek mekanları listesi
        """
        try:
            # 1. Önce konumu koordinatlara çevir
            geocode_url = f"https://api.opentripmap.com/0.1/en/places/geosearch"
            geocode_params = {
                "name": location,
                "limit": 1,
                "apikey": self.api_key
            }
            
            geocode_response = requests.get(geocode_url, params=geocode_params, timeout=10)
            geocode_response.raise_for_status()
            
            geocode_data = geocode_response.json()
            
            if not geocode_data:
                return []
            
            # Koordinatları al
            lat = geocode_data[0]["lat"]
            lon = geocode_data[0]["lon"]
            
            # 2. Yemek mekanlarını ara
            places_url = f"{self.base_url}/radius"
            places_params = {
                "radius": 5000,  # 5km yarıçap
                "lon": lon,
                "lat": lat,
                "kinds": category,
                "limit": limit,
                "apikey": self.api_key
            }
            
            places_response = requests.get(places_url, params=places_params, timeout=10)
            places_response.raise_for_status()
            
            places_data = places_response.json()
            
            # 3. Sonuçları işle
            food_places = []
            for place in places_data.get("features", []):
                properties = place.get("properties", {})
                
                # Detay bilgileri al
                place_details = self._get_place_details(properties.get("xid"))
                
                food_place = {
                    "name": properties.get("name", "İsimsiz"),
                    "category": self.food_categories.get(category, category),
                    "address": properties.get("address", {}).get("road", ""),
                    "neighborhood": properties.get("address", {}).get("suburb", ""),
                    "city": properties.get("address", {}).get("city", location),
                    "rating": place_details.get("rating", {}).get("average", 0),
                    "cuisine": place_details.get("cuisine", ""),
                    "price_level": place_details.get("price", ""),
                    "opening_hours": place_details.get("opening_hours", {}),
                    "website": place_details.get("url", ""),
                    "phone": place_details.get("phone", ""),
                    "description": place_details.get("wikipedia_extracts", {}).get("text", ""),
                    "tags": place_details.get("kinds", "").split(",")[:5] if place_details.get("kinds") else [],
                    "lat": place.get("geometry", {}).get("coordinates", [0, 0])[1],
                    "lon": place.get("geometry", {}).get("coordinates", [0, 0])[0],
                    "distance": properties.get("distance", 0)
                }
                
                food_places.append(food_place)
            
            # Mesafeye göre sırala
            food_places.sort(key=lambda x: x.get("distance", 0))
            
            return food_places[:limit]
            
        except Exception as e:
            st.error(f"Yemek mekanları aranırken hata oluştu: {str(e)}")
            return []
    
    def _get_place_details(self, xid: str) -> Dict:
        """Yer detaylarını al"""
        if not xid:
            return {}
        
        try:
            details_url = f"{self.base_url}/xid/{xid}"
            params = {"apikey": self.api_key}
            
            response = requests.get(details_url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception:
            return {}
    
    def search_by_cuisine(self, location: str, cuisine: str, limit: int = 10) -> List[Dict]:
        """Belirli mutfak türünde yerler ara"""
        # Mutfak türüne göre kategori belirle
        if cuisine.lower() in ["türk", "turkish", "kebap", "lahmacun"]:
            category = "restaurant"
        elif cuisine.lower() in ["kahve", "coffee", "çay", "tea"]:
            category = "cafe"
        elif cuisine.lower() in ["tatlı", "dessert", "dondurma", "ice cream"]:
            category = "confectionery"
        else:
            category = "restaurant"
        
        places = self.search_food_places(location, category, limit)
        
        # Mutfak türüne göre filtrele
        if cuisine.lower() != "genel":
            filtered_places = []
            for place in places:
                place_cuisine = place.get("cuisine", "").lower()
                place_tags = [tag.lower() for tag in place.get("tags", [])]
                place_name = place.get("name", "").lower()
                
                if (cuisine.lower() in place_cuisine or 
                    cuisine.lower() in place_tags or 
                    cuisine.lower() in place_name):
                    filtered_places.append(place)
            
            return filtered_places[:limit]
        
        return places
    
    def get_popular_food_places(self, location: str, top_k: int = 8) -> List[Dict]:
        """Popüler yemek mekanlarını getir"""
        # Farklı kategorilerden yerler al
        all_places = []
        
        # Restoranlar
        restaurants = self.search_food_places(location, "restaurant", top_k // 2)
        all_places.extend(restaurants)
        
        # Kafeler
        cafes = self.search_food_places(location, "cafe", top_k // 2)
        all_places.extend(cafes)
        
        # Rating'e göre sırala
        all_places.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        return all_places[:top_k]

# Kullanım örneği
def get_food_recommendations(location: str, cuisine: str = "genel", top_k: int = 8) -> List[Dict]:
    """Ana fonksiyon - yemek önerileri al"""
    recommender = FoodRecommender()
    
    if cuisine == "genel":
        return recommender.get_popular_food_places(location, top_k)
    else:
        return recommender.search_by_cuisine(location, cuisine, top_k)

# Test fonksiyonu
if __name__ == "__main__":
    # Test
    places = get_food_recommendations("Eminönü", "balık ekmek", 5)
    print(json.dumps(places, indent=2, ensure_ascii=False))
