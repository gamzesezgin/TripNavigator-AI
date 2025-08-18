"""
TripAdvisor API Entegrasyon Test Dosyası
"""

import os
from dotenv import load_dotenv
from agents.tripadvisor_handler import (
    get_attractions_by_city,
    get_restaurants_by_city,
    get_fallback_attractions,
    get_fallback_restaurants,
    search_tripadvisor_locations
)

# .env dosyasını yükle
load_dotenv()

def test_tripadvisor_integration():
    """
    TripAdvisor API entegrasyonunu test eder
    """
    print("🧪 TripAdvisor API Entegrasyon Testi Başlatılıyor...")
    
    # API anahtarlarını kontrol et
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    
    print(f"🔑 RapidAPI Key: {'✅ Var' if rapidapi_key else '❌ Yok'}")
    
    # Test şehirleri
    test_cities = ["Roma", "Paris", "İstanbul"]
    
    for city in test_cities:
        print(f"\n🏙️ {city} için test ediliyor...")
        
        # Lokasyon arama testi
        print("  🔍 Lokasyon aranıyor...")
        try:
            locations = search_tripadvisor_locations(city, 1)
            if locations:
                print(f"    ✅ Lokasyon bulundu: {locations[0].get('name', 'İsimsiz')}")
                location_id = locations[0].get('locationId')
                print(f"    📍 Location ID: {location_id}")
            else:
                print("    ⚠️ Lokasyon bulunamadı")
        except Exception as e:
            print(f"    ❌ Lokasyon arama hatası: {e}")
        
        # Turistik yerler testi
        print("  📍 Turistik yerler alınıyor...")
        try:
            attractions = get_attractions_by_city(city, 3)
            if attractions:
                print(f"    ✅ {len(attractions)} turistik yer bulundu")
                for attraction in attractions[:2]:  # İlk 2'sini göster
                    print(f"      - {attraction.get('name', 'İsimsiz')} ({attraction.get('rating', 0)}/5)")
                    print(f"        📝 {attraction.get('review_count', 0)} yorum")
            else:
                print("    ⚠️ Turistik yer bulunamadı, fallback kullanılıyor")
                fallback_attractions = get_fallback_attractions(city)
                print(f"    📋 {len(fallback_attractions)} fallback yer")
        except Exception as e:
            print(f"    ❌ Hata: {e}")
        
        # Restoran testi
        print("  🍽️ Restoranlar alınıyor...")
        try:
            restaurants = get_restaurants_by_city(city, "genel", 3)
            if restaurants:
                print(f"    ✅ {len(restaurants)} restoran bulundu")
                for restaurant in restaurants[:2]:  # İlk 2'sini göster
                    print(f"      - {restaurant.get('name', 'İsimsiz')} ({restaurant.get('rating', 0)}/5)")
                    print(f"        📝 {restaurant.get('review_count', 0)} yorum")
                    print(f"        💰 {restaurant.get('price_level', '')}")
            else:
                print("    ⚠️ Restoran bulunamadı, fallback kullanılıyor")
                fallback_restaurants = get_fallback_restaurants(city, "genel")
                print(f"    📋 {len(fallback_restaurants)} fallback restoran")
        except Exception as e:
            print(f"    ❌ Hata: {e}")
    
    print("\n🎉 Test tamamlandı!")

if __name__ == "__main__":
    test_tripadvisor_integration()
