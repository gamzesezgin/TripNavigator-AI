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

def generate_plan_with_gemini(goal: str, travel_style: str = None, plan_days: int = 3) -> Dict[str, Any]:
    """
    Gemini API kullanarak detaylı seyahat planı oluşturur
    """
    print(f"🤖 Plan Üretimi Başlatılıyor: {goal}")
    
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
    for day in range(1, plan_days + 1):
        prompt += f"""
GÜN {day}:
- 09:00: [Aktivite adı ve açıklaması]
- 12:00: [Aktivite adı ve açıklaması]
- 15:00: [Aktivite adı ve açıklaması]
- 18:00: [Aktivite adı ve açıklaması]
"""
    
    prompt += f"""
ÖNEMLİ:
- Her aktivite için saat belirt
- Aktivite sırası mantıklı olsun (yakın yerler bir arada)
- Yemek molaları dahil edilsin
- Ulaşım bilgileri eklenebilir
- Bütçe dostu ve lüks seçenekler karışık olsun
- Yerel deneyimler ve turistik yerler dengeli olsun

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
            if (line.upper().startswith('GÜN ') or 
                line.upper().startswith('DAY ') or 
                line.upper().startswith('1. GÜN') or
                line.upper().startswith('2. GÜN') or
                line.upper().startswith('3. GÜN') or
                line.upper().startswith('4. GÜN') or
                line.upper().startswith('5. GÜN') or
                line.upper().startswith('6. GÜN') or
                line.upper().startswith('7. GÜN')):
                
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

def generate_fallback_plan(goal: str, travel_style: str = None, plan_days: int = 3) -> Dict[str, Any]:
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
    for day in range(1, plan_days + 1):
        simple_prompt += f"""
GÜN {day}:
- 09:00: Aktivite 1
- 12:00: Aktivite 2
- 15:00: Aktivite 3
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

def generate_hardcoded_fallback_plan(goal: str, travel_style: str = None, plan_days: int = 3) -> Dict[str, Any]:
    """
    AI tamamen çalışmadığında kod içi plan şablonları kullanır
    """
    print("🔄 Kod içi plan şablonları kullanılıyor...")
    
    # Hedef türüne göre genel plan şablonu
    goal_lower = goal.lower()
    
    if "roma" in goal_lower:
        days = []
        roma_activities = [
            ["09:00: Colosseum ve Roman Forum ziyareti", "12:00: Vittorio Emanuele II Anıtı ve Piazza Venezia", "15:00: Trevi Çeşmesi ve Pantheon", "18:00: Piazza Navona ve Campo de' Fiori"],
            ["09:00: Vatikan Müzeleri ve Sistine Şapeli", "12:00: St. Peter's Bazilikası", "15:00: Castel Sant'Angelo", "18:00: Trastevere mahallesi akşam yemeği"],
            ["09:00: Villa Borghese ve Borghese Galerisi", "12:00: Piazza del Popolo", "15:00: İspanyol Merdivenleri", "18:00: Via del Corso alışveriş"],
            ["09:00: Ostia Antica arkeolojik alanı", "12:00: Tivoli ve Villa d'Este", "15:00: Hadrian Villası", "18:00: Roma'da geleneksel yemek"],
            ["09:00: Trastevere mahallesi keşfi", "12:00: Testaccio pazarı", "15:00: Aventino Tepesi", "18:00: Roma gece hayatı"],
            ["09:00: Borghese Galerisi", "12:00: Villa Medici", "15:00: Pincio Tepesi", "18:00: Roma'da son akşam"],
            ["09:00: Roma'da son kahvaltı", "12:00: Son alışveriş", "15:00: Roma'ya veda", "18:00: Dönüş hazırlığı"]
        ]
        
        for day in range(1, min(plan_days + 1, 8)):
            days.append({
                "day": f"GÜN {day}",
                "activities": roma_activities[day - 1]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }
    
    elif "paris" in goal_lower:
        days = []
        paris_activities = [
            ["09:00: Eiffel Kulesi ziyareti", "12:00: Champs-Élysées yürüyüşü", "15:00: Arc de Triomphe", "18:00: Seine Nehri tekne turu"],
            ["09:00: Louvre Müzesi", "12:00: Notre-Dame Katedrali", "15:00: Sainte-Chapelle", "18:00: Montmartre ve Sacré-Cœur"],
            ["09:00: Versailles Sarayı", "12:00: Musée d'Orsay", "15:00: Place de la Concorde", "18:00: Tuileries Bahçesi"],
            ["09:00: Musée Rodin", "12:00: Invalides", "15:00: Champ de Mars", "18:00: Paris'te geleneksel yemek"],
            ["09:00: Père Lachaise Mezarlığı", "12:00: Belleville mahallesi", "15:00: Canal Saint-Martin", "18:00: Paris gece hayatı"],
            ["09:00: Centre Pompidou", "12:00: Marais mahallesi", "15:00: Place des Vosges", "18:00: Paris'te son akşam"],
            ["09:00: Paris'te son kahvaltı", "12:00: Son alışveriş", "15:00: Paris'e veda", "18:00: Dönüş hazırlığı"]
        ]
        
        for day in range(1, min(plan_days + 1, 8)):
            days.append({
                "day": f"GÜN {day}",
                "activities": paris_activities[day - 1]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }
    
    elif "istanbul" in goal_lower:
        days = []
        istanbul_activities = [
            ["09:00: Ayasofya ve Sultanahmet Camii", "12:00: Topkapı Sarayı", "15:00: Yerebatan Sarnıcı", "18:00: Sultanahmet Meydanı"],
            ["09:00: Kapalı Çarşı alışveriş", "12:00: Galata Kulesi", "15:00: İstiklal Caddesi yürüyüşü", "18:00: Boğaz turu"],
            ["09:00: Dolmabahçe Sarayı", "12:00: Ortaköy Camii", "15:00: Beşiktaş ve Nişantaşı", "18:00: Taksim Meydanı"],
            ["09:00: Süleymaniye Camii", "12:00: Fatih mahallesi", "15:00: Eyüp Sultan Camii", "18:00: İstanbul'da geleneksel yemek"],
            ["09:00: Büyükada turu", "12:00: Adalar keşfi", "15:00: Deniz manzarası", "18:00: İstanbul gece hayatı"],
            ["09:00: Çamlıca Tepesi", "12:00: Üsküdar mahallesi", "15:00: Kız Kulesi", "18:00: İstanbul'da son akşam"],
            ["09:00: İstanbul'da son kahvaltı", "12:00: Son alışveriş", "15:00: İstanbul'a veda", "18:00: Dönüş hazırlığı"]
        ]
        
        for day in range(1, min(plan_days + 1, 8)):
            days.append({
                "day": f"GÜN {day}",
                "activities": istanbul_activities[day - 1]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }
    
    else:
        # Genel plan şablonu
        days = []
        general_activities = [
            ["09:00: Şehir merkezi keşif turu", "12:00: Ana turistik yerler ziyareti", "15:00: Yerel restoranlarda yemek", "18:00: Akşam şehir manzarası"],
            ["09:00: Müze ve kültür merkezleri", "12:00: Tarihi yerler ziyareti", "15:00: Yerel pazar alışverişi", "18:00: Geleneksel yemek deneyimi"],
            ["09:00: Doğa ve park ziyaretleri", "12:00: Alışveriş ve eğlence", "15:00: Kafeler ve barlar", "18:00: Veda akşam yemeği"],
            ["09:00: Şehir dışı tur", "12:00: Yakın kasaba ziyareti", "15:00: Doğa aktiviteleri", "18:00: Yerel deneyimler"],
            ["09:00: Sanat galerileri", "12:00: Tarihi mahalleler", "15:00: Yerel el sanatları", "18:00: Kültürel gösteriler"],
            ["09:00: Şehir parkları", "12:00: Rekreasyon alanları", "15:00: Spor aktiviteleri", "18:00: Şehir gece hayatı"],
            ["09:00: Son gün kahvaltısı", "12:00: Son alışveriş", "15:00: Şehre veda", "18:00: Dönüş hazırlığı"]
        ]
        
        for day in range(1, min(plan_days + 1, 8)):
            days.append({
                "day": f"GÜN {day}",
                "activities": general_activities[day - 1]
            })
        
        return {
            "days": days,
            "total_days": len(days)
        }

# Fonksiyonları export et
__all__ = ['generate_plan_with_gemini', 'generate_fallback_plan', 'generate_hardcoded_fallback_plan']
