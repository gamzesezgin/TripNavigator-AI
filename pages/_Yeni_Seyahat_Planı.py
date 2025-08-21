import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from gemini_handlers import generate_goal_specific_questions, generate_plan_with_gemini, generate_fallback_plan
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
        <i class="fas fa-plane-departure floating-animation"></i> Yeni Seyahat Planı
    </h1>
    <h2 style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">Hedefini belirt, seyahat tarzını keşfet, kişiselleştirilmiş günlük aktiviteler al!</h2>
</div>
""", unsafe_allow_html=True)

# Sayfa yüklendiğinde session state kontrolü
# Eğer önceki bir plan oluşturma işlemi tamamlanmışsa, session state'i sıfırla
if st.session_state.get('plan_created', False):
    # Plan oluşturuldu, session state'i temizle
    for key in ['step', 'learning_style_answers', 'user_goal', 'plan_days', 'start_day', 'travel_style', 'plan_created']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Session state'i başlat
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'learning_style_answers' not in st.session_state:
    st.session_state.learning_style_answers = []
if 'user_goal' not in st.session_state:
    st.session_state.user_goal = ""
if 'plan_days' not in st.session_state:
    st.session_state.plan_days = 7
if 'start_day' not in st.session_state:
    st.session_state.start_day = 0  # 0=Pazartesi, 1=Salı, 2=Çarşamba, ...
if 'travel_style' not in st.session_state:
    st.session_state.travel_style = "Doğa ve macera"

# Adım 1: Hedef belirleme
if st.session_state.step == 1:
    st.markdown("""
    <h3 style="display: flex; align-items: center;">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z"/>
        </svg>
        Adım 1: Seyahat Hedefini ve Tarzını Belirt
    </h3>
    """, unsafe_allow_html=True)
    
    user_goal = st.text_area(
        "Planlamak istediğiniz seyahati buraya yazın:",
        height=100,
        placeholder="Örn: 'Roma'",
        value=st.session_state.user_goal
    )
    
    st.markdown("---")
    
    st.markdown("""
    <h4 style="display: flex; align-items: center;">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/>
        </svg>
        Seyahat Tarzı
    </h4>
    """, unsafe_allow_html=True)
    st.markdown("Hangi tarz bir gezi istiyorsunuz?")
    
    travel_style = st.selectbox(
        "Seyahat tarzınız:",
        options=[
            "Doğa ve macera",
            "Tarih ve kültür", 
            "Sanat ve gastronomi",
            "Alışveriş ve eğlence",
            "Tatil ve dinlenme",
            "Karışık (hepsinden biraz)"
        ],
        index=["Doğa ve macera", "Tarih ve kültür", "Sanat ve gastronomi", "Alışveriş ve eğlence", "Tatil ve dinlenme", "Karışık (hepsinden biraz)"].index(st.session_state.travel_style)
    )
    
    st.markdown("---")
    
    st.markdown("""
    <h4 style="display: flex; align-items: center;">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,2C13.1,2 14,2.9 14,4C14,5.1 13.1,6 12,6C10.9,6 10,5.1 10,4C10,2.9 10.9,2 12,2M21,9V7L15,1H5C3.89,1 3,1.89 3,3V21A2,2 0 0,0 5,23H19A2,2 0 0,0 21,21V9M19,9H14V4H5V21H19V9Z"/>
        </svg>
        Seyahat Süresi
    </h4>
    """, unsafe_allow_html=True)
    st.markdown("Kaç günlük bir seyahat planı istiyorsunuz? (Maksimum 7 gün)")
    
    plan_days = st.slider(
        "Gün sayısı:",
        min_value=1,
        max_value=7,
        value=st.session_state.plan_days,
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
    
    # Başlangıç günü için radio button
    start_day = st.radio(
        "Seyahatiniz hangi günden başlasın?",
        options=day_names,
        index=st.session_state.start_day,
        horizontal=True
    )
    
    # Seçilen günleri göster
    start_day_index = day_names.index(start_day)
    end_day_index = (start_day_index + plan_days - 1) % 7
    end_day = day_names[end_day_index]
    
    if plan_days == 1:
        st.info(f"📅 {start_day} günü için seyahat planı oluşturulacak")
    else:
        st.info(f"📅 {start_day}'dan {end_day}'a kadar {plan_days} günlük seyahat planı oluşturulacak")
    
    if st.button("İleri", type="primary"):
        if user_goal.strip():
            st.session_state.user_goal = user_goal
            st.session_state.plan_days = plan_days
            st.session_state.start_day = day_names.index(start_day)
            st.session_state.travel_style = travel_style
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Lütfen bir seyahat hedefi girin.")

# Adım 2: Hedef bazında sorular
elif st.session_state.step == 2:
    st.markdown("""
    <h3 style="display: flex; align-items: center;">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"/>
        </svg>
        Adım 2: Size Özel Seyahat Planı Oluşturma
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("Size en uygun aktiviteleri oluşturmak için birkaç soru soralım.")
    
    questions = generate_goal_specific_questions(st.session_state.user_goal, st.session_state.travel_style)
    
    if len(st.session_state.learning_style_answers) < len(questions):
        current_question_index = len(st.session_state.learning_style_answers)
        current_question = questions[current_question_index]
        
        st.write(f"**{current_question['question']}**")
        
        selected_option = st.radio(
            "Seçenekler:",
            current_question['options'],
            key=f"question_{current_question_index}"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Geri"):
                if st.session_state.learning_style_answers:
                    st.session_state.learning_style_answers.pop()
                else:
                    st.session_state.step = 1
                st.rerun()
        
        with col2:
            if st.button("İleri", type="primary"):
                selected_index = current_question['options'].index(selected_option)
                st.session_state.learning_style_answers.append(selected_index)
                st.rerun()
    
    else:
        st.success("✅ Analiz tamamlandı!")
        
        # Kişilik analizi sonuçlarını göster
        st.markdown("""
        <h3 style="display: flex; align-items: center;">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
            </svg>
            Kişilik Analizi Sonuçlarınız
        </h3>
        """, unsafe_allow_html=True)
        
        # Analiz sonuçlarını analiz et
        from gemini_handlers import analyze_personality_from_answers
        
        personality_analysis = analyze_personality_from_answers(
            st.session_state.learning_style_answers, 
            st.session_state.user_goal
        )
        
        # Kişilik profili
        st.markdown("""
        <h4 style="display: flex; align-items: center;">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/>
            </svg>
            Kişilik Analizi Sonucunuz
        </h4>
        """, unsafe_allow_html=True)
        st.info(personality_analysis['description'])
        
        
        st.markdown("---")
        
        if st.button("Kişiselleştirilmiş Seyahat Planımı Oluştur!", type="primary"):
            st.session_state.step = 3
            st.rerun()

# Adım 3: Görevleri oluştur
elif st.session_state.step == 3:
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
        
        try:
            # Seyahat tarzını al
            travel_style = st.session_state.get('travel_style', 'Genel')
            
            # API'den plan al
            day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
            start_day = day_names[st.session_state.start_day]
            api_plan = generate_plan_with_gemini(st.session_state.user_goal, travel_style, st.session_state.plan_days, start_day)
            
            if api_plan and 'days' in api_plan:
                # API'den gelen planı kullan
                weekly_tasks = []
                for day_data in api_plan['days']:
                    day_name = day_data['day']
                    activities = day_data['activities']
                    weekly_tasks.append({
                        'day': day_name,
                        'tasks': activities
                    })
                motivation_message = f"'{st.session_state.user_goal}' seyahatinizde her gün unutulmaz anılar biriktirin!"
            else:
                # API başarısız olursa fallback plan kullan
                st.warning("⚠️ AI servisi şu anda yanıt veremiyor. Varsayılan plan oluşturuluyor...")
                fallback_plan = generate_fallback_plan(st.session_state.user_goal, travel_style, st.session_state.plan_days, start_day)
                weekly_tasks = []
                for day_data in fallback_plan['days']:
                    day_name = day_data['day']
                    activities = day_data['activities']
                    weekly_tasks.append({
                        'day': day_name,
                        'tasks': activities
                    })
                motivation_message = f"'{st.session_state.user_goal}' seyahatinizde her gün unutulmaz anılar biriktirin!"
        except Exception as e:
            # API hatası durumunda fallback plan kullan
            st.warning("⚠️ AI servisi zaman aşımına uğradı. Varsayılan plan oluşturuluyor...")
            fallback_plan = generate_fallback_plan(st.session_state.user_goal, travel_style, st.session_state.plan_days, start_day)
            weekly_tasks = []
            for day_data in fallback_plan['days']:
                day_name = day_data['day']
                activities = day_data['activities']
                weekly_tasks.append({
                    'day': day_name,
                    'tasks': activities
                })
            motivation_message = f"'{st.session_state.user_goal}' seyahatinizde her gün unutulmaz anılar biriktirin!"
        
        # Planı oluştur
        new_plan = create_new_plan(
            goal=st.session_state.user_goal,
            weekly_tasks=weekly_tasks,
            learning_style="Kişiselleştirilmiş",
            motivation_message=motivation_message,
            survey_answers=st.session_state.get('learning_style_answers', [])
        )
        
        # Planı kaydet
        all_plans = load_plans()
        all_plans.append(new_plan)
        save_plans(all_plans)
        
        st.success("Seyahat planınız başarıyla oluşturuldu!")
        st.info("Seyahat planlarınızı görmek ve aktivitelerinizi takip etmek için 'Seyahatlerim' sayfasına gidin.")
        
        # Plan oluşturuldu flag'ini set et
        st.session_state.plan_created = True
        
        # Yeni plan oluştur butonu
        if st.button("Yeni Seyahat Planı Oluştur", key="new_plan_button"):
            # Session state'i tamamen temizle
            for key in ['step', 'learning_style_answers', 'user_goal', 'plan_days', 'start_day', 'travel_style', 'plan_created']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
            