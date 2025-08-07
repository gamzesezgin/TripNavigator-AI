import streamlit as st
import json
import requests
import re

def generate_goal_specific_questions(goal):
    """
    Seyahat hedefi bazında özelleştirilmiş sorular oluşturur.
    """
    goal_lower = goal.lower()
    
    # Kültür ve tarih turları için
    if any(keyword in goal_lower for keyword in ['roma', 'paris', 'istanbul', 'atina', 'mısır', 'viyana', 'vienna', 'prag', 'prague', 'kültür', 'tarih', 'müze', 'bazilika', 'saray']):
        return [
            {
                "question": "Seyahat tarzınız nasıl?",
                "options": [
                    "Yoğun program, çok yer görmek istiyorum",
                    "Orta tempoda, keyifli bir denge arıyorum",
                    "Rahat, az yer ama detaylı keşif",
                    "Esnek, anlık kararlarla ilerlemek"
                ]
            },
            {
                "question": "Hangi aktiviteleri tercih edersiniz?",
                "options": [
                    "Müzeler ve tarihi yerler",
                    "Yerel kültür ve gelenekler",
                    "Mimari ve sanat eserleri",
                    "Hepsi dengeli bir şekilde"
                ]
            },
            {
                "question": "Günlük bütçeniz nasıl?",
                "options": [
                    "Yüksek bütçe, lüks deneyimler",
                    "Orta bütçe, kaliteli ama ekonomik",
                    "Düşük bütçe, yerel deneyimler",
                    "Karışık, bazı günler lüks bazı günler ekonomik"
                ]
            },
            {
                "question": "Yemek konusunda tercihiniz nedir?",
                "options": [
                    "Yerel restoranlar ve geleneksel yemekler",
                    "Lüks restoranlar ve fine dining",
                    "Sokak yemekleri ve kafeler",
                    "Karışık, her türlü deneyim"
                ]
            },
            {
                "question": "Rehber tercihiniz nedir?",
                "options": [
                    "Profesyonel rehber eşliğinde",
                    "Sesli rehber ve uygulamalar",
                    "Kendi başıma keşfetmek",
                    "Yerel arkadaşlar ve tavsiyeler"
                ]
            }
        ]
    
    # Doğa ve macera turları için
    elif any(keyword in goal_lower for keyword in ['isviçre', 'norveç', 'yeni zelanda', 'doğa', 'trekking', 'hiking', 'dağ', 'orman', 'macera']):
        return [
            {
                "question": "Fiziksel aktivite seviyeniz nedir?",
                "options": [
                    "Çok aktif, zorlu parkurlar",
                    "Orta seviye, dengeli aktiviteler",
                    "Hafif, yürüyüş odaklı",
                    "Dinlenme ağırlıklı"
                ]
            },
            {
                "question": "Konaklama tercihiniz nedir?",
                "options": [
                    "Dağ evleri ve kulübeler",
                    "Kamp ve çadır",
                    "Rahat oteller",
                    "Karışık, deneyim çeşitliliği"
                ]
            },
            {
                "question": "Hangi doğa aktivitelerini tercih edersiniz?",
                "options": [
                    "Trekking ve dağ yürüyüşleri",
                    "Bisiklet ve su sporları",
                    "Fotoğrafçılık ve gözlem",
                    "Hepsi dengeli bir şekilde"
                ]
            },
            {
                "question": "İklim tercihiniz nedir?",
                "options": [
                    "Serin ve dağlık iklim",
                    "Ilıman ve ormanlık",
                    "Sıcak ve güneşli",
                    "Değişken, mevsimsel"
                ]
            },
            {
                "question": "Grup seyahati tercihiniz nedir?",
                "options": [
                    "Küçük grup turları",
                    "Bireysel seyahat",
                    "Aile/arkadaş grubu",
                    "Karışık, esnek"
                ]
            }
        ]
    
    # Şehir turları için
    elif any(keyword in goal_lower for keyword in ['new york', 'londra', 'tokyo', 'şehir', 'urban', 'metropol', 'alışveriş']):
        return [
            {
                "question": "Şehir deneyimi tercihiniz nedir?",
                "options": [
                    "Yoğun şehir hayatı ve gece hayatı",
                    "Kültür ve sanat odaklı",
                    "Alışveriş ve eğlence",
                    "Karışık, her türlü deneyim"
                ]
            },
            {
                "question": "Ulaşım tercihiniz nedir?",
                "options": [
                    "Toplu taşıma ve metro",
                    "Yürüyüş ve bisiklet",
                    "Taksi ve özel araç",
                    "Karışık, duruma göre"
                ]
            },
            {
                "question": "Konaklama bölgesi tercihiniz nedir?",
                "options": [
                    "Şehir merkezi, turistik bölge",
                    "Yerel mahalleler, otantik deneyim",
                    "İş bölgesi, modern",
                    "Karışık, farklı bölgeler"
                ]
            },
            {
                "question": "Günlük program yoğunluğu nasıl olsun?",
                "options": [
                    "Çok yoğun, sabah akşam aktivite",
                    "Orta yoğunluk, dinlenme araları",
                    "Rahat, az aktivite",
                    "Esnek, anlık kararlar"
                ]
            },
            {
                "question": "Hangi şehir aktivitelerini tercih edersiniz?",
                "options": [
                    "Müzeler ve galeriler",
                    "Alışveriş ve eğlence",
                    "Yerel restoranlar ve kafeler",
                    "Hepsi dengeli bir şekilde"
                ]
            }
        ]
    
    # Tatil ve dinlenme turları için
    elif any(keyword in goal_lower for keyword in ['bali', 'santorini', 'maldivler', 'tatil', 'dinlenme', 'plaj', 'resort', 'spa']):
        return [
            {
                "question": "Tatil tarzınız nedir?",
                "options": [
                    "Aktif tatil, spor ve aktiviteler",
                    "Dinlenme odaklı, spa ve masaj",
                    "Kültür ve doğa dengesi",
                    "Lüks ve konfor odaklı"
                ]
            },
            {
                "question": "Konaklama tercihiniz nedir?",
                "options": [
                    "Lüks resort ve oteller",
                    "Butik oteller ve pansiyonlar",
                    "Villa ve özel konaklama",
                    "Karışık, deneyim çeşitliliği"
                ]
            },
            {
                "question": "Günlük aktivite seviyeniz nedir?",
                "options": [
                    "Yoğun aktiviteler ve turlar",
                    "Orta seviye, dinlenme araları",
                    "Az aktivite, çok dinlenme",
                    "Esnek, anlık kararlar"
                ]
            },
            {
                "question": "Yemek deneyimi tercihiniz nedir?",
                "options": [
                    "Lüks restoranlar ve fine dining",
                    "Yerel restoranlar ve geleneksel",
                    "Otel yemekleri ve all-inclusive",
                    "Karışık, her türlü deneyim"
                ]
            },
            {
                "question": "Bütçe tercihiniz nedir?",
                "options": [
                    "Yüksek bütçe, lüks deneyimler",
                    "Orta bütçe, kaliteli ama ekonomik",
                    "Düşük bütçe, yerel deneyimler",
                    "Karışık, bazı günler lüks"
                ]
            }
        ]
    
    # Gastronomi turları için
    elif any(keyword in goal_lower for keyword in ['tokyo', 'italya', 'fransa', 'gastronomi', 'yemek', 'şarap', 'kahve', 'çikolata']):
        return [
            {
                "question": "Yemek deneyimi seviyeniz nedir?",
                "options": [
                    "Gurme, lüks restoranlar",
                    "Yerel lezzetler ve sokak yemekleri",
                    "Geleneksel ve otantik",
                    "Karışık, her türlü deneyim"
                ]
            },
            {
                "question": "Hangi mutfak türünü tercih edersiniz?",
                "options": [
                    "Fine dining ve Michelin yıldızlı",
                    "Yerel ve geleneksel",
                    "Sokak yemekleri ve kafeler",
                    "Hepsi dengeli bir şekilde"
                ]
            },
            {
                "question": "İçecek tercihiniz nedir?",
                "options": [
                    "Şarap ve kokteyl",
                    "Kahve ve çay",
                    "Yerel içecekler",
                    "Karışık, her türlü"
                ]
            },
            {
                "question": "Yemek aktiviteleri tercihiniz nedir?",
                "options": [
                    "Yemek turları ve workshop'lar",
                    "Pazar ziyaretleri ve alışveriş",
                    "Restoran deneyimleri",
                    "Karışık, her türlü aktivite"
                ]
            },
            {
                "question": "Bütçe tercihiniz nedir?",
                "options": [
                    "Yüksek bütçe, lüks deneyimler",
                    "Orta bütçe, kaliteli ama ekonomik",
                    "Düşük bütçe, yerel deneyimler",
                    "Karışık, bazı günler lüks"
                ]
            }
        ]
    
    # Genel seyahat hedefleri için varsayılan sorular
    else:
        return [
            {
                "question": "Seyahat tarzınız nedir?",
                "options": [
                    "Yoğun program, çok yer görmek",
                    "Orta tempoda, dengeli",
                    "Rahat, az yer ama detaylı",
                    "Esnek, anlık kararlar"
                ]
            },
            {
                "question": "Bütçe tercihiniz nedir?",
                "options": [
                    "Yüksek bütçe, lüks deneyimler",
                    "Orta bütçe, kaliteli ama ekonomik",
                    "Düşük bütçe, yerel deneyimler",
                    "Karışık, esnek bütçe"
                ]
            },
            {
                "question": "Konaklama tercihiniz nedir?",
                "options": [
                    "Lüks oteller ve resort'lar",
                    "Butik oteller ve pansiyonlar",
                    "Hostel ve ekonomik",
                    "Karışık, deneyim çeşitliliği"
                ]
            },
            {
                "question": "Aktivite yoğunluğu nasıl olsun?",
                "options": [
                    "Çok yoğun, sabah akşam aktivite",
                    "Orta yoğunluk, dinlenme araları",
                    "Az aktivite, çok dinlenme",
                    "Esnek, anlık kararlar"
                ]
            },
            {
                "question": "Rehber tercihiniz nedir?",
                "options": [
                    "Profesyonel rehber eşliğinde",
                    "Sesli rehber ve uygulamalar",
                    "Kendi başıma keşfetmek",
                    "Yerel tavsiyeler ve arkadaşlar"
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
    
    # Dinamik JSON template oluştur
    json_template = '{\n  "weekly_tasks": [\n'
    
    for i in range(days):
        json_template += f'''    {{
      "day": "{selected_days[i]}",
      "tasks": [
        "Spesifik seyahat aktivitesi 1 (sayısal değerlerle)",
        "Spesifik seyahat aktivitesi 2 (sayısal değerlerle)",
        "Spesifik seyahat aktivitesi 3 (sayısal değerlerle)"
      ]
    }}{"," if i < days - 1 else ""}\n'''
    
    json_template += '  ]\n}'
    
    prompt = f"""
Kullanıcının belirttiği seyahat hedefi: "{goal}"

Bu seyahat hedefini detaylı şekilde analiz et ve {days} günlük bir seyahat planı oluştur. Her gün için 3-4 adet ÇOK SPESİFİK, ÖLÇÜLEBİLİR ve YAPILABİLİR aktivite belirle.

ÖNEMLİ: Kullanıcının belirttiği şehir/ülke için plan yap. Başka bir yer için plan yapma!

Aktiviteler şu kriterlere uygun olmalı:
- SEYAHAT ODAKLI: Hedefle doğrudan ilgili ve spesifik seyahat aktiviteleri
- ÖLÇÜLEBİLİR: Sayısal değerler içermeli (örn: 2 saat, 1 saat, 30 dakika)
- GÜNLÜK: O gün tamamlanabilir
- SPESİFİK: Genel değil, net ve belirli yerler/aktivite isimleri
- MOTİVASYONEL: Unutulmaz deneyimler sunacak

ÖRNEKLER:
- Viyana kültür turu için: "Stephansdom Katedrali'ni ziyaret edin ve 1.5 saat boyunca gotik mimarisini inceleyin.", "Hofburg Sarayı'nda 2 saat geçirin ve İmparatorluk Apartmanları'nı gezin.", "Naschmarkt'ta 1 saat geçirin ve yerel lezzetleri tadın."
- Paris sanat turu için: "Louvre Müzesi'ni ziyaret edin ve 3 saat boyunca Mona Lisa ve diğer başyapıtları inceleyin.", "Eiffel Kulesi'ne çıkın ve 1 saat boyunca Paris manzarasını seyredin.", "Montmartre'da 2 saat geçirin ve Sacré-Cœur Bazilikası'nı ziyaret edin."
- Tokyo gastronomi turu için: "Tsukiji Dış Pazarı'nda 2 saat geçirin ve taze deniz ürünlerini keşfedin.", "Shibuya'da 1 saat geçirin ve meşhur kavşakta fotoğraf çekin.", "Akihabara'da 2 saat geçirin ve elektronik mağazalarını keşfedin."

Cevabın SADECE aşağıdaki formatta bir JSON objesi olmalıdır:
{json_template}

ÖNEMLİ: 
1. Her aktivite sayısal değerler içermeli ve çok spesifik olmalı. Genel aktiviteler verme!
2. Kullanıcının belirttiği şehir/ülke için plan yap. Başka bir yer için plan yapma!
3. Seyahat odaklı, yer isimleri ve sürelerle birlikte detaylı aktiviteler oluştur.
4. Tam olarak {days} günlük plan oluştur, fazla veya eksik gün olmasın!
5. GÜNLERİN SIRASINI DEĞİŞTİRME! Template'deki gün sırasını aynen kullan!
6. İlk gün: {selected_days[0]}, son gün: {selected_days[-1]} olacak şekilde plan yap!
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