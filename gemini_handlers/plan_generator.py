"""
Plan Üretici Modülü
Gemini API kullanarak detaylı seyahat planları oluşturur
"""

import os
import requests
import streamlit as st
from typing import Dict, Any, List

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
            "maxOutputTokens": 2048,
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

def generate_plan_with_gemini(goal: str, travel_style: str = None, plan_days: int = 3, start_day: str = "Pazartesi") -> Dict[str, Any]:
    """
    Gemini API kullanarak detaylı seyahat planı oluşturur
    """
    print(f"🤖 Plan Üretimi Başlatılıyor: {goal}")
    
    # Gün isimlerini belirle
    day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    start_day_index = day_names.index(start_day) if start_day in day_names else 0
    
    # Seyahat tarzına göre prompt oluştur
    style_context = ""
    if travel_style:
        if "doğa" in travel_style.lower() or "macera" in travel_style.lower():
            style_context = """
Seyahat Tarzı: Doğa ve Macera
- Doğa aktiviteleri ve macera sporları öncelikli
- Trekking, dağ yürüyüşleri, su sporları
- Doğa fotoğrafçılığı ve gözlem
- Kamp ve doğa konaklama seçenekleri
"""
        elif "tarih" in travel_style.lower() or "kültür" in travel_style.lower():
            style_context = """
Seyahat Tarzı: Kültür ve Tarih
- Müzeler ve tarihi yerler öncelikli
- Kültür turları ve rehberli geziler
- Geleneksel restoranlar ve yerel deneyimler
- Tarihi oteller ve butik konaklama
"""
        elif "sanat" in travel_style.lower() or "gastronomi" in travel_style.lower():
            style_context = """
Seyahat Tarzı: Sanat ve Gastronomi
- Sanat galerileri ve müzeler
- Gastronomi deneyimleri ve yemek turları
- Şarap tadımı ve kokteyl barlar
- Lüks restoranlar ve fine dining
"""
        elif "alışveriş" in travel_style.lower() or "eğlence" in travel_style.lower():
            style_context = """
Seyahat Tarzı: Alışveriş ve Eğlence
- Alışveriş merkezleri ve çarşılar
- Gece hayatı ve eğlence mekanları
- Kafeler ve restoranlar
- Şehir turları ve aktiviteler
"""
        elif "tatil" in travel_style.lower() or "dinlenme" in travel_style.lower():
            style_context = """
Seyahat Tarzı: Tatil ve Dinlenme
- Rahat ve dinlendirici aktiviteler
- Spa ve wellness merkezleri
- Plaj aktiviteleri ve dinlenme
- Lüks resort ve oteller
"""
        elif "karışık" in travel_style.lower():
            style_context = """
Seyahat Tarzı: Karışık
- Kültür, eğlence ve dinlenme dengesi
- Çeşitli aktivite seçenekleri
- Farklı konaklama türleri
- Yerel ve turistik deneyimler
"""
    
    # AI prompt'unu oluştur
    prompt = f"""
Bu seyahat hedefi için detaylı bir günlük plan oluştur:

Hedef: {goal}
Gün Sayısı: {plan_days} gün

{style_context}

Lütfen şu formatta yanıt ver:

"""
    
    # Dinamik gün sayısına göre prompt oluştur
    for day in range(plan_days):
        current_day_index = (start_day_index + day) % 7
        current_day_name = day_names[current_day_index]
        prompt += f"""
{current_day_name}:
- [Aktivite adı ve açıklaması]
- [Aktivite adı ve açıklaması]
- [Aktivite adı ve açıklaması]
- [Aktivite adı ve açıklaması]
"""
    
    prompt += f"""
ÖNEMLİ:
- Dil ve Ton: Bana ikinci tekil şahıs ("sen/siz") kullanarak hitap et. "Sabah ilk olarak Topkapı Sarayı'nı keşfedebilirsin" gibi yönlendirici ve tavsiye veren bir dil kullan. Asla "ilk olarak sarayı geziyoruz, sonra yemeğe gidiyoruz" gibi "biz" diliyle yazma.

- Mantıksal Akış: Her günün planını, mekanların birbirine yakınlığını göz önünde bulundurarak coğrafi olarak mantıklı bir sırayla oluştur. Birbirine uzak yerler arasında gidip gelerek zaman kaybettirme.

- Yemek Molaları: Her gün için en az bir öğle ve bir akşam yemeği önerisi ekle. Bu öneriler gezilen bölgeye yakın olmalı.

- Doğal Bilgi Akışı: Ulaşım, bütçe ve diğer notları parantez içinde verme. Bunun yerine, "Karaköy'e vapurla geçtikten sonra, sizi ortalama bir bütçeyle harika lezzetler sunan bir esnaf lokantası karşılayacak" gibi akıcı ve doğal cümleler kur.

- Dengeli Seçenekler: Hem dünyaca ünlü turistik yerlere (Ayasofya, Kapalıçarşı gibi) hem de daha az bilinen yerel deneyimlere (Balat'ta bir kahve molası, Kadıköy balık pazarını gezmek gibi) planda yer ver. Yemek önerilerinde de bütçe dostu esnaf lokantaları ve lüks restoranlar gibi farklı seçenekler sun.

- Dengeli Plan: Dünyaca ünlü turistik yerlere (İstanbul'daAyasofya, Kapalıçarşı gibi), ikonik yemek duraklarını (Viyana'da Figlmüller ve Kafe Demel vb.), şehrin mutlaka görülmesi gereken turistik yerlerini dengeli bir şekilde programa dahil et.

Sadece bu formatta yanıt ver, başka açıklama ekleme.
"""
    
    print("📤 AI'ya plan isteği gönderiliyor...")
    
    try:
        result = call_gemini_api(prompt)
        
        if result and 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            print(f"🤖 AI Plan Yanıtı: {content}")
            
            # Yanıtı parse et
            plan = parse_ai_plan(content)
            
            if plan:
                print("✅ Plan başarıyla oluşturuldu!")
                return plan
            else:
                print("❌ Plan parse edilemedi, fallback plan oluşturuluyor...")
                return generate_fallback_plan(goal, travel_style, plan_days)
        else:
            print("❌ AI'dan geçerli yanıt alınamadı, fallback plan oluşturuluyor...")
            return generate_fallback_plan(goal, travel_style, plan_days)
            
    except Exception as e:
        print(f"❌ Plan oluşturulurken hata: {e}")
        print("🔄 Fallback plan oluşturuluyor...")
        return generate_fallback_plan(goal, travel_style, plan_days)

def parse_ai_plan(content: str) -> Dict[str, Any]:
    """
    AI'dan gelen plan yanıtını parse eder
    """
    try:
        lines = content.strip().split('\n')
        plan = {
            "days": [],
            "total_days": 0
        }
        
        current_day = None
        current_activities = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Gün başlığını kontrol et (daha esnek)
            day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
            is_day_header = (line.upper().startswith('GÜN ') or 
                line.upper().startswith('DAY ') or 
                line.upper().startswith('1. GÜN') or
                line.upper().startswith('2. GÜN') or
                line.upper().startswith('3. GÜN') or
                line.upper().startswith('4. GÜN') or
                line.upper().startswith('5. GÜN') or
                line.upper().startswith('6. GÜN') or
                line.upper().startswith('7. GÜN') or
                any(line.startswith(day) for day in day_names))
            
            if is_day_header:
                # Önceki günü kaydet
                if current_day and current_activities:
                    plan["days"].append({
                        "day": current_day,
                        "activities": current_activities
                    })
                
                # Yeni gün başlat
                current_day = line
                current_activities = []
            
            # Aktivite satırını kontrol et (daha esnek)
            elif ((line.startswith('- ') or line.startswith('• ') or line.startswith('* ')) and current_day):
                activity = line[2:].strip() if line.startswith('- ') else line[1:].strip()
                if activity:
                    current_activities.append(activity)
            
            # Saatli aktivite formatını da kontrol et
            elif current_day and (':' in line and ('09:' in line or '10:' in line or '11:' in line or 
                                 '12:' in line or '13:' in line or '14:' in line or 
                                 '15:' in line or '16:' in line or '17:' in line or 
                                 '18:' in line or '19:' in line or '20:' in line)):
                activity = line.strip()
                if activity:
                    current_activities.append(activity)
        
        # Son günü ekle
        if current_day and current_activities:
            plan["days"].append({
                "day": current_day,
                "activities": current_activities
            })
        
        plan["total_days"] = len(plan["days"])
        
        if plan["total_days"] > 0:
            return plan
        else:
            return None
            
    except Exception as e:
        print(f"Plan parse hatası: {e}")
        return None

def generate_fallback_plan(goal: str, travel_style: str = None, plan_days: int = 3, start_day: str = "Pazartesi") -> Dict[str, Any]:
    """
    AI yanıtı alınamadığında fallback plan oluşturur
    """
    print("🔄 Fallback plan sistemi: Basitleştirilmiş AI isteği deneniyor...")
    
    # Basitleştirilmiş prompt ile tekrar dene
    simple_prompt = f"""
{goal} için {plan_days} günlük basit seyahat planı oluştur.

Format:
"""
    
    # Dinamik gün sayısına göre fallback prompt oluştur
    day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    start_day_index = day_names.index(start_day) if start_day in day_names else 0
    
    for day in range(plan_days):
        current_day_index = (start_day_index + day) % 7
        current_day_name = day_names[current_day_index]
        simple_prompt += f"""
{current_day_name}:
- Aktivite 1
- Aktivite 2
- Aktivite 3
"""
    
    simple_prompt += """
Sadece bu formatta yanıt ver.
"""
    
    try:
        print("🔄 Basitleştirilmiş AI isteği gönderiliyor...")
        result = call_gemini_api(simple_prompt)
        
        if result and 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Fallback AI yanıtı alındı: {content}")
            
            # Yanıtı parse et
            plan = parse_ai_plan(content)
            
            if plan:
                print("✅ Fallback AI planı başarıyla oluşturuldu!")
                return plan
            else:
                print("❌ Fallback AI planı parse edilemedi, kod içi plana geçiliyor...")
                return generate_hardcoded_fallback_plan(goal, travel_style, plan_days)
        else:
            print("❌ Fallback AI'dan yanıt alınamadı, kod içi plana geçiliyor...")
            return generate_hardcoded_fallback_plan(goal, travel_style, plan_days)
            
    except Exception as e:
        print(f"❌ Fallback AI hatası: {e}")
        print("🔄 Kod içi plana geçiliyor...")
        return generate_hardcoded_fallback_plan(goal, travel_style, plan_days)

def generate_hardcoded_fallback_plan(goal: str, travel_style: str = None, plan_days: int = 3, start_day: str = "Pazartesi") -> Dict[str, Any]:
    """
    AI tamamen çalışmadığında kod içi plan şablonları kullanır
    """
    print("🔄 Kod içi plan şablonları kullanılıyor...")
    
    # Hedef türüne göre genel plan şablonu
    goal_lower = goal.lower()
    
    if "roma" in goal_lower:
        days = []
        roma_activities = [
            ["Colosseum ve Roman Forum ziyareti", "Vittorio Emanuele II Anıtı ve Piazza Venezia", "Trevi Çeşmesi ve Pantheon", "Piazza Navona ve Campo de' Fiori"],
            ["Vatikan Müzeleri ve Sistine Şapeli", "St. Peter's Bazilikası", "Castel Sant'Angelo", "Trastevere mahallesi akşam yemeği"],
            ["Villa Borghese ve Borghese Galerisi", "Piazza del Popolo", "İspanyol Merdivenleri", "Via del Corso alışveriş"],
            ["Ostia Antica arkeolojik alanı", "Tivoli ve Villa d'Este", "Hadrian Villası", "Roma'da geleneksel yemek"],
            ["Trastevere mahallesi keşfi", "Testaccio pazarı", "Aventino Tepesi", "Roma gece hayatı"],
            ["Borghese Galerisi", "Villa Medici", "Pincio Tepesi", "Roma'da son akşam"],
            ["Roma'da son kahvaltı", "Son alışveriş", "Roma'ya veda", "Dönüş hazırlığı"]
        ]
        
        day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        start_day_index = day_names.index(start_day) if start_day in day_names else 0
        
        for day in range(min(plan_days, 7)):
            current_day_index = (start_day_index + day) % 7
            current_day_name = day_names[current_day_index]
            days.append({
                "day": current_day_name,
                "activities": roma_activities[day]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }
    
    elif "paris" in goal_lower:
        days = []
        paris_activities = [
            ["Eiffel Kulesi ziyareti", "Champs-Élysées yürüyüşü", "Arc de Triomphe", "Seine Nehri tekne turu"],
            ["Louvre Müzesi", "Notre-Dame Katedrali", "Sainte-Chapelle", "Montmartre ve Sacré-Cœur"],
            ["Versailles Sarayı", "Musée d'Orsay", "Place de la Concorde", "Tuileries Bahçesi"],
            ["Musée Rodin", "Invalides", "Champ de Mars", "Paris'te geleneksel yemek"],
            ["Père Lachaise Mezarlığı", "Belleville mahallesi", "Canal Saint-Martin", "Paris gece hayatı"],
            ["Centre Pompidou", "Marais mahallesi", "Place des Vosges", "Paris'te son akşam"],
            ["Paris'te son kahvaltı", "Son alışveriş", "Paris'e veda", "Dönüş hazırlığı"]
        ]
        
        for day in range(min(plan_days, 7)):
            current_day_index = (start_day_index + day) % 7
            current_day_name = day_names[current_day_index]
            days.append({
                "day": current_day_name,
                "activities": paris_activities[day]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }
    
    elif "istanbul" in goal_lower:
        days = []
        istanbul_activities = [
            ["Ayasofya ve Sultanahmet Camii", "Topkapı Sarayı", "Yerebatan Sarnıcı", "Sultanahmet Meydanı"],
            ["Kapalı Çarşı alışveriş", "Galata Kulesi", "İstiklal Caddesi yürüyüşü", "Boğaz turu"],
            ["Dolmabahçe Sarayı", "Ortaköy Camii", "Beşiktaş ve Nişantaşı", "Taksim Meydanı"],
            ["Süleymaniye Camii", "Fatih mahallesi", "Eyüp Sultan Camii", "İstanbul'da geleneksel yemek"],
            ["Büyükada turu", "Adalar keşfi", "Deniz manzarası", "İstanbul gece hayatı"],
            ["Çamlıca Tepesi", "Üsküdar mahallesi", "Kız Kulesi", "İstanbul'da son akşam"],
            ["İstanbul'da son kahvaltı", "Son alışveriş", "İstanbul'a veda", "Dönüş hazırlığı"]
        ]
        
        for day in range(min(plan_days, 7)):
            current_day_index = (start_day_index + day) % 7
            current_day_name = day_names[current_day_index]
            days.append({
                "day": current_day_name,
                "activities": istanbul_activities[day]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }
    
    else:
        # Genel plan şablonu
        days = []
        general_activities = [
            ["Şehir merkezi keşif turu", "Ana turistik yerler ziyareti", "Yerel restoranlarda yemek", "Akşam şehir manzarası"],
            ["Müze ve kültür merkezleri", "Tarihi yerler ziyareti", "Yerel pazar alışverişi", "Geleneksel yemek deneyimi"],
            ["Doğa ve park ziyaretleri", "Alışveriş ve eğlence", "Kafeler ve barlar", "Veda akşam yemeği"],
            ["Şehir dışı tur", "Yakın kasaba ziyareti", "Doğa aktiviteleri", "Yerel deneyimler"],
            ["Sanat galerileri", "Tarihi mahalleler", "Yerel el sanatları", "Kültürel gösteriler"],
            ["Şehir parkları", "Rekreasyon alanları", "Spor aktiviteleri", "Şehir gece hayatı"],
            ["Son gün kahvaltısı", "Son alışveriş", "Şehre veda", "Dönüş hazırlığı"]
        ]
        
        for day in range(min(plan_days, 7)):
            current_day_index = (start_day_index + day) % 7
            current_day_name = day_names[current_day_index]
            days.append({
                "day": current_day_name,
                "activities": general_activities[day]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }

# Fonksiyonları export et
__all__ = ['generate_plan_with_gemini', 'generate_fallback_plan', 'generate_hardcoded_fallback_plan']
