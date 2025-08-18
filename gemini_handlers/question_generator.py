"""
Soru Üretme Modülü
Seyahat hedeflerine göre özelleştirilmiş sorular oluşturur
"""

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
