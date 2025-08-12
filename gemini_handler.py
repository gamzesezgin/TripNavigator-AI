import streamlit as st
import json
import requests
import re

def generate_goal_specific_questions(goal, travel_style=None):
    """
    Seyahat hedefi ve tarzı bazında özelleştirilmiş sorular oluşturur.
    """
    goal_lower = goal.lower()
    
    # Eğer travel_style belirtilmişse, ona göre sorular oluştur
    if travel_style:
        if "doğa" in travel_style.lower() or "macera" in travel_style.lower():
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
        
        elif "tarih" in travel_style.lower() or "kültür" in travel_style.lower():
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
        
        elif "sanat" in travel_style.lower() or "gastronomi" in travel_style.lower():
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
        
        elif "alışveriş" in travel_style.lower() or "eğlence" in travel_style.lower():
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
        
        elif "tatil" in travel_style.lower() or "dinlenme" in travel_style.lower():
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
        
        elif "karışık" in travel_style.lower():
            return [
                {
                    "question": "Hangi aktivite türünü daha çok tercih edersiniz?",
                    "options": [
                        "Doğa ve macera",
                        "Kültür ve tarih",
                        "Sanat ve gastronomi",
                        "Alışveriş ve eğlence"
                    ]
                },
                {
                    "question": "Günlük program yoğunluğu nasıl olsun?",
                    "options": [
                        "Yoğun, çok aktivite",
                        "Orta yoğunluk, denge",
                        "Rahat, az aktivite",
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
                    "question": "Rehber tercihiniz nedir?",
                    "options": [
                        "Profesyonel rehber eşliğinde",
                        "Sesli rehber ve uygulamalar",
                        "Kendi başıma keşfetmek",
                        "Yerel tavsiyeler ve arkadaşlar"
                    ]
                }
            ]
    
    # Eğer travel_style belirtilmemişse, eski mantığı kullan
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
    return generate_goal_specific_questions("genel hedef", None)

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

def analyze_personality_from_answers(answers, goal):
    """
    Kullanıcının cevaplarına göre kişilik analizi yapar ve kişiselleştirilmiş öneriler verir.
    """
    if not answers or len(answers) < 3:
        return {
            "personality_type": "Çok Yönlü Seyahatçı",
            "description": "Farklı seyahat tarzlarını denemeye açık, esnek bir yaklaşımınız var.",
            "travel_style": "Esnek ve uyarlanabilir",
            "strengths": ["Çeşitliliğe açık", "Kolay uyum sağlar", "Yeni deneyimlere meraklı"],
            "tips": ["Farklı aktivite türlerini deneyin", "Esnek program yapın", "Anlık kararlarla ilerleyin"],
            "destination_recommendations": []
        }
    
    # Hedef bazında kişilik analizi
    goal_lower = goal.lower()
    
    # Kültür ve tarih turları için
    if any(keyword in goal_lower for keyword in ['roma', 'paris', 'istanbul', 'atina', 'mısır', 'viyana', 'vienna', 'prag', 'prague', 'kültür', 'tarih', 'müze', 'bazilika', 'saray']):
        return analyze_culture_travel_personality(answers, goal)
    
    # Doğa ve macera turları için
    elif any(keyword in goal_lower for keyword in ['isviçre', 'norveç', 'yeni zelanda', 'doğa', 'trekking', 'hiking', 'dağ', 'orman', 'macera']):
        return analyze_adventure_travel_personality(answers, goal)
    
    # Şehir turları için
    elif any(keyword in goal_lower for keyword in ['new york', 'londra', 'tokyo', 'şehir', 'urban', 'metropol', 'alışveriş']):
        return analyze_city_travel_personality(answers, goal)
    
    # Tatil ve dinlenme turları için
    elif any(keyword in goal_lower for keyword in ['bali', 'santorini', 'maldivler', 'tatil', 'dinlenme', 'plaj', 'resort', 'spa']):
        return analyze_relaxation_travel_personality(answers, goal)
    
    # Gastronomi turları için
    elif any(keyword in goal_lower for keyword in ['tokyo', 'italya', 'fransa', 'gastronomi', 'yemek', 'şarap', 'kahve', 'çikolata']):
        return analyze_food_travel_personality(answers, goal)
    
    # Genel seyahat hedefleri için
    else:
        return analyze_general_travel_personality(answers, goal)

def analyze_culture_travel_personality(answers, goal):
    """Kültür ve tarih turları için kişilik analizi"""
    
    # Seyahat tarzı analizi
    travel_style_score = 0
    if answers[0] == 0:  # Yoğun program
        travel_style_score += 2
        personality_type = "Kültür Avcısı"
        travel_style = "Yoğun ve kapsamlı kültür turu"
        strengths = ["Çok yer görme isteği", "Detaylı planlama", "Yüksek enerji"]
        tips = ["Erken başlayın", "Müze kartı alın", "Rehberli turları tercih edin"]
    elif answers[0] == 1:  # Orta tempo
        travel_style_score += 1
        personality_type = "Dengeli Kültür Sever"
        travel_style = "Dengeli ve keyifli kültür deneyimi"
        strengths = ["Denge kurma", "Keyifli deneyim", "Esnek yaklaşım"]
        tips = ["Günlük 2-3 ana aktivite", "Dinlenme araları verin", "Yerel kafelerde mola"]
    elif answers[0] == 2:  # Rahat
        travel_style_score += 0
        personality_type = "Sakin Kültür Keşifçisi"
        travel_style = "Sakin ve detaylı kültür keşfi"
        strengths = ["Detaylı inceleme", "Sakin yaklaşım", "Derinlemesine öğrenme"]
        tips = ["Günde 1-2 yer", "Uzun süre kalın", "Rehber kitaplar kullanın"]
    else:  # Esnek
        travel_style_score += 1
        personality_type = "Esnek Kültür Maceracısı"
        travel_style = "Esnek ve spontane kültür deneyimi"
        strengths = ["Uyum sağlama", "Spontane kararlar", "Yerel deneyimler"]
        tips = ["Esnek program yapın", "Yerel tavsiyeleri dinleyin", "Anlık kararlarla ilerleyin"]
    
    # Hedef bazında öneriler
    destination_recommendations = generate_culture_recommendations(goal, personality_type, answers)
    
    return {
        "personality_type": personality_type,
        "description": f"Kültür ve tarih odaklı seyahatlerde {travel_style.lower()} tarzını tercih ediyorsunuz.",
        "travel_style": travel_style,
        "strengths": strengths,
        "tips": tips,
        "destination_recommendations": destination_recommendations
    }

def analyze_adventure_travel_personality(answers, goal):
    """Doğa ve macera turları için kişilik analizi"""
    
    # Fiziksel aktivite seviyesi analizi
    if answers[0] == 0:  # Çok aktif
        personality_type = "Macera Avcısı"
        travel_style = "Zorlu ve aktif doğa macerası"
        strengths = ["Yüksek enerji", "Zorluklara meydan okuma", "Fiziksel dayanıklılık"]
        tips = ["Uygun ekipman alın", "Fiziksel hazırlık yapın", "Profesyonel rehber kullanın"]
    elif answers[0] == 1:  # Orta seviye
        personality_type = "Dengeli Maceracı"
        travel_style = "Dengeli doğa ve macera deneyimi"
        strengths = ["Denge kurma", "Çeşitli aktiviteler", "Güvenli yaklaşım"]
        tips = ["Karışık aktiviteler yapın", "Dinlenme günleri ekleyin", "Yerel rehberlerle çalışın"]
    elif answers[0] == 2:  # Hafif
        personality_type = "Sakin Doğa Sever"
        travel_style = "Sakin ve keyifli doğa deneyimi"
        strengths = ["Sakin yaklaşım", "Doğa gözlemi", "Keyifli aktiviteler"]
        tips = ["Kolay parkurlar seçin", "Fotoğraf çekin", "Piknik yapın"]
    else:  # Dinlenme
        personality_type = "Doğa Dinlenme Ustası"
        travel_style = "Doğada dinlenme ve huzur bulma"
        strengths = ["Huzur arama", "Doğa terapisi", "Sakin aktiviteler"]
        tips = ["Sessiz yerler seçin", "Meditasyon yapın", "Doğa seslerini dinleyin"]
    
    destination_recommendations = generate_adventure_recommendations(goal, personality_type, answers)
    
    return {
        "personality_type": personality_type,
        "description": f"Doğa ve macera odaklı seyahatlerde {travel_style.lower()} tarzını tercih ediyorsunuz.",
        "travel_style": travel_style,
        "strengths": strengths,
        "tips": tips,
        "destination_recommendations": destination_recommendations
    }

def analyze_city_travel_personality(answers, goal):
    """Şehir turları için kişilik analizi"""
    
    # Şehir deneyimi tercihi analizi
    if answers[0] == 0:  # Yoğun şehir hayatı
        personality_type = "Şehir Canavarı"
        travel_style = "Yoğun şehir hayatı ve gece hayatı"
        strengths = ["Yüksek enerji", "Şehir hayatına uyum", "Sosyal aktiviteler"]
        tips = ["Gece hayatını keşfedin", "Yoğun program yapın", "Yerel etkinliklere katılın"]
    elif answers[0] == 1:  # Kültür ve sanat
        personality_type = "Şehir Kültür Severi"
        travel_style = "Kültür ve sanat odaklı şehir deneyimi"
        strengths = ["Kültürel merak", "Sanat zevki", "Tarih bilgisi"]
        tips = ["Müzeleri ziyaret edin", "Sanat galerilerini keşfedin", "Tarihi yerleri inceleyin"]
    elif answers[0] == 2:  # Alışveriş ve eğlence
        personality_type = "Şehir Eğlence Severi"
        travel_style = "Alışveriş ve eğlence odaklı şehir deneyimi"
        strengths = ["Eğlence arama", "Alışveriş zevki", "Sosyal aktiviteler"]
        tips = ["Alışveriş merkezlerini ziyaret edin", "Eğlence mekanlarını keşfedin", "Yerel pazarları gezin"]
    else:  # Karışık
        personality_type = "Çok Yönlü Şehir Keşifçisi"
        travel_style = "Karışık şehir deneyimi"
        strengths = ["Çeşitliliğe açık", "Esnek yaklaşım", "Deneyim çeşitliliği"]
        tips = ["Farklı aktiviteleri deneyin", "Esnek program yapın", "Yerel tavsiyeleri dinleyin"]
    
    destination_recommendations = generate_city_recommendations(goal, personality_type, answers)
    
    return {
        "personality_type": personality_type,
        "description": f"Şehir odaklı seyahatlerde {travel_style.lower()} tarzını tercih ediyorsunuz.",
        "travel_style": travel_style,
        "strengths": strengths,
        "tips": tips,
        "destination_recommendations": destination_recommendations
    }

def analyze_relaxation_travel_personality(answers, goal):
    """Tatil ve dinlenme turları için kişilik analizi"""
    
    # Tatil tarzı analizi
    if answers[0] == 0:  # Aktif tatil
        personality_type = "Aktif Dinlenme Ustası"
        travel_style = "Aktif tatil ve spor aktiviteleri"
        strengths = ["Aktif dinlenme", "Spor sevgisi", "Enerji dolu yaklaşım"]
        tips = ["Spor aktiviteleri yapın", "Su sporlarını deneyin", "Yoga ve pilates"]
    elif answers[0] == 1:  # Dinlenme odaklı
        personality_type = "Huzur Arayan"
        travel_style = "Dinlenme odaklı spa ve masaj"
        strengths = ["Huzur arama", "Dinlenme ihtiyacı", "Sakin yaklaşım"]
        tips = ["Spa merkezlerini ziyaret edin", "Masaj yaptırın", "Sessiz yerler seçin"]
    elif answers[0] == 2:  # Kültür ve doğa dengesi
        personality_type = "Dengeli Tatilci"
        travel_style = "Kültür ve doğa dengesi"
        strengths = ["Denge kurma", "Çeşitli deneyimler", "Esnek yaklaşım"]
        tips = ["Kültür ve doğa aktivitelerini dengeleyin", "Dinlenme araları verin", "Yerel deneyimler yaşayın"]
    else:  # Lüks ve konfor
        personality_type = "Lüks Tatil Severi"
        travel_style = "Lüks ve konfor odaklı tatil"
        strengths = ["Lüks tercih", "Konfor arama", "Kaliteli deneyim"]
        tips = ["Lüks otelleri tercih edin", "VIP hizmetler alın", "Özel deneyimler yaşayın"]
    
    destination_recommendations = generate_relaxation_recommendations(goal, personality_type, answers)
    
    return {
        "personality_type": personality_type,
        "description": f"Tatil ve dinlenme odaklı seyahatlerde {travel_style.lower()} tarzını tercih ediyorsunuz.",
        "travel_style": travel_style,
        "strengths": strengths,
        "tips": tips,
        "destination_recommendations": destination_recommendations
    }

def analyze_food_travel_personality(answers, goal):
    """Gastronomi turları için kişilik analizi"""
    
    # Yemek deneyimi seviyesi analizi
    if answers[0] == 0:  # Gurme
        personality_type = "Gurme Seyahatçı"
        travel_style = "Lüks restoranlar ve fine dining"
        strengths = ["Gurme zevki", "Lüks deneyim", "Kaliteli yemek"]
        tips = ["Michelin yıldızlı restoranları ziyaret edin", "Şarap eşleştirmeleri yapın", "Özel yemek turlarına katılın"]
    elif answers[0] == 1:  # Yerel lezzetler
        personality_type = "Yerel Lezzet Keşifçisi"
        travel_style = "Yerel lezzetler ve sokak yemekleri"
        strengths = ["Yerel merak", "Sokak yemekleri", "Otantik deneyim"]
        tips = ["Sokak yemeklerini deneyin", "Yerel pazarları ziyaret edin", "Yerel restoranları tercih edin"]
    elif answers[0] == 2:  # Geleneksel
        personality_type = "Geleneksel Mutfak Severi"
        travel_style = "Geleneksel ve otantik mutfak"
        strengths = ["Geleneksel zevk", "Tarih bilgisi", "Kültürel merak"]
        tips = ["Geleneksel restoranları ziyaret edin", "Yemek tarihini öğrenin", "Aile restoranlarını tercih edin"]
    else:  # Karışık
        personality_type = "Çok Yönlü Yemek Severi"
        travel_style = "Karışık yemek deneyimi"
        strengths = ["Çeşitliliğe açık", "Esnek yaklaşım", "Deneyim çeşitliliği"]
        tips = ["Farklı yemek türlerini deneyin", "Esnek program yapın", "Yerel tavsiyeleri dinleyin"]
    
    destination_recommendations = generate_food_recommendations(goal, personality_type, answers)
    
    return {
        "personality_type": personality_type,
        "description": f"Gastronomi odaklı seyahatlerde {travel_style.lower()} tarzını tercih ediyorsunuz.",
        "travel_style": travel_style,
        "strengths": strengths,
        "tips": tips,
        "destination_recommendations": destination_recommendations
    }

def analyze_general_travel_personality(answers, goal):
    """Genel seyahat hedefleri için kişilik analizi"""
    
    # Seyahat tarzı analizi
    if answers[0] == 0:  # Yoğun program
        personality_type = "Yoğun Seyahatçı"
        travel_style = "Yoğun program ve çok yer görme"
        strengths = ["Yüksek enerji", "Çok yer görme", "Detaylı planlama"]
        tips = ["Erken başlayın", "Yoğun program yapın", "Ulaşım planlaması yapın"]
    elif answers[0] == 1:  # Orta tempoda
        personality_type = "Dengeli Seyahatçı"
        travel_style = "Orta tempoda ve dengeli seyahat"
        strengths = ["Denge kurma", "Keyifli deneyim", "Esnek yaklaşım"]
        tips = ["Günlük 2-3 aktivite", "Dinlenme araları verin", "Esnek program yapın"]
    elif answers[0] == 2:  # Rahat
        personality_type = "Sakin Seyahatçı"
        travel_style = "Rahat ve az yer ama detaylı keşif"
        strengths = ["Detaylı inceleme", "Sakin yaklaşım", "Derinlemesine öğrenme"]
        tips = ["Günde 1-2 yer", "Uzun süre kalın", "Detaylı inceleme yapın"]
    else:  # Esnek
        personality_type = "Esnek Seyahatçı"
        travel_style = "Esnek ve anlık kararlarla ilerleme"
        strengths = ["Uyum sağlama", "Spontane kararlar", "Esnek yaklaşım"]
        tips = ["Esnek program yapın", "Anlık kararlarla ilerleyin", "Yerel tavsiyeleri dinleyin"]
    
    destination_recommendations = generate_general_recommendations(goal, personality_type, answers)
    
    return {
        "personality_type": personality_type,
        "description": f"Genel seyahat hedeflerinde {travel_style.lower()} tarzını tercih ediyorsunuz.",
        "travel_style": travel_style,
        "strengths": strengths,
        "tips": tips,
        "destination_recommendations": destination_recommendations
    }

# Öneri üretme fonksiyonları
def generate_culture_recommendations(goal, personality_type, answers):
    """Kültür turları için öneriler üretir"""
    recommendations = []
    
    if "roma" in goal.lower():
        recommendations.extend([
            {
                "title": "Vatikan Müzeleri",
                "description": "Dünyanın en büyük sanat koleksiyonlarından biri",
                "why_suitable": f"{personality_type} için mükemmel - detaylı inceleme imkanı"
            },
            {
                "title": "Colosseum Gece Turu",
                "description": "Roma'nın simgesi olan amfitiyatroda özel deneyim",
                "why_suitable": f"{personality_type} için ideal - benzersiz ve unutulmaz"
            }
        ])
    
    elif "istanbul" in goal.lower():
        recommendations.extend([
            {
                "title": "Ayasofya",
                "description": "Bizans ve Osmanlı mimarisinin eşsiz örneği",
                "why_suitable": f"{personality_type} için mükemmel - tarihi ve mimari değer"
            },
            {
                "title": "Topkapı Sarayı",
                "description": "Osmanlı İmparatorluğu'nun yönetim merkezi",
                "why_suitable": f"{personality_type} için ideal - imparatorluk tarihi ve hazineler"
            },
            {
                "title": "Sultanahmet Camii",
                "description": "Mavi Camii olarak bilinen Osmanlı mimarisi şaheseri",
                "why_suitable": f"{personality_type} için mükemmel - İslam mimarisi ve sanatı"
            },
            {
                "title": "Kapalı Çarşı",
                "description": "Dünyanın en eski ve büyük kapalı çarşısı",
                "why_suitable": f"{personality_type} için ideal - geleneksel ticaret ve kültür"
            }
        ])
    
    elif "paris" in goal.lower():
        recommendations.extend([
            {
                "title": "Louvre Müzesi",
                "description": "Mona Lisa ve diğer başyapıtları keşfedin",
                "why_suitable": f"{personality_type} için mükemmel - dünyaca ünlü sanat eserleri"
            },
            {
                "title": "Notre-Dame Katedrali",
                "description": "Gotik mimarinin şaheseri",
                "why_suitable": f"{personality_type} için ideal - tarihi ve mimari değer"
            }
        ])
    
    elif "viyana" in goal.lower() or "vienna" in goal.lower():
        recommendations.extend([
            {
                "title": "Stephansdom Katedrali",
                "description": "Viyana'nın simgesi olan gotik katedral",
                "why_suitable": f"{personality_type} için mükemmel - tarihi ve mimari değer"
            },
            {
                "title": "Hofburg Sarayı",
                "description": "Habsburg İmparatorluğu'nun eski kraliyet sarayı",
                "why_suitable": f"{personality_type} için ideal - imparatorluk tarihi ve lüks"
            },
            {
                "title": "Schönbrunn Sarayı",
                "description": "UNESCO Dünya Mirası Listesi'ndeki barok saray",
                "why_suitable": f"{personality_type} için mükemmel - barok mimari ve bahçeler"
            },
            {
                "title": "Belvedere Sarayı",
                "description": "Klimt'in 'Öpücük' tablosunun bulunduğu sanat müzesi",
                "why_suitable": f"{personality_type} için ideal - sanat ve tarih birleşimi"
            }
        ])
    
    elif "prag" in goal.lower() or "prague" in goal.lower():
        recommendations.extend([
            {
                "title": "Prag Kalesi",
                "description": "Dünyanın en büyük antik kalesi",
                "why_suitable": f"{personality_type} için mükemmel - tarihi ve mimari değer"
            },
            {
                "title": "Charles Köprüsü",
                "description": "Gotik mimarinin şaheseri olan tarihi köprü",
                "why_suitable": f"{personality_type} için ideal - tarihi ve romantik atmosfer"
            },
            {
                "title": "Eski Şehir Meydanı",
                "description": "Astronomik saat ve gotik binalar",
                "why_suitable": f"{personality_type} için mükemmel - orta çağ atmosferi"
            }
        ])
    
    elif "atina" in goal.lower() or "athens" in goal.lower():
        recommendations.extend([
            {
                "title": "Akropolis",
                "description": "Antik Yunan uygarlığının en önemli anıtı",
                "why_suitable": f"{personality_type} için mükemmel - antik tarih ve arkeoloji"
            },
            {
                "title": "Parthenon",
                "description": "Athena'ya adanmış antik tapınak",
                "why_suitable": f"{personality_type} için ideal - klasik mimari ve mitoloji"
            },
            {
                "title": "Antik Agora",
                "description": "Antik Yunan'ın sosyal ve politik merkezi",
                "why_suitable": f"{personality_type} için mükemmel - antik toplum yapısı"
            }
        ])
    
    return recommendations

def generate_adventure_recommendations(goal, personality_type, answers):
    """Macera turları için öneriler üretir"""
    recommendations = []
    
    if "isviçre" in goal.lower():
        recommendations.extend([
            {
                "title": "Jungfraujoch",
                "description": "Avrupa'nın en yüksek tren istasyonu",
                "why_suitable": f"{personality_type} için mükemmel - benzersiz dağ deneyimi"
            },
            {
                "title": "Interlaken",
                "description": "Doğa sporları ve macera aktiviteleri",
                "why_suitable": f"{personality_type} için ideal - aktif ve macera dolu"
            }
        ])
    
    elif "norveç" in goal.lower() or "norway" in goal.lower():
        recommendations.extend([
            {
                "title": "Geirangerfjord",
                "description": "UNESCO Dünya Mirası Listesi'ndeki muhteşem fiyord",
                "why_suitable": f"{personality_type} için mükemmel - doğal güzellik ve macera"
            },
            {
                "title": "Trolltunga",
                "description": "Ünlü kaya çıkıntısı ve trekking rotası",
                "why_suitable": f"{personality_type} için ideal - zorlu doğa macerası"
            }
        ])
    
    elif "yeni zelanda" in goal.lower() or "new zealand" in goal.lower():
        recommendations.extend([
            {
                "title": "Milford Sound",
                "description": "Dünyanın en güzel fiyordlarından biri",
                "why_suitable": f"{personality_type} için mükemmel - doğal güzellik ve su sporları"
            },
            {
                "title": "Tongariro Alpine Crossing",
                "description": "Volkanik manzaralı ünlü trekking rotası",
                "why_suitable": f"{personality_type} için ideal - zorlu doğa macerası"
            }
        ])
    
    return recommendations

def generate_city_recommendations(goal, personality_type, answers):
    """Şehir turları için öneriler üretir"""
    recommendations = []
    
    if "new york" in goal.lower():
        recommendations.extend([
            {
                "title": "Times Square",
                "description": "Şehrin kalbi ve enerjisi",
                "why_suitable": f"{personality_type} için mükemmel - yoğun şehir hayatı"
            },
            {
                "title": "Central Park",
                "description": "Şehirde doğa ve dinlenme",
                "why_suitable": f"{personality_type} için ideal - şehir ve doğa dengesi"
            }
        ])
    
    elif "londra" in goal.lower() or "london" in goal.lower():
        recommendations.extend([
            {
                "title": "Big Ben ve Westminster",
                "description": "İngiltere'nin simgesi olan saat kulesi",
                "why_suitable": f"{personality_type} için mükemmel - tarihi ve politik önem"
            },
            {
                "title": "British Museum",
                "description": "Dünyanın en büyük müzelerinden biri",
                "why_suitable": f"{personality_type} için ideal - kültür ve tarih"
            }
        ])
    
    elif "tokyo" in goal.lower():
        recommendations.extend([
            {
                "title": "Shibuya Crossing",
                "description": "Dünyanın en yoğun yaya geçidi",
                "why_suitable": f"{personality_type} için mükemmel - modern şehir hayatı"
            },
            {
                "title": "Senso-ji Tapınağı",
                "description": "Tokyo'nun en eski Budist tapınağı",
                "why_suitable": f"{personality_type} için ideal - geleneksel kültür"
            }
        ])
    
    return recommendations

def generate_relaxation_recommendations(goal, personality_type, answers):
    """Tatil turları için öneriler üretir"""
    recommendations = []
    
    if "bali" in goal.lower():
        recommendations.extend([
            {
                "title": "Ubud Spa Merkezleri",
                "description": "Geleneksel Bali masajları ve spa tedavileri",
                "why_suitable": f"{personality_type} için mükemmel - huzur ve dinlenme"
            },
            {
                "title": "Nusa Penida Adası",
                "description": "Sakin plajlar ve doğal güzellikler",
                "why_suitable": f"{personality_type} için ideal - sakin ve huzurlu ortam"
            }
        ])
    
    elif "santorini" in goal.lower():
        recommendations.extend([
            {
                "title": "Oia Köyü",
                "description": "Gün batımının en güzel izlendiği yer",
                "why_suitable": f"{personality_type} için mükemmel - romantik atmosfer"
            },
            {
                "title": "Fira Şehri",
                "description": "Adanın başkenti ve kaldera manzarası",
                "why_suitable": f"{personality_type} için ideal - şehir ve doğa dengesi"
            }
        ])
    
    elif "maldivler" in goal.lower() or "maldives" in goal.lower():
        recommendations.extend([
            {
                "title": "Su Üstü Villaları",
                "description": "Kristal berraklığında denizde konaklama",
                "why_suitable": f"{personality_type} için mükemmel - lüks ve huzur"
            },
            {
                "title": "Dalış Noktaları",
                "description": "Renkli mercan resifleri ve tropik balıklar",
                "why_suitable": f"{personality_type} için ideal - su altı macerası"
            }
        ])
    
    return recommendations

def generate_food_recommendations(goal, personality_type, answers):
    """Gastronomi turları için öneriler üretir"""
    recommendations = []
    
    if "tokyo" in goal.lower():
        recommendations.extend([
            {
                "title": "Tsukiji Dış Pazarı",
                "description": "Dünyanın en büyük balık pazarı",
                "why_suitable": f"{personality_type} için mükemmel - taze deniz ürünleri"
            },
            {
                "title": "Ginza Restoranları",
                "description": "Lüks Japon restoranları ve fine dining",
                "why_suitable": f"{personality_type} için ideal - yüksek kaliteli yemek deneyimi"
            }
        ])
    
    elif "italya" in goal.lower() or "italy" in goal.lower():
        recommendations.extend([
            {
                "title": "Toskana Şarap Turları",
                "description": "Chianti ve Brunello şaraplarının anavatanı",
                "why_suitable": f"{personality_type} için mükemmel - şarap kültürü"
            },
            {
                "title": "Napoli Pizza Deneyimi",
                "description": "Pizzanın doğduğu yer, geleneksel tarifler",
                "why_suitable": f"{personality_type} için ideal - otantik pizza kültürü"
            }
        ])
    
    elif "fransa" in goal.lower() or "france" in goal.lower():
        recommendations.extend([
            {
                "title": "Bordeaux Şarap Bölgesi",
                "description": "Dünyaca ünlü şarap üretim merkezi",
                "why_suitable": f"{personality_type} için mükemmel - şarap kültürü"
            },
            {
                "title": "Paris Pastane Turları",
                "description": "Macaron ve croissant'ların anavatanı",
                "why_suitable": f"{personality_type} için ideal - Fransız pastacılığı"
            }
        ])
    
    return recommendations

def generate_general_recommendations(goal, personality_type, answers):
    """Genel seyahat hedefleri için öneriler üretir"""
    return [
        {
            "title": "Yerel Rehber Bulun",
            "description": "Hedefinizdeki yerel rehberlerle çalışın",
            "why_suitable": f"{personality_type} için mükemmel - kişiselleştirilmiş deneyim"
        },
        {
            "title": "Yerel Kültürü Keşfedin",
            "description": "Geleneksel aktivitelere ve festivallere katılın",
            "why_suitable": f"{personality_type} için ideal - otantik deneyim"
        }
    ]

# AI Destinasyon Önerisi Fonksiyonları
def generate_ai_destination_recommendation(answers, api_key):
    """
    Kullanıcı cevaplarına göre AI'dan 3 destinasyon önerisi alır
    """
    # AI öneri soruları tanımları
    ai_questions = [
        {
            "id": "climate",
            "question": "🌡️ İklim tercihiniz nedir?",
            "options": ["Sıcak ve güneşli", "Serin ve dağlık", "Ilıman ve ormanlık", "Fark etmez"],
            "category": "climate"
        },
        {
            "id": "budget",
            "question": "💰 Bütçe seviyeniz nedir?",
            "options": ["Düşük bütçe", "Orta bütçe", "Yüksek bütçe", "Karışık"],
            "category": "budget"
        },
        {
            "id": "activity",
            "question": "🎯 Hangi aktivite tarzını tercih edersiniz?",
            "options": ["Doğa ve macera", "Tarih ve kültür", "Sanat ve gastronomi", "Alışveriş ve eğlence", "Karışık"],
            "category": "activity"
        },
        {
            "id": "duration",
            "question": "📅 Seyahat süreniz ne kadar olsun?",
            "options": ["3 gün", "5 gün", "7+ gün", "Fark etmez"],
            "category": "duration"
        },
        {
            "id": "distance",
            "question": "🌍 Kıta veya mesafe tercihiniz nedir?",
            "options": ["Yakın (Avrupa/Türkiye)", "Uzak (Asya/Amerika)", "Fark etmez"],
            "category": "distance"
        },
        {
            "id": "cuisine",
            "question": "🍽️ Yerel mutfak deneyimi ister misiniz?",
            "options": ["Evet, çok önemli", "Hayır, önemsiz", "Karışık"],
            "category": "cuisine"
        },
        {
            "id": "atmosphere",
            "question": "🎭 Hangi ortamı tercih edersiniz?",
            "options": ["Canlı ve kalabalık", "Sakin ve huzurlu", "Karışık"],
            "category": "atmosphere"
        },
        {
            "id": "language",
            "question": "🗣️ Dil konusunda tercihiniz nedir?",
            "options": ["İngilizce konuşulan yerler", "Farklı dillerin konuşulduğu yerler", "Fark etmez"],
            "category": "language"
        },
        {
            "id": "transport",
            "question": "✈️ Ulaşım tercihiniz nedir?",
            "options": ["Uçakla uzun yolculuk sorun değil", "Kısa mesafeler tercih", "Fark etmez"],
            "category": "transport"
        },
        {
            "id": "interests",
            "question": "🎨 Özel ilgi alanlarınız nelerdir?",
            "options": ["Festival ve etkinlikler", "Müzik ve sanat", "Kış sporları", "Dalış ve su sporları", "Trekking ve doğa", "Fotoğrafçılık", "Hepsi"],
            "category": "interests"
        }
    ]
    
    # Cevapları analiz et ve prompt oluştur
    prompt = f"""
Kullanıcının seyahat tercihleri şu şekilde:

İklim: {ai_questions[0]['options'][answers.get('climate', 0)]}
Bütçe: {ai_questions[1]['options'][answers.get('budget', 0)]}
Aktivite: {ai_questions[2]['options'][answers.get('activity', 0)]}
Süre: {ai_questions[3]['options'][answers.get('duration', 0)]}
Mesafe: {ai_questions[4]['options'][answers.get('distance', 0)]}
Mutfak: {ai_questions[5]['options'][answers.get('cuisine', 0)]}
Atmosfer: {ai_questions[6]['options'][answers.get('atmosphere', 0)]}
Dil: {ai_questions[7]['options'][answers.get('language', 0)]}
Ulaşım: {ai_questions[8]['options'][answers.get('transport', 0)]}
İlgi Alanları: {ai_questions[9]['options'][answers.get('interests', 0)]}

Bu tercihlere göre dünyadaki en uygun 3 destinasyon öner. 

ÖNEMLİ: Her destinasyon için kısa bir açıklama da ekle.
Örnek format:
1. Şehir Adı, Ülke Adı - Kısa açıklama
2. Şehir Adı, Ülke Adı - Kısa açıklama  
3. Şehir Adı, Ülke Adı - Kısa açıklama

Sadece bu formatta yanıt ver, başka hiçbir şey yazma.
"""
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    payload = {
      "contents": [{"parts": [{"text": prompt}]}],
      "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 300,
      }
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        import requests
        response = requests.post(api_url, headers=headers, data=requests.compat.json.dumps(payload), timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # Debug için AI yanıtını göster
            print(f"AI Yanıtı: {content}")
            
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
                    clean_line = line.replace('1.', '').replace('2.', '').replace('3.', '').strip()
                    
                    # Tire ile ayrılmış formatı kontrol et
                    if ' - ' in clean_line:
                        parts = clean_line.split(' - ', 1)
                        destination = parts[0].strip()
                        description = parts[1].strip() if len(parts) > 1 else ""
                        
                        if len(destination) > 3:  # En az 3 karakter olmalı
                            destinations.append({
                                "name": destination,
                                "description": description
                            })
                            print(f"Bulunan destinasyon: {destination} - {description}")
                
                # Numarasız satırları da kontrol et
                elif ' - ' in line and len(line) > 3:
                    parts = line.split(' - ', 1)
                    destination = parts[0].strip()
                    description = parts[1].strip() if len(parts) > 1 else ""
                    
                    if len(destination) > 3:
                        destinations.append({
                            "name": destination,
                            "description": description
                        })
                        print(f"Numarasız destinasyon bulundu: {destination} - {description}")
            
            # Eğer 3 destinasyon bulunduysa döndür
            if len(destinations) >= 3:
                return destinations[:3]  # İlk 3'ünü al
            
            # Eğer 1-2 destinasyon bulunduysa, fallback ile tamamla
            elif len(destinations) > 0:
                fallback_destinations = generate_fallback_destinations(answers, ai_questions, destinations)
                return fallback_destinations[:3]
            
            # Hiçbir destinasyon bulunamazsa, tamamen fallback kullan
            else:
                print("AI yanıtından destinasyon bulunamadı, fallback kullanılıyor...")
                fallback_destinations = generate_fallback_destinations(answers, ai_questions, [])
                return fallback_destinations[:3]
            
        else:
            print("API yanıtında candidates bulunamadı")
            fallback_destinations = generate_fallback_destinations(answers, ai_questions, [])
            return fallback_destinations[:3]
            
    except Exception as e:
        print(f"AI önerisi alınırken hata: {e}")
        fallback_destinations = generate_fallback_destinations(answers, ai_questions, [])
        return fallback_destinations[:3]

def generate_fallback_destinations(answers, ai_questions, existing_destinations):
    """
    AI yanıtı alınamadığında kullanıcı tercihlerine göre 3 destinasyon önerir
    """
    climate = ai_questions[0]['options'][answers.get('climate', 0)]
    activity = ai_questions[2]['options'][answers.get('activity', 0)]
    distance = ai_questions[4]['options'][answers.get('distance', 0)]
    budget = ai_questions[1]['options'][answers.get('budget', 0)]
    
    destinations = []
    
    # Mevcut destinasyonları ekle
    for dest in existing_destinations:
        destinations.append(dest)
    
    # İklim tercihine göre öneriler
    if "sıcak" in climate.lower():
        if "yakın" in distance.lower():
            if not any("Antalya" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Antalya, Türkiye",
                    "description": "Sıcak iklim, tarihi ve doğal güzellikler, ekonomik seyahat"
                })
            if not any("Barselona" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Barselona, İspanya",
                    "description": "Sıcak iklim, kültür, sanat ve gastronomi"
                })
        else:
            if not any("Bangkok" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Bangkok, Tayland",
                    "description": "Sıcak iklim, egzotik kültür, uygun fiyatlar"
                })
            if not any("Bali" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Bali, Endonezya",
                    "description": "Sıcak iklim, doğa, spa ve huzur"
                })
    
    elif "serin" in climate.lower():
        if "yakın" in distance.lower():
            if not any("İsviçre" in d["name"] for d in destinations):
                destinations.append({
                    "name": "İsviçre Alpleri, İsviçre",
                    "description": "Serin iklim, doğa sporları, lüks deneyim"
                })
            if not any("Norveç" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Bergen, Norveç",
                    "description": "Serin iklim, fiyordlar, doğa macerası"
                })
        else:
            if not any("Banff" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Banff, Kanada",
                    "description": "Serin iklim, dağ manzaraları, doğa aktiviteleri"
                })
            if not any("Yeni Zelanda" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Queenstown, Yeni Zelanda",
                    "description": "Serin iklim, macera sporları, doğal güzellikler"
                })
    
    # Aktivite tercihine göre öneriler
    if "doğa" in activity.lower() or "macera" in activity.lower():
        if "yakın" in distance.lower():
            if not any("İsviçre" in d["name"] for d in destinations):
                destinations.append({
                    "name": "İsviçre Alpleri, İsviçre",
                    "description": "Doğa sporları, trekking, dağ aktiviteleri"
                })
        else:
            if not any("Yeni Zelanda" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Queenstown, Yeni Zelanda",
                    "description": "Macera sporları, doğa aktiviteleri, ekstrem sporlar"
                })
    
    elif "tarih" in activity.lower() or "kültür" in activity.lower():
        if "yakın" in distance.lower():
            if not any("Roma" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Roma, İtalya",
                    "description": "Tarihi ve kültürel miras, antik uygarlık"
                })
        else:
            if not any("Kyoto" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Kyoto, Japonya",
                    "description": "Geleneksel kültür, tapınaklar, tarihi atmosfer"
                })
    
    elif "sanat" in activity.lower() or "gastronomi" in activity.lower():
        if "yakın" in distance.lower():
            if not any("Paris" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Paris, Fransa",
                    "description": "Sanat, gastronomi, lüks deneyim"
                })
        else:
            if not any("Tokyo" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Tokyo, Japonya",
                    "description": "Modern sanat, geleneksel mutfak, kültür"
                })
    
    # Bütçe tercihine göre öneriler
    if "düşük" in budget.lower():
        if not any("Türkiye" in d["name"] for d in destinations):
            destinations.append({
                "name": "İstanbul, Türkiye",
                "description": "Ekonomik seyahat, tarih, kültür ve lezzetli mutfak"
            })
    
    # Eğer hala 3'ten azsa, genel öneriler ekle
    while len(destinations) < 3:
        if "yakın" in distance.lower():
            if not any("Prag" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Prag, Çek Cumhuriyeti",
                    "description": "Orta çağ atmosferi, uygun fiyatlar, güzel mimari"
                })
            elif not any("Budapeşte" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Budapeşte, Macaristan",
                    "description": "Tarihi şehir, termal banyolar, ekonomik seyahat"
                })
        else:
            if not any("Singapur" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Singapur",
                    "description": "Modern şehir, kültür karışımı, temizlik"
                })
            elif not any("Melbourne" in d["name"] for d in destinations):
                destinations.append({
                    "name": "Melbourne, Avustralya",
                    "description": "Kültür şehri, sanat, gastronomi ve doğa"
                })
    
    return destinations[:3]

def generate_recommendation_reasoning(answers, destination):
    """
    Kullanıcı cevaplarına göre öneri gerekçesi oluşturur
    """
    # AI öneri soruları tanımları
    ai_questions = [
        {
            "id": "climate",
            "question": "🌡️ İklim tercihiniz nedir?",
            "options": ["Sıcak ve güneşli", "Serin ve dağlık", "Ilıman ve ormanlık", "Fark etmez"],
            "category": "climate"
        },
        {
            "id": "budget",
            "question": "💰 Bütçe seviyeniz nedir?",
            "options": ["Düşük bütçe", "Orta bütçe", "Yüksek bütçe", "Karışık"],
            "category": "budget"
        },
        {
            "id": "activity",
            "question": "🎯 Hangi aktivite tarzını tercih edersiniz?",
            "options": ["Doğa ve macera", "Tarih ve kültür", "Sanat ve gastronomi", "Alışveriş ve eğlence", "Karışık"],
            "category": "activity"
        },
        {
            "id": "duration",
            "question": "📅 Seyahat süreniz ne kadar olsun?",
            "options": ["3 gün", "5 gün", "7+ gün", "Fark etmez"],
            "category": "duration"
        },
        {
            "id": "distance",
            "question": "🌍 Kıta veya mesafe tercihiniz nedir?",
            "options": ["Yakın (Avrupa/Türkiye)", "Uzak (Asya/Amerika)", "Fark etmez"],
            "category": "distance"
        },
        {
            "id": "cuisine",
            "question": "🍽️ Yerel mutfak deneyimi ister misiniz?",
            "options": ["Evet, çok önemli", "Hayır, önemsiz", "Karışık"],
            "category": "cuisine"
        },
        {
            "id": "atmosphere",
            "question": "🎭 Hangi ortamı tercih edersiniz?",
            "options": ["Canlı ve kalabalık", "Sakin ve huzurlu", "Karışık"],
            "category": "atmosphere"
        },
        {
            "id": "language",
            "question": "🗣️ Dil konusunda tercihiniz nedir?",
            "options": ["İngilizce konuşulan yerler", "Farklı dillerin konuşulduğu yerler", "Fark etmez"],
            "category": "language"
        },
        {
            "id": "transport",
            "question": "✈️ Ulaşım tercihiniz nedir?",
            "options": ["Uçakla uzun yolculuk sorun değil", "Kısa mesafeler tercih", "Fark etmez"],
            "category": "transport"
        },
        {
            "id": "interests",
            "question": "🎨 Özel ilgi alanlarınız nelerdir?",
            "options": ["Festival ve etkinlikler", "Müzik ve sanat", "Kış sporları", "Dalış ve su sporları", "Trekking ve doğa", "Fotoğrafçılık", "Hepsi"],
            "category": "interests"
        }
    ]
    
    reasoning = f"**{destination}** size önerilmesinin nedenleri:\n\n"
    
    # İklim tercihi
    climate = ai_questions[0]['options'][answers.get('climate', 0)]
    if "sıcak" in climate.lower():
        reasoning += "🌡️ **Sıcak iklim tercihiniz** - Bu destinasyon yıl boyunca sıcak ve güneşli hava sunar.\n"
    elif "serin" in climate.lower():
        reasoning += "🌡️ **Serin iklim tercihiniz** - Bu destinasyon dağlık ve serin hava koşullarına sahiptir.\n"
    
    # Bütçe
    budget = ai_questions[1]['options'][answers.get('budget', 0)]
    if "düşük" in budget.lower():
        reasoning += "💰 **Düşük bütçe tercihiniz** - Bu destinasyon ekonomik seyahat seçenekleri sunar.\n"
    elif "yüksek" in budget.lower():
        reasoning += "💰 **Yüksek bütçe tercihiniz** - Bu destinasyon lüks ve premium deneyimler sunar.\n"
    
    # Aktivite
    activity = ai_questions[2]['options'][answers.get('activity', 0)]
    if "doğa" in activity.lower():
        reasoning += "🌿 **Doğa ve macera tercihiniz** - Bu destinasyon zengin doğal güzellikler ve macera aktiviteleri sunar.\n"
    elif "tarih" in activity.lower():
        reasoning += "🏛️ **Tarih ve kültür tercihiniz** - Bu destinasyon zengin tarihi ve kültürel mirasa sahiptir.\n"
    elif "sanat" in activity.lower():
        reasoning += "🎨 **Sanat ve gastronomi tercihiniz** - Bu destinasyon dünya çapında ünlü sanat eserleri ve lezzetli mutfak sunar.\n"
    
    # Mesafe
    distance = ai_questions[4]['options'][answers.get('distance', 0)]
    if "yakın" in distance.lower():
        reasoning += "🌍 **Yakın mesafe tercihiniz** - Bu destinasyon Türkiye'ye yakın ve kolay ulaşılabilir.\n"
    elif "uzak" in distance.lower():
        reasoning += "🌍 **Uzak mesafe tercihiniz** - Bu destinasyon benzersiz ve farklı kültür deneyimi sunar.\n"
    
    reasoning += "\nBu destinasyon, belirttiğiniz tüm tercihleri en iyi şekilde karşılayacak ve unutulmaz bir seyahat deneyimi yaşatacaktır."
    
    return reasoning

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