import streamlit as st
import json
import requests
import re

def generate_goal_specific_questions(goal):
    """
    Hedef bazında özelleştirilmiş sorular oluşturur.
    """
    goal_lower = goal.lower()
    
    # Diyet ve sağlık hedefleri için
    if any(keyword in goal_lower for keyword in ['diyet', 'kilo', 'sağlık', 'beslenme', 'zayıflama', 'fitness', 'spor', 'egzersiz']):
        return [
            {
                "question": "Daha önce diyet/spor deneyiminiz var mı?",
                "options": [
                    "Evet, başarılı oldum ve sürdürdüm",
                    "Evet ama sürdüremedim",
                    "Ara sıra denedim",
                    "Hiç denemedim, ilk kez"
                ]
            },
            {
                "question": "Günlük rutininiz nasıl?",
                "options": [
                    "Çok yoğun, az zamanım var",
                    "Orta yoğunlukta, esnek zamanım var",
                    "Rahat, çok zamanım var",
                    "Değişken, düzenli değil"
                ]
            },
            {
                "question": "Motivasyon kaynağınız nedir?",
                "options": [
                    "Sağlık ve uzun ömür",
                    "Görünüm ve özgüven",
                    "Sosyal baskı/çevre",
                    "Kişisel hedef ve başarı"
                ]
            },
            {
                "question": "Hangi tür aktiviteleri tercih edersiniz?",
                "options": [
                    "Evde yapabileceğim egzersizler",
                    "Spor salonu ve grup aktiviteleri",
                    "Açık hava ve doğa aktiviteleri",
                    "Yoga/pilates gibi sakin aktiviteler"
                ]
            },
            {
                "question": "Beslenme konusunda hangi yaklaşımı tercih edersiniz?",
                "options": [
                    "Sıkı kurallar ve ölçümler",
                    "Esnek ama bilinçli beslenme",
                    "Hazır diyet programları",
                    "Kendi tariflerim ve denemeler"
                ]
            }
        ]
    
    # Öğrenme hedefleri için
    elif any(keyword in goal_lower for keyword in ['öğren', 'çalış', 'ders', 'kurs', 'eğitim', 'okul', 'üniversite']):
        return [
            {
                "question": "Öğrenme tarzınız nedir?",
                "options": [
                    "Görsel öğrenme (video, resim)",
                    "İşitsel öğrenme (ses, konuşma)",
                    "Kinestetik öğrenme (pratik, deneyim)",
                    "Okuma/yazma odaklı"
                ]
            },
            {
                "question": "Günlük çalışma süreniz ne kadar?",
                "options": [
                    "30 dakika veya daha az",
                    "1-2 saat",
                    "3-4 saat",
                    "5 saat veya daha fazla"
                ]
            },
            {
                "question": "Hangi ortamda daha iyi çalışırsınız?",
                "options": [
                    "Sessiz ve düzenli ortam",
                    "Müzik eşliğinde",
                    "Grup çalışması",
                    "Değişken ortamlar"
                ]
            },
            {
                "question": "Motivasyon kaynağınız nedir?",
                "options": [
                    "Kariyer ve gelecek",
                    "Kişisel gelişim",
                    "Sosyal baskı",
                    "İlgi ve merak"
                ]
            },
            {
                "question": "Hangi kaynakları tercih edersiniz?",
                "options": [
                    "Video dersler ve online kurslar",
                    "Kitaplar ve yazılı materyaller",
                    "Pratik projeler ve uygulamalar",
                    "Grup tartışmaları ve mentorluk"
                ]
            }
        ]
    
    # Kariyer hedefleri için
    elif any(keyword in goal_lower for keyword in ['kariyer', 'iş', 'meslek', 'profesyonel', 'çalışma']):
        return [
            {
                "question": "Kariyer hedefiniz nedir?",
                "options": [
                    "Yeni bir alana geçiş",
                    "Mevcut pozisyonda yükselme",
                    "Yeni beceriler kazanma",
                    "Kendi işini kurma"
                ]
            },
            {
                "question": "Günlük iş yoğunluğunuz nasıl?",
                "options": [
                    "Çok yoğun, az zamanım var",
                    "Orta yoğunlukta",
                    "Rahat, esnek zamanım var",
                    "Değişken yoğunluk"
                ]
            },
            {
                "question": "Hangi tür gelişimi tercih edersiniz?",
                "options": [
                    "Teknik beceriler",
                    "Liderlik ve yönetim",
                    "İletişim ve networking",
                    "Yaratıcılık ve inovasyon"
                ]
            },
            {
                "question": "Öğrenme yönteminiz nedir?",
                "options": [
                    "Online kurslar ve sertifikalar",
                    "Mentorluk ve koçluk",
                    "Pratik projeler ve deneyim",
                    "Konferanslar ve networking"
                ]
            },
            {
                "question": "Zaman yönetimi yaklaşımınız nedir?",
                "options": [
                    "Sıkı program ve planlama",
                    "Esnek ama düzenli",
                    "Anlık kararlar",
                    "Haftalık hedefler"
                ]
            }
        ]
    
    # Genel hedefler için varsayılan sorular
    else:
        return [
            {
                "question": "Bu hedefe ulaşmak için hangi yaklaşımı tercih edersiniz?",
                "options": [
                    "Adım adım planlı ilerleme",
                    "Esnek ve uyarlanabilir yaklaşım",
                    "Yoğun ve hızlı ilerleme",
                    "Sakin ve sürdürülebilir yaklaşım"
                ]
            },
            {
                "question": "Günlük zamanınız nasıl?",
                "options": [
                    "Çok yoğun, az zamanım var",
                    "Orta yoğunlukta",
                    "Rahat, çok zamanım var",
                    "Değişken zaman"
                ]
            },
            {
                "question": "Motivasyon kaynağınız nedir?",
                "options": [
                    "Kişisel başarı ve tatmin",
                    "Dış baskı ve beklentiler",
                    "Sosyal onay ve tanınma",
                    "İçsel merak ve ilgi"
                ]
            },
            {
                "question": "Hangi tür aktiviteleri tercih edersiniz?",
                "options": [
                    "Yapılandırılmış ve düzenli",
                    "Yaratıcı ve esnek",
                    "Sosyal ve etkileşimli",
                    "Bireysel ve odaklanmış"
                ]
            },
            {
                "question": "İlerleme takibi konusunda nasılsınız?",
                "options": [
                    "Detaylı notlar ve ölçümler",
                    "Genel gözlem ve his",
                    "Düzenli değerlendirme",
                    "Anlık geri bildirim"
                ]
            }
        ]

def generate_learning_style_questions():
    """
    Geriye uyumluluk için eski fonksiyon (artık kullanılmıyor)
    """
    return generate_goal_specific_questions("genel hedef")

def analyze_learning_style(answers):
    """
    Öğrenme tarzı cevaplarını analiz ederek öğrenme tarzını belirler.
    """
    if not answers or len(answers) < 5:
        return "Çok Yönlü"
    
    # Her cevap için puan hesapla
    scores = {
        "Görsel": 0,
        "İşitsel": 0,
        "Kinestetik": 0,
        "Okuma/Yazma": 0
    }
    
    # Soru 1: Öğrenme yöntemi
    if answers[0] == 0:  # Görsel materyaller
        scores["Görsel"] += 2
    elif answers[0] == 1:  # Dinleyerek
        scores["İşitsel"] += 2
    elif answers[0] == 2:  # Pratik yaparak
        scores["Kinestetik"] += 2
    elif answers[0] == 3:  # Okuyarak
        scores["Okuma/Yazma"] += 2
    
    # Soru 2: Problem çözme
    if answers[1] == 0:  # Mantıksal
        scores["Okuma/Yazma"] += 1
    elif answers[1] == 1:  # Yaratıcı
        scores["Görsel"] += 1
    elif answers[1] == 2:  # Tartışarak
        scores["İşitsel"] += 1
    elif answers[1] == 3:  # Örneklerle
        scores["Kinestetik"] += 1
    
    # Soru 3: Öğrenme ortamı
    if answers[2] == 0:  # Sessiz ortam
        scores["Okuma/Yazma"] += 1
    elif answers[2] == 1:  # Müzikli ortam
        scores["İşitsel"] += 1
    elif answers[2] == 2:  # Grup ortamı
        scores["Kinestetik"] += 1
    elif answers[2] == 3:  # Bağımsız
        scores["Görsel"] += 1
    
    # Soru 4: Hatırlama yöntemi
    if answers[3] == 0:  # Görsel imgeler
        scores["Görsel"] += 2
    elif answers[3] == 1:  # Sesler
        scores["İşitsel"] += 2
    elif answers[3] == 2:  # Hareket
        scores["Kinestetik"] += 2
    elif answers[3] == 3:  # Yazılı notlar
        scores["Okuma/Yazma"] += 2
    
    # Soru 5: Kaynak tercihi
    if answers[4] == 0:  # Video/animasyon
        scores["Görsel"] += 1
    elif answers[4] == 1:  # Podcast/sesli
        scores["İşitsel"] += 1
    elif answers[4] == 2:  # Uygulamalı
        scores["Kinestetik"] += 1
    elif answers[4] == 3:  # Kitaplar
        scores["Okuma/Yazma"] += 1
    
    # En yüksek puanı alan öğrenme tarzını belirle
    max_score = max(scores.values())
    learning_styles = [style for style, score in scores.items() if score == max_score]
    
    if len(learning_styles) > 1:
        return "Çok Yönlü"
    else:
        return learning_styles[0]

def generate_plan_with_gemini(goal, api_key, days=7, start_day=0):
    """
    Kullanıcının isteği doğrultusunda güncellenmiş prompt'u kullanarak
    Gemini API'sinden bir eylem planı oluşturur. Bu, projenin son,
    temizlenmiş versiyonudur.
    """
    if not api_key:
        st.error("API anahtarı bulunamadı. Lütfen .env dosyasını ve kodunuzu kontrol edin.")
        return None
    
    # Gün isimlerini belirle
    day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    selected_days = day_names[start_day:start_day + days]
    
    prompt = f"""
Kullanıcının belirttiği hedef: "{goal}"

Bu hedefi detaylı şekilde analiz et ve {days} günlük bir plan oluştur. Her gün için 3-4 adet ÇOK SPESİFİK, ÖLÇÜLEBİLİR ve YAPILABİLİR görev belirle.

Görevler şu kriterlere uygun olmalı:
- HEDEFE ÖZEL: Hedefle doğrudan ilgili ve spesifik
- ÖLÇÜLEBİLİR: Sayısal değerler içermeli (örn: 10 kelime, 30 dakika, 1 bölüm)
- GÜNLÜK: O gün tamamlanabilir
- SPESİFİK: Genel değil, net ve belirli
- MOTİVASYONEL: Başarı hissi verecek

ÖRNEKLER:
- İngilizce için: "10 yeni kelime ezberle", "1 bölüm İngilizce altyazılı dizi izle", "30 dakika İngilizce podcast dinle"
- Diyet için: "Kahvaltıda 2 yumurta ve 1 dilim tam tahıllı ekmek ye", "Günde 2 litre su iç", "Akşam yemeğini 19:00'dan önce tamamla"
- Spor için: "30 dakika yürüyüş yap", "20 şınav çek", "10 dakika plank yap"

Cevabın SADECE aşağıdaki formatta bir JSON objesi olmalıdır:
{{
  "weekly_tasks": [
    {{
      "day": "{selected_days[0]}",
      "tasks": [
        "Spesifik görev 1 (sayısal değerlerle)",
        "Spesifik görev 2 (sayısal değerlerle)",
        "Spesifik görev 3 (sayısal değerlerle)"
      ]
    }}{f''',
    {{
      "day": "{selected_days[1]}",
      "tasks": [
        "Spesifik görev 1 (sayısal değerlerle)",
        "Spesifik görev 2 (sayısal değerlerle)",
        "Spesifik görev 3 (sayısal değerlerle)"
      ]
    }}''' if days > 1 else ''}{f''',
    {{
      "day": "{selected_days[2]}",
      "tasks": [
        "Spesifik görev 1 (sayısal değerlerle)",
        "Spesifik görev 2 (sayısal değerlerle)",
        "Spesifik görev 3 (sayısal değerlerle)"
      ]
    }}''' if days > 2 else ''}{f''',
    {{
      "day": "{selected_days[3]}",
      "tasks": [
        "Spesifik görev 1 (sayısal değerlerle)",
        "Spesifik görev 2 (sayısal değerlerle)",
        "Spesifik görev 3 (sayısal değerlerle)"
      ]
    }}''' if days > 3 else ''}{f''',
    {{
      "day": "{selected_days[4]}",
      "tasks": [
        "Spesifik görev 1 (sayısal değerlerle)",
        "Spesifik görev 2 (sayısal değerlerle)",
        "Spesifik görev 3 (sayısal değerlerle)"
      ]
    }}''' if days > 4 else ''}{f''',
    {{
      "day": "{selected_days[5]}",
      "tasks": [
        "Spesifik görev 1 (sayısal değerlerle)",
        "Spesifik görev 2 (sayısal değerlerle)",
        "Spesifik görev 3 (sayısal değerlerle)"
      ]
    }}''' if days > 5 else ''}{f''',
    {{
      "day": "{selected_days[6]}",
      "tasks": [
        "Spesifik görev 1 (sayısal değerlerle)",
        "Spesifik görev 2 (sayısal değerlerle)",
        "Spesifik görev 3 (sayısal değerlerle)"
      ]
    }}''' if days > 6 else ''}
  ]
}}

ÖNEMLİ: Her görev sayısal değerler içermeli ve çok spesifik olmalı. Genel görevler verme!
Lütfen sadece JSON formatında yanıt ver, başka hiçbir açıklama ekleme.
"""
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    payload = {
      "contents": [{"parts": [{"text": prompt}]}],
      "generationConfig": {
        "responseMimeType": "application/json",
        "temperature": 0.5,
        "maxOutputTokens": 2048,
      }
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        # Yavaş bağlantılar için bekleme süresi 90 saniye olarak ayarlandı.
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=90)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # JSON içeriğini temizle ve parse et
            try:
                # JSON içeriğini bulmak için regex kullan
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_content = json_match.group()
                    parsed_result = json.loads(json_content)
                    
                    # Gerekli alanların varlığını kontrol et
                    if 'weekly_tasks' in parsed_result and isinstance(parsed_result['weekly_tasks'], list):
                        return parsed_result
                    else:
                        st.error("API yanıtında 'weekly_tasks' alanı bulunamadı veya geçersiz format.")
                        return None
                else:
                    st.error("API yanıtında JSON formatı bulunamadı.")
                    return None
                    
            except json.JSONDecodeError as json_error:
                st.error(f"JSON parsing hatası: {json_error}")
                return None
        else:
            st.error("API'den beklenen formatda bir cevap alınamadı. Lütfen tekrar deneyin.")
            return None
            
    except requests.exceptions.Timeout:
        st.error("API'den cevap alınamadı (Zaman aşımı). Lütfen internet bağlantınızı kontrol edin veya daha sonra tekrar deneyin.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API isteği sırasında bir ağ hatası oluştu: {e}")
        return None
    except Exception as e:
        st.error(f"Beklenmedik bir hata oluştu: {e}")
        return None