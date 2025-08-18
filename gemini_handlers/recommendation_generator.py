"""
Öneri Üretme Modülü
Kişilik analizine göre özelleştirilmiş öneriler oluşturur
"""

def generate_culture_recommendations(personality_type):
    """
    Kültür seyahati için öneriler
    """
    if "Lüks" in personality_type:
        return [
            "Özel rehber eşliğinde VIP müze turları",
            "Lüks restoranlarda geleneksel yemek deneyimi",
            "Özel araçla tarihi şehir turu",
            "Butik otellerde konaklama",
            "Özel sanat galerisi ziyaretleri"
        ]
    elif "Yerel" in personality_type:
        return [
            "Yerel rehberle otantik mahalle turları",
            "Geleneksel pazarlarda alışveriş",
            "Yerel ailelerle yemek deneyimi",
            "Küçük pansiyonlarda konaklama",
            "Yerel festivallere katılım"
        ]
    else:
        return [
            "Müze ve tarihi yerler ziyareti",
            "Kültür turları ve rehberli geziler",
            "Geleneksel restoranlarda yemek",
            "Tarihi otellerde konaklama",
            "Sanat galerileri ve sergiler"
        ]

def generate_adventure_recommendations(personality_type):
    """
    Macera seyahati için öneriler
    """
    if "Macera" in personality_type:
        return [
            "Zorlu trekking parkurları",
            "Kamp ve çadır deneyimi",
            "Tırmanış ve dağ sporları",
            "Vahşi doğa turları",
            "Macera sporları (rafting, zipline)"
        ]
    elif "Doğa" in personality_type:
        return [
            "Doğa fotoğrafçılığı turları",
            "Kuş gözlemciliği",
            "Botanik bahçe ziyaretleri",
            "Doğa yürüyüşleri",
            "Vahşi yaşam gözlem turları"
        ]
    elif "Spor" in personality_type:
        return [
            "Bisiklet turları",
            "Su sporları aktiviteleri",
            "Kayak ve kış sporları",
            "Yoga ve pilates kampları",
            "Fitness ve spor turları"
        ]
    else:
        return [
            "Orta seviye trekking",
            "Doğa yürüyüşleri",
            "Bisiklet turları",
            "Su sporları",
            "Doğa fotoğrafçılığı"
        ]

def generate_city_recommendations(personality_type):
    """
    Şehir seyahati için öneriler
    """
    if "Metropol" in personality_type:
        return [
            "Yoğun şehir turları",
            "Gece hayatı ve eğlence",
            "Metro ve toplu taşıma deneyimi",
            "Şehir merkezi konaklama",
            "Modern restoranlar ve kafeler"
        ]
    elif "Kültür" in personality_type:
        return [
            "Müzeler ve galeriler",
            "Tarihi mahalleler",
            "Sanat sergileri",
            "Kültür merkezleri",
            "Tarihi restoranlar"
        ]
    elif "Eğlence" in personality_type:
        return [
            "Alışveriş merkezleri",
            "Eğlence parkları",
            "Kafeler ve barlar",
            "Spor etkinlikleri",
            "Konser ve tiyatro"
        ]
    else:
        return [
            "Şehir turları",
            "Müze ziyaretleri",
            "Alışveriş",
            "Yerel restoranlar",
            "Park ve bahçeler"
        ]

def generate_relaxation_recommendations(personality_type):
    """
    Dinlenme seyahati için öneriler
    """
    if "Lüks" in personality_type:
        return [
            "Lüks resort ve spa",
            "Özel villa kiralama",
            "Fine dining restoranlar",
            "Özel plaj kulübeleri",
            "VIP transfer hizmetleri"
        ]
    elif "Doğa" in personality_type:
        return [
            "Doğa resort'ları",
            "Orman evleri",
            "Doğa yürüyüşleri",
            "Meditasyon kampları",
            "Ekoturizm deneyimleri"
        ]
    elif "Spa" in personality_type:
        return [
            "Spa ve wellness merkezleri",
            "Masaj ve terapi",
            "Yoga ve pilates",
            "Detoks programları",
            "Termal kaplıcalar"
        ]
    else:
        return [
            "Rahat oteller",
            "Plaj aktiviteleri",
            "Hafif yürüyüşler",
            "Yerel restoranlar",
            "Dinlenme aktiviteleri"
        ]

def generate_food_recommendations(personality_type):
    """
    Gastronomi seyahati için öneriler
    """
    if "Gurme" in personality_type:
        return [
            "Michelin yıldızlı restoranlar",
            "Şef masası deneyimleri",
            "Özel yemek turları",
            "Şarap tadım etkinlikleri",
            "Gurme market alışverişi"
        ]
    elif "Yerel Lezzet" in personality_type:
        return [
            "Geleneksel restoranlar",
            "Yerel pazar ziyaretleri",
            "Aile restoranları",
            "Geleneksel yemek kursları",
            "Yerel içecek tadımları"
        ]
    elif "Sokak Lezzeti" in personality_type:
        return [
            "Sokak yemekleri turları",
            "Yerel kafeler",
            "Pazar yemekleri",
            "Food truck deneyimleri",
            "Yerel tatlı dükkanları"
        ]
    else:
        return [
            "Yerel restoranlar",
            "Pazar ziyaretleri",
            "Yemek turları",
            "Kafeler",
            "Geleneksel lezzetler"
        ]

def generate_general_recommendations(personality_type):
    """
    Genel seyahat için öneriler
    """
    if "Aktif" in personality_type:
        return [
            "Yoğun aktivite programları",
            "Spor ve fitness aktiviteleri",
            "Macera turları",
            "Şehir keşif turları",
            "Kültür ve sanat aktiviteleri"
        ]
    elif "Dengeli" in personality_type:
        return [
            "Dengeli aktivite programları",
            "Kültür ve eğlence karışımı",
            "Doğa ve şehir deneyimleri",
            "Yerel ve turistik aktiviteler",
            "Dinlenme ve aktivite dengesi"
        ]
    elif "Rahat" in personality_type:
        return [
            "Hafif aktivite programları",
            "Dinlenme odaklı turlar",
            "Rahat konaklama seçenekleri",
            "Yerel deneyimler",
            "Esnek program seçenekleri"
        ]
    elif "Lüks" in personality_type:
        return [
            "Lüks konaklama seçenekleri",
            "VIP turlar ve hizmetler",
            "Fine dining deneyimleri",
            "Özel transfer hizmetleri",
            "Premium aktivite seçenekleri"
        ]
    else:
        return [
            "Genel turistik aktiviteler",
            "Popüler destinasyonlar",
            "Standart konaklama",
            "Yerel restoranlar",
            "Kültür ve eğlence karışımı"
        ]
