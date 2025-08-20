import requests
import streamlit as st
import json
from typing import Dict, List, Optional
import re
from urllib.parse import quote
import time # Hata durumunda beklemek için eklendi

class WikipediaAgent:
    """
    Wikipedia'dan şehir bilgilerini çeken agent
    """

    def __init__(self):
        self.base_url = "https://tr.wikipedia.org/api/rest_v1/page/summary/"
        self.search_url = "https://tr.wikipedia.org/w/api.php"
        # DÜZELTME 1: Wikipedia'nın istediği User-Agent'ı tanımlıyoruz.
        # Bu, 429 hatasını çözmek için en önemli adımdır.
        # E-posta veya bir web sitesi linki vermeniz tavsiye edilir.
        self.headers = {
            'User-Agent': 'TravelPlannerApp/1.0 (sizin_emailiniz@example.com)'
        }

    def search_city(self, city_name: str, max_retries: int = 3) -> Optional[Dict]:
        """
        Şehir için Wikipedia sayfası arar ve doğrudan özetini getirir.
        Hata durumunda birkaç kez tekrar dener.
        """
        retries = 0
        while retries < max_retries:
            try:
                # ... (params ve response = requests.get(...) kısmı aynı)
                params = { 'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': city_name, 'srlimit': 1, 'utf8': 1 }
                response = requests.get(self.search_url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                if 'query' in data and 'search' in data['query'] and data['query']['search']:
                    page_title = data['query']['search'][0]['title']
                    return self.get_summary_by_title(page_title) # Başarılı olursa fonksiyondan çık
                
                return None # Sonuç bulunamazsa çık
                
            except requests.exceptions.HTTPError as http_err:
                if http_err.response.status_code == 429:
                    retries += 1
                    print(f"!!! HATA (429), deneme {retries}/{max_retries}. 5 saniye bekleniyor...")
                    time.sleep(5)
                else:
                    st.error(f"Wikipedia HTTP hatası: {http_err}")
                    return None
            except Exception as e:
                st.error(f"Wikipedia arama hatası: {e}")
                return None
        
        print("Maksimum deneme sayısına ulaşıldı, arama başarısız.")
        return None

    def get_summary_by_title(self, page_title: str) -> Optional[Dict]:
        """
        Sayfa başlığı ile özet bilgi alır.
        """
        try:
            url = f"{self.base_url}{quote(page_title)}"
            # DÜZELTME 1: Her isteğe headers (kimlik bilgisi) ekliyoruz.
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            return {
                'title': data.get('title', ''),
                'extract': data.get('extract', ''),
                'content_urls': data.get('content_urls', {}),
                'thumbnail': data.get('thumbnail', {}),
                'coordinates': data.get('coordinates', {})
            }
            
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 429:
                print(f"!!! Özet alırken HATA (429): {page_title}. 5 saniye bekleniyor...")
                time.sleep(5) # Wikipedia engellerse 5 saniye bekle ve tekrar dene
                return self.get_summary_by_title(page_title) # Fonksiyonu tekrar çağır
            st.error(f"Wikipedia özet alma HTTP hatası: {http_err}")
            return None
        except Exception as e:
            print(f"Wikipedia özet alma hatası ({page_title}): {e}")
            return None

    def get_city_info(self, city_name: str) -> Dict:
        """
        Şehir bilgilerini alır ve işler
        """
        # KALDIRILDI: print(f"🔍 Wikipedia Agent: '{city_name}' şehri aranıyor...")
        
        clean_city = self.clean_city_name(city_name)
        
        if not clean_city:
            # KALDIRILDI: print(f"⚠️ '{city_name}' temizlenemedi, fallback kullanılıyor.")
            return self.get_fallback_city_info(city_name)

        wiki_data = self.search_city(clean_city)
        
        if wiki_data:
            processed_info = self.process_city_info(wiki_data, city_name)
            # KALDIRILDI: print(f"✅ Wikipedia Agent: '{city_name}' bilgileri alındı")
            return processed_info
        else:
            fallback_info = self.get_fallback_city_info(city_name)
            # KALDIRILDI: print(f"⚠️ Wikipedia Agent: '{clean_city}' için sonuç bulunamadı, fallback bilgi kullanılıyor")
            return fallback_info
    
    def clean_city_name(self, city_name: str) -> str:
        """
        Şehir adını Wikipedia araması için temizler.
        "AI Önerisi: Çeşme, Türkiye" gibi girdileri "Çeşme" haline getirir.
        """
        # DÜZELTME 2: Temizleme mantığını iyileştiriyoruz.
        # "AI Önerisi:" veya benzeri ön ekleri kaldır
        if ':' in city_name:
            city_name = city_name.split(':')[-1]
            
        # Ülke veya eyalet isimlerini kaldır (virgülden sonrasını at)
        city = city_name.split(',')[0]
        
        # Baştaki ve sondaki boşlukları temizle
        city = city.strip()
        
        # Gereksiz karakterleri temizle (isteğe bağlı)
        # city = re.sub(r'[^\w\s]', '', city) 
        
        return city
    
    # process_city_info ve get_fallback_city_info fonksiyonlarınızda
    # değişiklik yapmanıza gerek yok, onlar olduğu gibi kalabilir.
    def process_city_info(self, wiki_data: Dict, original_city: str) -> Dict:
        extract = wiki_data.get('extract', '')
        if len(extract) > 300:
            extract = extract[:300] + "..."
        
        coordinates = wiki_data.get('coordinates', {})
        lat = coordinates.get('lat', 0)
        lon = coordinates.get('lon', 0)
        
        thumbnail = wiki_data.get('thumbnail', {})
        image_url = thumbnail.get('source', '') if thumbnail else ''
        
        return {
            'city_name': original_city,
            'title': wiki_data.get('title', original_city),
            'summary': extract,
            'latitude': lat,
            'longitude': lon,
            'image_url': image_url,
            'wikipedia_url': wiki_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
            'source': 'Wikipedia'
        }
    
    def get_fallback_city_info(self, city_name: str) -> Dict:
        # Bu fonksiyon olduğu gibi kalabilir.
        return {'city_name': city_name, 'title': city_name, 'summary': f"{city_name} hakkında bilgi bulunamadı.", 'source': 'General Fallback'}


# Global agent instance
wikipedia_agent = WikipediaAgent()

@st.cache_data
def get_city_wikipedia_info(city_name: str) -> Dict:
    """
    Şehir için Wikipedia bilgilerini alır
    """
    return wikipedia_agent.get_city_info(city_name)