"""
Kişilik Analizi Modülü
Kullanıcı cevaplarına göre seyahat kişiliği analizi yapar
"""

def analyze_learning_style(answers):
    """
    Kullanıcının öğrenme stilini analiz eder
    """
    if not answers or len(answers) < 5:
        return "Dengeli"
    
    # Basit analiz - çoğunluk hangi seçenekte
    option_counts = {}
    
    for answer in answers:
        if answer in option_counts:
            option_counts[answer] += 1
        else:
            option_counts[answer] = 1
    
    # En çok seçilen seçeneği bul
    most_common = max(option_counts, key=option_counts.get)
    
    # Seçeneklere göre stil belirleme
    if "yoğun" in most_common.lower() or "aktif" in most_common.lower():
        return "Aktif"
    elif "orta" in most_common.lower() or "dengeli" in most_common.lower():
        return "Dengeli"
    elif "rahat" in most_common.lower() or "az" in most_common.lower():
        return "Rahat"
    else:
        return "Esnek"

def analyze_personality_from_answers(answers, user_goal):
    """
    Kullanıcı cevaplarına göre seyahat kişiliğini analiz eder
    """
    if not answers:
        return {
            "personality_type": "Test Sonucu Belirlenemedi",
            "description": "Test sonuçlarınıza göre kişilik profiliniz belirlenemedi. Genel seyahat tercihleriniz dikkate alınacak.",
            "travel_style": "Genel seyahat tercihleri"
        }
    
    # Her cevap için analiz yap
    personality_traits = []
    
    # Seyahat tarzına göre analiz
    user_goal_lower = user_goal.lower()
    
    # Cevap index'lerini analiz et (0, 1, 2, 3 gibi)
    for answer_index in answers:
        if answer_index == 0:  # İlk seçenek genellikle aktif/yoğun
            personality_traits.append("Aktif")
        elif answer_index == 1:  # İkinci seçenek genellikle orta/dengeli
            personality_traits.append("Dengeli")
        elif answer_index == 2:  # Üçüncü seçenek genellikle rahat/az
            personality_traits.append("Rahat")
        elif answer_index == 3:  # Dördüncü seçenek genellikle esnek/karışık
            personality_traits.append("Esnek")
        

    
    # En çok tekrar eden özelliği bul
    if personality_traits:
        from collections import Counter
        trait_counts = Counter(personality_traits)
        dominant_trait = trait_counts.most_common(1)[0][0]
        
        # Seyahat tarzına göre kişilik türünü belirle
        if "doğa" in user_goal_lower or "macera" in user_goal_lower or "isviçre" in user_goal_lower or "norveç" in user_goal_lower:
            if dominant_trait in ["Aktif", "Dengeli"]:
                personality_type = "Yoğun Doğa Aktivitesi Tercih Eden"
                description = "Yoğun doğa aktiviteleri ve macera dolu seyahatler sizi heyecanlandırıyor."
                travel_style = "Yoğun doğa aktivitesi odaklı seyahatler"
            else:
                personality_type = "Rahat Doğa Aktivitesi Tercih Eden"
                description = "Sakin doğa aktiviteleri ve gözlem odaklı seyahatler sizi mutlu ediyor."
                travel_style = "Rahat doğa aktivitesi odaklı seyahatler"
        
        elif "kültür" in user_goal_lower or "tarih" in user_goal_lower or "roma" in user_goal_lower or "paris" in user_goal_lower or "istanbul" in user_goal_lower:
            if dominant_trait in ["Aktif", "Dengeli"]:
                personality_type = "Yoğun Kültür Aktivitesi Tercih Eden"
                description = "Yoğun kültür aktiviteleri ve tarih odaklı seyahatler sizi heyecanlandırıyor."
                travel_style = "Yoğun kültür aktivitesi odaklı seyahatler"
            else:
                personality_type = "Rahat Kültür Aktivitesi Tercih Eden"
                description = "Rahat kültür aktiviteleri ve tarih gözlemi sizi mutlu ediyor."
                travel_style = "Rahat kültür aktivitesi odaklı seyahatler"
        
        elif "gastronomi" in user_goal_lower or "yemek" in user_goal_lower or "italya" in user_goal_lower or "fransa" in user_goal_lower or "tokyo" in user_goal_lower:
            if dominant_trait in ["Aktif", "Dengeli"]:
                personality_type = "Yoğun Gastronomi Aktivitesi Tercih Eden"
                description = "Yoğun gastronomi aktiviteleri ve lezzet odaklı seyahatler sizi heyecanlandırıyor."
                travel_style = "Yoğun gastronomi aktivitesi odaklı seyahatler"
            else:
                personality_type = "Rahat Gastronomi Aktivitesi Tercih Eden"
                description = "Rahat gastronomi aktiviteleri ve lezzet keşfi sizi mutlu ediyor."
                travel_style = "Rahat gastronomi aktivitesi odaklı seyahatler"
        
        elif "lüks" in user_goal_lower or "kaliteli" in user_goal_lower or "bali" in user_goal_lower or "santorini" in user_goal_lower:
            personality_type = "Lüks Aktivite Tercih Eden"
            description = "Lüks ve kaliteli aktiviteler sizi mutlu ediyor."
            travel_style = "Lüks aktivite odaklı seyahatler"
        
        elif "dinlenme" in user_goal_lower or "tatil" in user_goal_lower or "plaj" in user_goal_lower:
            personality_type = "Dinlenme Aktivitesi Tercih Eden"
            description = "Dinlenme ve huzur odaklı aktiviteler sizi mutlu ediyor."
            travel_style = "Dinlenme aktivitesi odaklı seyahatler"
        
        else:
            # Genel analiz - Test sonuçlarına göre
            if dominant_trait in ["Aktif", "Dengeli"]:
                personality_type = "Yoğun Aktivite Tercih Eden"
                description = "Yoğun aktiviteler ve dinamik seyahatler sizi heyecanlandırıyor."
                travel_style = "Yoğun aktivite odaklı seyahatler"
            elif dominant_trait in ["Rahat", "Esnek"]:
                personality_type = "Rahat Aktivite Tercih Eden"
                description = "Rahat ve esnek seyahatler sizi mutlu ediyor."
                travel_style = "Rahat aktivite odaklı seyahatler"
            else:
                personality_type = "Dengeli Aktivite Tercih Eden"
                description = "Dengeli aktiviteler ve çeşitli deneyimler sizi mutlu ediyor."
                travel_style = "Dengeli aktivite odaklı seyahatler"
        
        return {
            "personality_type": personality_type,
            "description": description,
            "travel_style": travel_style
        }
    
    return {
        "personality_type": "Test Sonucu Belirlenemedi",
        "description": "Kişilik profiliniz belirlenemedi. Genel seyahat tercihleriniz dikkate alınacak.",
        "travel_style": "Genel seyahat tercihleri"
    }

def analyze_culture_travel_personality(answers):
    """
    Kültür seyahati kişiliği analizi
    """
    if not answers:
        return "Kültür Meraklısı"
    
    # Kültür seyahati için özel analiz
    culture_score = 0
    luxury_score = 0
    local_score = 0
    
    for answer in answers:
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ["müze", "tarih", "sanat", "mimari"]):
            culture_score += 1
        elif any(word in answer_lower for word in ["lüks", "yüksek", "profesyonel"]):
            luxury_score += 1
        elif any(word in answer_lower for word in ["yerel", "geleneksel", "sokak"]):
            local_score += 1
    
    if culture_score > luxury_score and culture_score > local_score:
        return "Kültür Meraklısı"
    elif luxury_score > culture_score and luxury_score > local_score:
        return "Lüks Kültür Seyahatçısı"
    elif local_score > culture_score and local_score > luxury_score:
        return "Yerel Kültür Seyahatçısı"
    else:
        return "Dengeli Kültür Seyahatçısı"

def analyze_adventure_travel_personality(answers):
    """
    Macera seyahati kişiliği analizi
    """
    if not answers:
        return "Macera Meraklısı"
    
    # Macera seyahati için özel analiz
    adventure_score = 0
    nature_score = 0
    sport_score = 0
    
    for answer in answers:
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ["trekking", "dağ", "zorlu", "kamp"]):
            adventure_score += 1
        elif any(word in answer_lower for word in ["fotoğraf", "gözlem", "orman"]):
            nature_score += 1
        elif any(word in answer_lower for word in ["bisiklet", "su sporları", "aktif"]):
            sport_score += 1
    
    if adventure_score > nature_score and adventure_score > sport_score:
        return "Macera Meraklısı"
    elif nature_score > adventure_score and nature_score > sport_score:
        return "Doğa Gözlemcisi"
    elif sport_score > adventure_score and sport_score > nature_score:
        return "Spor Seyahatçısı"
    else:
        return "Dengeli Macera Seyahatçısı"

def analyze_city_travel_personality(answers):
    """
    Şehir seyahati kişiliği analizi
    """
    if not answers:
        return "Şehir Keşifçisi"
    
    # Şehir seyahati için özel analiz
    urban_score = 0
    culture_score = 0
    shopping_score = 0
    
    for answer in answers:
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ["yoğun", "gece hayatı", "metro", "merkez"]):
            urban_score += 1
        elif any(word in answer_lower for word in ["müze", "galeri", "sanat"]):
            culture_score += 1
        elif any(word in answer_lower for word in ["alışveriş", "eğlence", "kafe"]):
            shopping_score += 1
    
    if urban_score > culture_score and urban_score > shopping_score:
        return "Metropol Seyahatçısı"
    elif culture_score > urban_score and culture_score > shopping_score:
        return "Şehir Kültür Seyahatçısı"
    elif shopping_score > urban_score and shopping_score > culture_score:
        return "Şehir Eğlence Seyahatçısı"
    else:
        return "Dengeli Şehir Seyahatçısı"

def analyze_relaxation_travel_personality(answers):
    """
    Dinlenme seyahati kişiliği analizi
    """
    if not answers:
        return "Dinlenme Arayan"
    
    # Dinlenme seyahati için özel analiz
    luxury_score = 0
    nature_score = 0
    spa_score = 0
    
    for answer in answers:
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ["lüks", "resort", "villa", "yüksek"]):
            luxury_score += 1
        elif any(word in answer_lower for word in ["doğa", "denge", "orman"]):
            nature_score += 1
        elif any(word in answer_lower for word in ["spa", "masaj", "dinlenme"]):
            spa_score += 1
    
    if luxury_score > nature_score and luxury_score > spa_score:
        return "Lüks Dinlenme Seyahatçısı"
    elif nature_score > luxury_score and nature_score > spa_score:
        return "Doğa Dinlenme Seyahatçısı"
    elif spa_score > luxury_score and spa_score > nature_score:
        return "Spa Dinlenme Seyahatçısı"
    else:
        return "Dengeli Dinlenme Seyahatçısı"

def analyze_food_travel_personality(answers):
    """
    Gastronomi seyahati kişiliği analizi
    """
    if not answers:
        return "Lezzet Meraklısı"
    
    # Gastronomi seyahati için özel analiz
    gourmet_score = 0
    local_score = 0
    street_score = 0
    
    for answer in answers:
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ["gurme", "lüks", "michelin", "fine dining"]):
            gourmet_score += 1
        elif any(word in answer_lower for word in ["yerel", "geleneksel", "otantik"]):
            local_score += 1
        elif any(word in answer_lower for word in ["sokak", "kafe", "pazar"]):
            street_score += 1
    
    if gourmet_score > local_score and gourmet_score > street_score:
        return "Gurme Seyahatçısı"
    elif local_score > gourmet_score and local_score > street_score:
        return "Yerel Lezzet Seyahatçısı"
    elif street_score > gourmet_score and street_score > local_score:
        return "Sokak Lezzeti Seyahatçısı"
    else:
        return "Dengeli Gastronomi Seyahatçısı"

def analyze_general_travel_personality(answers):
    """
    Genel seyahat kişiliği analizi
    """
    if not answers:
        return "Genel Seyahatçı"
    
    # Genel seyahat için analiz
    active_score = 0
    balanced_score = 0
    relaxed_score = 0
    luxury_score = 0
    
    for answer in answers:
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ["yoğun", "aktif", "çok"]):
            active_score += 1
        elif any(word in answer_lower for word in ["orta", "dengeli", "denge"]):
            balanced_score += 1
        elif any(word in answer_lower for word in ["rahat", "az", "dinlenme"]):
            relaxed_score += 1
        elif any(word in answer_lower for word in ["lüks", "yüksek", "kaliteli"]):
            luxury_score += 1
    
    if active_score > balanced_score and active_score > relaxed_score and active_score > luxury_score:
        return "Aktif Seyahatçı"
    elif balanced_score > active_score and balanced_score > relaxed_score and balanced_score > luxury_score:
        return "Dengeli Seyahatçı"
    elif relaxed_score > active_score and relaxed_score > balanced_score and relaxed_score > luxury_score:
        return "Rahat Seyahatçı"
    elif luxury_score > active_score and luxury_score > balanced_score and luxury_score > relaxed_score:
        return "Lüks Seyahatçı"
    else:
        return "Genel Seyahatçı"
