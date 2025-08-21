import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from gemini_handlers import generate_plan_with_gemini, generate_ai_destination_recommendation, generate_recommendation_reasoning
from data_handler import load_plans, save_plans, create_new_plan

# .env dosyasındaki değişkenleri yükle
load_dotenv()

st.set_page_config(layout="wide")

# CSS stilleri
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    .hero-section {
        background: linear-gradient(135deg, #3e5151 0%, #decba4 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .step-card {
        background: linear-gradient(to right, #C71A1A 0%, #F0573C 46%, #F77D3B 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        color: white;
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .icon {
        width: 24px;
        height: 24px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 8px;
        filter: brightness(0) invert(1);
    }
    
    .icon-large {
        width: 48px;
        height: 48px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 12px;
        filter: brightness(0) invert(1);
    }
    
    .floating-animation {
        animation: float 3s ease-in-out infinite;
        margin-right: 15px;
        font-size: 3rem;
    }
    
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3.5rem; margin-bottom: 1.5rem; font-weight: 700;">
        <i class="fas fa-robot floating-animation"></i> AI Destinasyon Önerisi
    </h1>
    <h2 style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">Birkaç soruyla sana en uygun seyahat destinasyonunu önereyim!</h2>
</div>
""", unsafe_allow_html=True)

# Sayfa yüklendiğinde session state kontrolü
if st.session_state.get('ai_plan_created', False):
    # Plan oluşturuldu, session state'i temizle
    for key in ['ai_step', 'ai_answers', 'recommended_destination', 'selected_destination_description', 'plan_days', 'start_day', 'ai_plan_created']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Session state'i başlat
if 'ai_step' not in st.session_state:
    st.session_state.ai_step = 1
if 'ai_answers' not in st.session_state:
    st.session_state.ai_answers = {}
if 'recommended_destination' not in st.session_state:
    st.session_state.recommended_destination = ""
if 'selected_destination_description' not in st.session_state:
    st.session_state.selected_destination_description = ""
if 'plan_days' not in st.session_state:
    st.session_state.plan_days = 7
if 'start_day' not in st.session_state:
    st.session_state.start_day = 0
if 'api_quota_exceeded' not in st.session_state:
    st.session_state.api_quota_exceeded = False

# Soru iconları için fonksiyon
# Soru iconları için fonksiyon (Anlamlı Şekiller & Beyaz Renk)
def get_question_icon(question_id):
    icons = {
        "climate": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12,7C10.6,7 9.5,8.1 9.5,9.5C9.5,10.9 10.6,12 12,12C13.4,12 14.5,10.9 14.5,9.5C14.5,8.1 13.4,7 12,7M12,9A1.5,1.5 0 0,1 13.5,10.5A1.5,1.5 0 0,1 12,12A1.5,1.5 0 0,1 10.5,10.5A1.5,1.5 0 0,1 12,9M12,2L9.5,4.5L12,7L14.5,4.5L12,2M19.5,9.5L17,12L19.5,14.5L22,12L19.5,9.5M4.5,9.5L2,12L4.5,14.5L7,12L4.5,9.5M12,17L9.5,19.5L12,22L14.5,19.5L12,17M12,14A2,2 0 0,0 10,16C10,17.1 10.9,18 12,18C13.1,18 14,17.1 14,16A2,2 0 0,0 12,14Z" /></svg>',
        "budget": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M11.5,12C10.12,12 9,10.88 9,9.5C9,8.12 10.12,7 11.5,7C12.88,7 14,8.12 14,9.5C14,10.88 12.88,12 11.5,12M11.5,9C10.67,9 10,9.67 10,10.5C10,11.33 10.67,12 11.5,12C12.33,12 13,11.33 13,10.5C13,9.67 12.33,9 11.5,9M20,6H4V4H20V6M4,18H20V20H4V18M18,7H6V17H18V7M8,9H15V15H8V9Z" /></svg>',
        "activity": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M14.12,10H19V12H14.12L15.17,13.05L14.11,14.11L11,11L14.11,7.89L15.17,8.95L14.12,10M13,3.5C13,4.88 11.88,6 10.5,6S8,4.88 8,3.5S9.12,1 10.5,1S13,2.12 13,3.5M6.5,23V16H5V10.5C5,8.57 6.57,7 8.5,7H12.5C14.43,7 16,8.57 16,10.5V16H14.5V23H6.5Z" /></svg>',
        "distance": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2C6.48,2 2,6.48 2,12C2,17.52 6.48,22 12,22C17.52,22 22,17.52 22,12C22,6.48 17.52,2 12,2M11,18.93C7.05,18.44 4,15.54 4,12C4,11.38 4.08,10.79 4.21,10.21L9,15V16C9,17.1 9.9,18 11,18V18.93M17.9,17.79C17.38,16.63 16.3,15.82 15,15.42V14C15,13.45 14.55,13 14,13H10V11H12C12.55,11 13,10.55 13,10V8C13,7.45 12.55,7 12,7H9.5C8.8,7 8.23,7.41 8.04,8H5.09C5.03,7.67 5,7.34 5,7C5,4.79 6.79,3 9,3C10.66,3 12.09,4.08 12.72,5.5L14.22,7.03C14.73,7.54 15.09,8.22 15.24,9H18.91C19.5,9.67 19.92,10.47 20,11.34C20,11.56 20,11.78 20,12C20,14.09 18.95,16.04 17.9,17.79Z" /></svg>',
        "cuisine": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M16,5V4C16,2.9 16.9,2 18,2H20C21.1,2 22,2.9 22,4V5H16M18,10H22V8H18V10M18,14H22V12H18V14M11.3,2.4C10.5,3.1 10,4.2 10,5.3C10,6.4 10.5,7.5 11.3,8.2L12,9L12.7,8.2C13.5,7.5 14,6.4 14,5.3C14,4.1 13.5,3.1 12.7,2.4L12,1.7L11.3,2.4M4.3,8.4L5.7,7L2,3.3L3.4,1.9L7,5.6L8.4,4.2L5.7,1.5L7.1,0L11.7,4.6L4.3,12L2.9,10.6L4.3,9.1V8.4M3.3,22L7,18.4L8.4,19.8L4.7,23.5L3.3,22M9.4,15.2C10.2,16 10.7,17 10.7,18.2C10.7,19.3 10.2,20.3 9.4,21.1L8.7,21.8L8,21.1C7.2,20.3 6.7,19.3 6.7,18.2C6.7,17 7.2,16 8,15.2L8.7,14.5L9.4,15.2Z" /></svg>',
        "atmosphere": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M16,13C15.71,13 15.42,13.12 15.21,13.33L11.29,11.21C11.42,10.83 11.5,10.43 11.5,10C11.5,9.57 11.42,9.17 11.29,8.79L15.21,6.67C15.42,6.88 15.71,7 16,7C17.1,7 18,6.1 18,5C18,3.9 17.1,3 16,3C14.9,3 14,3.9 14,5C14,5.43 14.08,5.83 14.21,6.21L10.29,8.33C10.08,8.12 9.79,8 9.5,8C8.4,8 7.5,8.9 7.5,10C7.5,11.1 8.4,12 9.5,12C9.79,12 10.08,11.88 10.29,11.67L14.21,13.79C14.08,14.17 14,14.57 14,15C14,16.1 14.9,17 16,17C17.1,17 18,16.1 18,15C18,13.9 17.1,13 16,13Z" /></svg>',
        "language": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M4,2H20A2,2 0 0,1 22,4V16A2,2 0 0,1 20,18H13L11,22L9,18H4A2,2 0 0,1 2,16V4A2,2 0 0,1 4,2M4,4V16H10.1L12,19.8L13.9,16H20V4H4M6,7H8V13H6V7M12,7H10V13H12V7M14,7H16V13H14V7Z" /></svg>',
        "transport": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M21.41,11.58L19.5,13.5L16.5,10.5L14,13L16,15H9V12L11,10L8,7L5,10L7,12H4V9L2,7L3.41,5.59L2,4.17L3.41,2.76L4.83,4.17L6.24,2.76L7.66,4.17L9.07,2.76L10.5,4.17L11.91,2.76L13.33,4.17L14.74,2.76L16.16,4.17L17.57,2.76L19,4.17L20.41,2.76L21.83,4.17L20.41,5.59L21.83,7L20.41,8.41L21.83,9.83L21.41,11.58M12.09,18H16V21H18V18H21V16H18V13H16V16H12.09C12.03,16.33 12,16.66 12,17C12,17.34 12.03,17.67 12.09,18Z" /></svg>',
        "interests": '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z" /></svg>'
    }
    # Varsayılan ikon (eğer eşleşme bulunamazsa)
    return icons.get(question_id, '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/></svg>')

# AI Öneri Soruları
ai_questions = [
    {
        "id": "climate",
        "question": "İklim tercihiniz nedir?",
        "options": ["Sıcak ve güneşli", "Serin ve dağlık", "Ilıman ve ormanlık", "Fark etmez"],
        "category": "climate"
    },
    {
        "id": "budget",
        "question": "Bütçe seviyeniz nedir?",
        "options": ["Düşük bütçe", "Orta bütçe", "Yüksek bütçe", "Karışık"],
        "category": "budget"
    },
    {
        "id": "activity",
        "question": "Hangi aktivite tarzını tercih edersiniz?",
        "options": ["Doğa ve macera", "Tarih ve kültür", "Sanat ve gastronomi", "Alışveriş ve eğlence", "Karışık"],
        "category": "activity"
    },

    {
        "id": "distance",
        "question": "Kıta veya mesafe tercihiniz nedir?",
        "options": ["Türkiye", "Avrupa", "Asya/Amerika/Afrika", "Fark etmez"],
        "category": "distance"
    },
    {
        "id": "cuisine",
        "question": "Yerel mutfak deneyimi ister misiniz?",
        "options": ["Evet, çok önemli", "Hayır, önemsiz", "Karışık"],
        "category": "cuisine"
    },
    {
        "id": "atmosphere",
        "question": "Hangi ortamı tercih edersiniz?",
        "options": ["Canlı ve kalabalık", "Sakin ve huzurlu", "Karışık"],
        "category": "atmosphere"
    },
    {
        "id": "language",
        "question": "Dil konusunda tercihiniz nedir?",
        "options": ["İngilizce konuşulan yerler", "Farklı dillerin konuşulduğu yerler", "Fark etmez"],
        "category": "language"
    },
    {
        "id": "transport",
        "question": "Ulaşım tercihiniz nedir?",
        "options": ["Uçakla uzun yolculuk sorun değil", "Kısa mesafeler tercih", "Fark etmez"],
        "category": "transport"
    },
    {
        "id": "interests",
        "question": "Özel ilgi alanlarınız nelerdir?",
        "options": ["Festival ve etkinlikler", "Müzik ve sanat", "Kış sporları", "Dalış ve su sporları", "Trekking ve doğa", "Fotoğrafçılık", "Hepsi"],
        "category": "interests"
    }
]

# Adım 1: AI Soruları
if st.session_state.ai_step == 1:
    st.markdown("""
    <h3 style="display: flex; align-items: center;">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z"/>
        </svg>
        Adım 1: Seyahat Tercihlerinizi Belirleyelim
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("Size en uygun destinasyonu önerebilmek için birkaç soru soralım.")
    
    # Mevcut cevapları göster
    if st.session_state.ai_answers:
        st.info("Daha önce verdiğiniz cevaplar:")
        for q_id, answer in st.session_state.ai_answers.items():
            question = next((q for q in ai_questions if q["id"] == q_id), None)
            if question:
                # Her soru için uygun icon
                icon_svg = get_question_icon(question["id"])
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    {icon_svg}
                    <span><strong>{question['question']}</strong> → {question['options'][answer]}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("---")
    
    # Mevcut soru
    current_question_index = len(st.session_state.ai_answers)
    if current_question_index < len(ai_questions):
        current_question = ai_questions[current_question_index]
        
        # Mevcut soru için icon
        icon_svg = get_question_icon(current_question["id"])
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            {icon_svg}
            <span style="font-size: 1.2rem; font-weight: bold;">{current_question['question']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        selected_option = st.radio(
            "Seçenekler:",
            current_question['options'],
            key=f"ai_question_{current_question_index}"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Geri"):
                if st.session_state.ai_answers:
                    # Son cevabı sil
                    last_question_id = list(st.session_state.ai_answers.keys())[-1]
                    del st.session_state.ai_answers[last_question_id]
                st.rerun()
        
        with col2:
            if st.button("İleri", type="primary"):
                selected_index = current_question['options'].index(selected_option)
                st.session_state.ai_answers[current_question['id']] = selected_index
                st.rerun()
    
    else:
        st.success("✅ Tüm sorular tamamlandı!")
        
        # Destinasyon önerisi oluştur
        if st.button("Destinasyon Önerimi Al!", type="primary"):
            st.session_state.ai_step = 2
            st.rerun()

# Adım 2: Destinasyon Önerisi
elif st.session_state.ai_step == 2:
    st.markdown("""
    <h3 style="display: flex; align-items: center;">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M7.5,13A2.5,2.5 0 0,0 5,15.5A2.5,2.5 0 0,0 7.5,18A2.5,2.5 0 0,0 10,15.5A2.5,2.5 0 0,0 7.5,13M16.5,13A2.5,2.5 0 0,0 14,15.5A2.5,2.5 0 0,0 16.5,18A2.5,2.5 0 0,0 19,15.5A2.5,2.5 0 0,0 16.5,13Z"/>
        </svg>
        Adım 2: AI Destinasyon Önerisi
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("Cevaplarınıza göre size en uygun destinasyonları öneriyorum...")
    
    # AI çağrısını sadece bir kez yap
    if 'recommended_destinations' not in st.session_state:
        with st.spinner("🤖 AI analiz yapıyor ve en uygun destinasyonları buluyor..."):
            # AI'dan destinasyon önerisi al
            api_key = os.getenv('GEMINI_API_KEY')
            
            if api_key:
                try:
                    # Kullanıcı cevaplarını analiz et ve destinasyon öner
                    # Cevapları liste formatına çevir
                    answers_list = []
                    for q_id, answer_index in st.session_state.ai_answers.items():
                        question = next((q for q in ai_questions if q["id"] == q_id), None)
                        if question:
                            answers_list.append(question['options'][answer_index])
                    
                    # API kotası kontrolü - eğer daha önce hata aldıysak direkt fallback kullan
                    if st.session_state.get('api_quota_exceeded', False):
                        st.warning("⚠️ API kotası doldu, önceden hazırlanmış öneriler kullanılıyor...")
                        from gemini_handlers.ai_destination_recommender import generate_fallback_destinations
                        st.session_state.recommended_destinations = generate_fallback_destinations(answers_list, ai_questions, [])
                    else:
                        st.session_state.recommended_destinations = generate_ai_destination_recommendation(
                            answers_list, ai_questions
                        )
                    
                except Exception as e:
                    error_message = str(e)
                    if "429" in error_message or "quota" in error_message.lower():
                        st.error("❌ API kotası doldu! Günlük 50 istek limiti aşıldı.")
                        st.info("💡 Yarın tekrar deneyebilir veya ücretli plana geçebilirsiniz.")
                        # Kotası doldu flag'ini set et
                        st.session_state.api_quota_exceeded = True
                        if st.button("🔄 Fallback Önerileri Kullan"):
                            # Fallback önerilerini yükle
                            from gemini_handlers.ai_destination_recommender import generate_fallback_destinations
                            answers_list = []
                            for q_id, answer_index in st.session_state.ai_answers.items():
                                question = next((q for q in ai_questions if q["id"] == q_id), None)
                                if question:
                                    answers_list.append(question['options'][answer_index])
                            st.session_state.recommended_destinations = generate_fallback_destinations(answers_list, ai_questions, [])
                            st.rerun()
                        st.stop()
                    else:
                        st.error(f"❌ AI servisi hatası: {e}")
                        if st.button("🔄 Tekrar Dene"):
                            # Session state'i temizle ve tekrar dene
                            if 'recommended_destinations' in st.session_state:
                                del st.session_state.recommended_destinations
                            st.rerun()
                        st.stop()
            else:
                st.error("❌ API anahtarı bulunamadı. Lütfen sistem yöneticisi ile iletişime geçin.")
                st.stop()
    
    # Destinasyonları göster
    if 'recommended_destinations' in st.session_state and st.session_state.recommended_destinations and len(st.session_state.recommended_destinations) >= 3:
        st.success("🎉 Size önerilen 3 destinasyon:")
        
        # 3 destinasyonu göster ve seçim yaptır
        st.markdown("**🌟 Lütfen size en uygun olan destinasyonu seçin:**")
        
        # Destinasyonları kartlar halinde göster
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       padding: 1.5rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;">
                <h4 style="color: white; margin-bottom: 1rem;">🏆 1. Seçenek</h4>
                <h3 style="color: white; margin-bottom: 0.5rem;">{st.session_state.recommended_destinations[0]['name']}</h3>
                <p style="color: white; font-size: 0.9rem;">{st.session_state.recommended_destinations[0]['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"✅ {st.session_state.recommended_destinations[0]['name']} Seç", key="dest1", use_container_width=True):
                st.session_state.recommended_destination = st.session_state.recommended_destinations[0]['name']
                st.session_state.selected_destination_description = st.session_state.recommended_destinations[0]['description']
                # st.rerun() kaldırıldı - artık gereksiz yeniden yükleme yok
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                       padding: 1.5rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;">
                <h4 style="color: white; margin-bottom: 1rem;">🥈 2. Seçenek</h4>
                <h3 style="color: white; margin-bottom: 0.5rem;">{st.session_state.recommended_destinations[1]['name']}</h3>
                <p style="color: white; font-size: 0.9rem;">{st.session_state.recommended_destinations[1]['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"✅ {st.session_state.recommended_destinations[1]['name']} Seç", key="dest2", use_container_width=True):
                st.session_state.recommended_destination = st.session_state.recommended_destinations[1]['name']
                st.session_state.selected_destination_description = st.session_state.recommended_destinations[1]['description']
                # st.rerun() kaldırıldı - artık gereksiz yeniden yükleme yok
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                       padding: 1.5rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;">
                <h4 style="color: white; margin-bottom: 1rem;">🥉 3. Seçenek</h4>
                <h3 style="color: white; margin-bottom: 0.5rem;">{st.session_state.recommended_destinations[2]['name']}</h3>
                <p style="color: white; font-size: 0.9rem;">{st.session_state.recommended_destinations[2]['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"✅ {st.session_state.recommended_destinations[2]['name']} Seç", key="dest3", use_container_width=True):
                st.session_state.recommended_destination = st.session_state.recommended_destinations[2]['name']
                st.session_state.selected_destination_description = st.session_state.recommended_destinations[2]['description']
                # st.rerun() kaldırıldı - artık gereksiz yeniden yükleme yok
        
        # Seçim yapıldıysa devam et
        if 'recommended_destination' in st.session_state and st.session_state.recommended_destination:
            st.markdown("---")
            st.success(f"🎯 **Seçilen Destinasyon:** {st.session_state.recommended_destination}")
            
            # Öneri gerekçesi
            st.info("💡 **Öneri Gerekçesi:**")
            # Cevapları liste formatına çevir
            answers_list = []
            for q_id, answer_index in st.session_state.ai_answers.items():
                question = next((q for q in ai_questions if q["id"] == q_id), None)
                if question:
                    answers_list.append(question['options'][answer_index])
            
            st.write(generate_recommendation_reasoning(answers_list, ai_questions, st.session_state.recommended_destination))
            
            st.markdown("---")
            
            # Seyahat süresi seçimi
            st.markdown("""
            <h4 style="display: flex; align-items: center;">
                <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,2C13.1,2 14,2.9 14,4C14,5.1 13.1,6 12,6C10.9,6 10,5.1 10,4C10,2.9 10.9,2 12,2M21,9V7L15,1H5C3.89,1 3,1.89 3,3V21A2,2 0 0,0 5,23H19A2,2 0 0,0 21,21V9M19,9H14V4H5V21H19V9Z"/>
                </svg>
                Seyahat Süresi
            </h4>
            """, unsafe_allow_html=True)
            st.markdown("Seçilen destinasyon için kaç günlük bir seyahat planı istiyorsunuz?")
            
            plan_days = st.slider(
                "Gün sayısı:",
                min_value=1,
                max_value=7,
                value=5,
                step=1
            )
            
            # Başlangıç günü seçimi
            st.markdown("""
            <h4 style="display: flex; align-items: center;">
                <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
                </svg>
                Başlangıç Günü
            </h4>
            """, unsafe_allow_html=True)
            day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
            
            start_day = st.radio(
                "Seyahatiniz hangi günden başlasın?",
                options=day_names,
                index=0,
                horizontal=True
            )
            
            if st.button("Bu Destinasyon İçin Plan Oluştur!", type="primary"):
                st.session_state.plan_days = plan_days
                st.session_state.start_day = day_names.index(start_day)
                st.session_state.ai_step = 3
                st.rerun()
    
    else:
        st.error("❌ AI servisi şu anda yanıt veremiyor. Lütfen daha sonra tekrar deneyin.")
        if st.button("🔄 Tekrar Dene"):
            # Session state'i temizle ve tekrar dene
            if 'recommended_destinations' in st.session_state:
                del st.session_state.recommended_destinations
            st.session_state.ai_step = 1
            st.rerun()

# Adım 3: Plan Oluşturma
elif st.session_state.ai_step == 3:
    st.markdown("""
    <h3 style="display: flex; align-items: center;">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M13,2.05V4.05C17.39,4.59 20.5,8.58 19.96,12.97C19.5,16.61 16.64,19.5 13,19.93V21.93C18.5,21.38 22.5,16.5 21.95,11C21.5,6.25 17.73,2.5 13,2.03V2.05M5.67,19.74C7.18,21 9.04,21.79 11,22V20C9.58,19.82 8.23,19.25 7.1,18.37L5.67,19.74M7.1,5.74C8.22,4.84 9.57,4.26 11,4.06V2.06C9.05,2.25 7.19,3 5.67,4.26L7.1,5.74M5.69,7.1L4.26,5.67C3,7.19 2.25,9.04 2.05,11H4.05C4.24,9.58 4.8,8.23 5.69,7.1M4.06,13H2.06C2.26,14.96 3.03,16.81 4.27,18.33L5.69,16.9C4.81,15.77 4.24,14.42 4.06,13M10,16.5L16,14L16.5,15.5L14,16.5L10,16.5M16,12.5L10,10.5L9.5,12L12,13L16,12.5M16,9.5L10,7.5L9.5,9L12,10L16,9.5M16,6.5L10,4.5L9.5,6L12,7L16,6.5M16,3.5L10,1.5L9.5,3L12,4L16,3.5"/>
        </svg>
        Adım 3: Kişiselleştirilmiş Seyahat Planınız Oluşturuluyor
    </h3>
    """, unsafe_allow_html=True)
    
    with st.spinner("🤖 Seyahat planınız hazırlanıyor..."):
        # API'den plan al
        api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key:
            try:
                day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
                start_day = day_names[st.session_state.start_day]
                api_plan = generate_plan_with_gemini(
                    st.session_state.recommended_destination,
                    plan_days=st.session_state.plan_days,
                    start_day=start_day
                )
                
                if api_plan and 'days' in api_plan:
                    # API'den gelen planı kullan
                    weekly_tasks = []
                    for day in api_plan['days']:
                        weekly_tasks.append({
                            'day': day['day'],
                            'tasks': day['activities']
                        })
                    motivation_message = f"'{st.session_state.recommended_destination}' seyahatinizde her gün unutulmaz anılar biriktirin!"
                else:
                    # API başarısız olursa hata ver
                    st.error("❌ AI servisi şu anda yanıt veremiyor. Lütfen daha sonra tekrar deneyin.")
                    st.stop()
            except Exception as e:
                # API hatası durumunda hata ver
                st.error("❌ AI servisi zaman aşımına uğradı. Lütfen daha sonra tekrar deneyin.")
                st.stop()
        else:
            # API key yoksa hata ver
            st.error("❌ API anahtarı bulunamadı. Lütfen sistem yöneticisi ile iletişime geçin.")
            st.stop()
        
        # Planı oluştur
        new_plan = create_new_plan(
            goal=f"AI Önerisi: {st.session_state.recommended_destination}",
            weekly_tasks=weekly_tasks,
            learning_style="AI Önerisi",
            motivation_message=motivation_message,
            survey_answers=list(st.session_state.ai_answers.values())
        )
        
        # Planı kaydet
        all_plans = load_plans()
        all_plans.append(new_plan)
        save_plans(all_plans)
        
        st.success("Seyahat planınız başarıyla oluşturuldu!")
        st.info("Seyahat planlarınızı görmek ve aktivitelerinizi takip etmek için 'Seyahatlerim' sayfasına gidin.")
        
        # Plan oluşturuldu flag'ini set et
        st.session_state.ai_plan_created = True
        
        # Yeni plan oluştur butonu
        if st.button("Yeni AI Önerisi Al", key="new_ai_plan_button"):
            # Session state'i tamamen temizle
            for key in ['ai_step', 'ai_answers', 'recommended_destination', 'selected_destination_description', 'plan_days', 'start_day', 'ai_plan_created']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()