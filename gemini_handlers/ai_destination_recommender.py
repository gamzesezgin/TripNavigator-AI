"""
AI Destinasyon Önerici Modülü
Gemini API kullanarak AI destekli destinasyon önerileri oluşturur
"""

import os
import requests
import streamlit as st
from typing import List, Dict, Any

def get_gemini_api_key():
    """
    Gemini API anahtarını alır
    """
    # Önce environment variable'dan dene
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Eğer yoksa Streamlit secrets'tan dene
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass
    
    return api_key

def call_gemini_api(prompt: str) -> Dict[str, Any]:
    """
    Gemini API'yi çağırır
    """
    api_key = get_gemini_api_key()
    
    if not api_key:
        st.error("API anahtarı bulunamadı. Lütfen .env dosyasını ve kodunuzu kontrol edin.")
        return None
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        }
    }
    
    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API hatası: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("API'den cevap alınamadı (Zaman aşımı). Lütfen internet bağlantınızı kontrol edin veya daha sonra tekrar deneyin.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API isteği sırasında hata: {e}")
        return None

def generate_ai_destination_recommendation(answers: List[str], ai_questions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    AI kullanarak destinasyon önerisi oluşturur
    """
    print("🤖 AI Destinasyon Önerisi Başlatılıyor...")
    
    # Kullanıcı tercihlerini analiz et
    preferences = {}
    
    for i, (question, answer) in enumerate(zip(ai_questions, answers)):
        question_text = question["question"]
        preferences[f"Soru {i+1}: {question_text}"] = answer
    
    # Mesafe tercihini belirle
    distance_preference = "Genel"
    for answer in answers:
        if "türkiye" in answer.lower():
            distance_preference = "Türkiye içi"
        elif "avrupa" in answer.lower() or "yakın" in answer.lower():
            distance_preference = "Avrupa (yakın)"
        elif "uzak" in answer.lower():
            distance_preference = "Uzak"
    
    # AI prompt'unu oluştur
    prompt = f"""
Bu tercihlere göre dünyadaki en uygun 3 destinasyon öner. 

ÖNEMLİ: 
- Eğer "Türkiye içi" seçildiyse, SADECE Türkiye içi destinasyonlar öner
- Eğer "Avrupa (yakın)" seçildiyse, SADECE Avrupa destinasyonları öner  
- Eğer "Uzak" seçildiyse, farklı kıtalardan destinasyonlar öner

Kullanıcı Tercihleri:
"""
    
    for key, value in preferences.items():
        prompt += f"- {key}: {value}\n"
    
    prompt += f"""
Mesafe Tercihi: {distance_preference}

Lütfen sadece 3 destinasyon öner ve her biri için kısa bir açıklama ver.
Format:
1. [Destinasyon Adı] - [Kısa Açıklama]
2. [Destinasyon Adı] - [Kısa Açıklama]  
3. [Destinasyon Adı] - [Kısa Açıklama]

Sadece bu formatta yanıt ver, başka açıklama ekleme.
"""
    
    print("📤 AI'ya istek gönderiliyor...")
    
    try:
        result = call_gemini_api(prompt)
        
        if result and 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # Debug için AI yanıtını göster
            print(f"🤖 AI Yanıtı: {content}")
            
            # Yanıtı temizle
            content = content.strip()
            
            # Satırlara böl
            lines = content.split('\n')
            
            destinations = []
            
            # Her satırı kontrol et
            for line in lines:
                line = line.strip()
                
                # Boş satırları atla
                if not line:
                    continue
                
                # Numaralı satırları kontrol et (1., 2., 3.)
                if line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                    # Numarayı kaldır ve temizle
                    clean_line = line[2:].strip()
                    
                    # Tire işaretini bul
                    if ' - ' in clean_line:
                        parts = clean_line.split(' - ', 1)
                        if len(parts) == 2:
                            name = parts[0].strip()
                            description = parts[1].strip()
                            
                            destinations.append({
                                "name": name,
                                "description": description
                            })
                            print(f"✅ AI'dan Bulunan Destinasyon: {name} - {description}")
            
            if len(destinations) >= 3:
                print("🎉 AI'dan 3 destinasyon başarıyla alındı!")
                return destinations[:3]
            elif len(destinations) > 0:
                print(f"⚠️ AI'dan sadece {len(destinations)} destinasyon alındı, fallback ile tamamlanıyor...")
                fallback_destinations = generate_fallback_destinations(answers, ai_questions, destinations)
                return fallback_destinations[:3]
            else:
                print("❌ AI'dan geçerli destinasyon alınamadı, fallback sistemi devreye giriyor...")
                fallback_destinations = generate_fallback_destinations(answers, ai_questions, [])
                return fallback_destinations[:3]
        else:
            print("❌ AI'dan geçerli yanıt alınamadı, fallback sistemi devreye giriyor...")
            fallback_destinations = generate_fallback_destinations(answers, ai_questions, [])
            return fallback_destinations[:3]
            
    except Exception as e:
        print(f"❌ AI önerisi alınırken hata: {e}")
        print("🔄 Fallback sistemi devreye giriyor...")
        fallback_destinations = generate_fallback_destinations(answers, ai_questions, [])
        return fallback_destinations[:3]

def generate_fallback_destinations(answers: List[str], ai_questions: List[Dict[str, Any]], existing_destinations: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    AI yanıtı alınamadığında kullanıcı tercihlerine göre 3 destinasyon önerir
    """
    print("🔄 Fallback sistemi: Kod içi şehir listesinden öneriler oluşturuluyor...")
    
    # Mevcut destinasyonları kopyala
    destinations = existing_destinations.copy()
    
    # Kullanıcı tercihlerini analiz et
    preferences = {}
    for i, (question, answer) in enumerate(zip(ai_questions, answers)):
        question_text = question["question"].lower()
        answer_text = answer.lower()
        preferences[question_text] = answer_text
    
    # Mesafe tercihini belirle
    distance_preference = "genel"
    for answer in answers:
        if "türkiye" in answer.lower():
            distance_preference = "türkiye"
        elif "avrupa" in answer.lower() or "yakın" in answer.lower():
            distance_preference = "avrupa"
        elif "uzak" in answer.lower():
            distance_preference = "uzak"
    
    # Türkiye içi destinasyonlar
    if distance_preference == "türkiye":
        turkey_destinations = [
            {"name": "İstanbul", "description": "Tarih, kültür ve modern yaşam"},
            {"name": "Antalya", "description": "Plaj, tarih ve doğa"},
            {"name": "Kapadokya", "description": "Doğal güzellikler ve tarih"},
            {"name": "İzmir", "description": "Ege kültürü ve lezzetler"},
            {"name": "Bursa", "description": "Tarih ve termal kaplıcalar"},
            {"name": "Trabzon", "description": "Karadeniz doğası ve kültürü"},
            {"name": "Konya", "description": "Tasavvuf kültürü ve tarih"},
            {"name": "Gaziantep", "description": "Gastronomi ve tarih"},
            {"name": "Mardin", "description": "Tarihi mimari ve kültür"},
            {"name": "Van", "description": "Doğa ve tarih"}
        ]
        
        # Kullanıcı tercihlerine göre filtrele
        for dest in turkey_destinations:
            if len(destinations) >= 3:
                break
            if dest not in destinations:
                destinations.append(dest)
    
    # Avrupa destinasyonları
    elif distance_preference == "avrupa":
        europe_destinations = [
            {"name": "Paris, Fransa", "description": "Sanat, kültür ve romantizm"},
            {"name": "Roma, İtalya", "description": "Tarih, sanat ve gastronomi"},
            {"name": "Barcelona, İspanya", "description": "Mimari, kültür ve plaj"},
            {"name": "Amsterdam, Hollanda", "description": "Kültür, sanat ve kanallar"},
            {"name": "Prag, Çekya", "description": "Tarih, mimari ve biralar"},
            {"name": "Viyana, Avusturya", "description": "Müzik, sanat ve tarih"},
            {"name": "Budapeşte, Macaristan", "description": "Tarih, spa ve kültür"},
            {"name": "Atina, Yunanistan", "description": "Antik tarih ve deniz"},
            {"name": "Lizbon, Portekiz", "description": "Tarih, deniz ve lezzetler"},
            {"name": "Krakow, Polonya", "description": "Tarih, kültür ve mimari"}
        ]
        
        for dest in europe_destinations:
            if len(destinations) >= 3:
                break
            if dest not in destinations:
                destinations.append(dest)
    
    # Uzak destinasyonlar
    elif distance_preference == "uzak":
        far_destinations = [
            {"name": "Tokyo, Japonya", "description": "Teknoloji, kültür ve gastronomi"},
            {"name": "New York, ABD", "description": "Şehir hayatı, sanat ve kültür"},
            {"name": "Bangkok, Tayland", "description": "Kültür, lezzetler ve tapınaklar"},
            {"name": "Singapur", "description": "Modern şehir ve kültür"},
            {"name": "Sydney, Avustralya", "description": "Doğa, plaj ve şehir hayatı"},
            {"name": "Cape Town, Güney Afrika", "description": "Dağ ve deniz manzarası, tarih"},
            {"name": "Rio de Janeiro, Brezilya", "description": "Plaj, karnaval ve doğa"},
            {"name": "Mumbai, Hindistan", "description": "Kültür, tarih ve lezzetler"},
            {"name": "Mexico City, Meksika", "description": "Tarih, kültür ve gastronomi"},
            {"name": "Dubai, BAE", "description": "Modern şehir ve lüks"}
        ]
        
        for dest in far_destinations:
            if len(destinations) >= 3:
                break
            if dest not in destinations:
                destinations.append(dest)
    
    # Genel destinasyonlar
    else:
        general_destinations = [
            {"name": "İstanbul, Türkiye", "description": "Tarih, kültür ve modern yaşam"},
            {"name": "Paris, Fransa", "description": "Sanat, kültür ve romantizm"},
            {"name": "Roma, İtalya", "description": "Tarih, sanat ve gastronomi"},
            {"name": "Barcelona, İspanya", "description": "Mimari, kültür ve plaj"},
            {"name": "Tokyo, Japonya", "description": "Teknoloji, kültür ve gastronomi"},
            {"name": "New York, ABD", "description": "Şehir hayatı, sanat ve kültür"},
            {"name": "Bangkok, Tayland", "description": "Kültür, lezzetler ve tapınaklar"},
            {"name": "Amsterdam, Hollanda", "description": "Kültür, sanat ve kanallar"},
            {"name": "Prag, Çekya", "description": "Tarih, mimari ve biralar"},
            {"name": "Cape Town, Güney Afrika", "description": "Dağ ve deniz manzarası, tarih"}
        ]
        
        for dest in general_destinations:
            if len(destinations) >= 3:
                break
            if dest not in destinations:
                destinations.append(dest)
    
    print(f"✅ Fallback sistemi: {len(destinations[:3])} destinasyon önerisi hazırlandı")
    return destinations[:3]

def generate_recommendation_reasoning(answers: List[str], ai_questions: List[Dict[str, Any]], selected_destination: str) -> str:
    """
    Seçilen destinasyon için öneri gerekçesi oluşturur
    """
    # Basit gerekçe oluşturma
    reasoning_parts = []
    
    for i, (question, answer) in enumerate(zip(ai_questions, answers)):
        question_text = question["question"]
        
        # Soru türüne göre gerekçe oluştur
        if "bütçe" in question_text.lower():
            if "yüksek" in answer.lower() or "lüks" in answer.lower():
                reasoning_parts.append("Lüks deneyimler için uygun")
            elif "orta" in answer.lower():
                reasoning_parts.append("Kaliteli ama ekonomik seçenekler")
            elif "düşük" in answer.lower():
                reasoning_parts.append("Ekonomik seyahat imkanları")
        
        elif "aktivite" in question_text.lower() or "yoğunluk" in question_text.lower():
            if "yoğun" in answer.lower() or "aktif" in answer.lower():
                reasoning_parts.append("Yoğun aktivite programları")
            elif "orta" in answer.lower() or "dengeli" in answer.lower():
                reasoning_parts.append("Dengeli aktivite seçenekleri")
            elif "rahat" in answer.lower() or "az" in answer.lower():
                reasoning_parts.append("Rahat ve dinlendirici aktiviteler")
        
        elif "kültür" in question_text.lower() or "müze" in question_text.lower():
            if "müze" in answer.lower() or "tarih" in answer.lower():
                reasoning_parts.append("Zengin kültürel miras")
            elif "yerel" in answer.lower():
                reasoning_parts.append("Otantik yerel deneyimler")
            elif "sanat" in answer.lower():
                reasoning_parts.append("Sanat ve kültür odaklı")
    
    if reasoning_parts:
        return f"{selected_destination} seçimi şu tercihlerinize dayanmaktadır: {', '.join(reasoning_parts)}."
    else:
        return f"{selected_destination} seçimi genel seyahat tercihlerinize uygun olarak önerilmiştir."
