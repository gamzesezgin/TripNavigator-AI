import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from gemini_handlers import generate_goal_specific_questions, generate_plan_with_gemini, generate_fallback_plan
from data_handler import load_plans, save_plans, create_new_plan

# .env dosyasındaki değişkenleri yükle
load_dotenv()

st.set_page_config(layout="wide")
st.title("✈️ Yeni Bir Seyahat Planı Oluştur")
st.markdown("Hedefini belirt, seyahat tarzını keşfet, kişiselleştirilmiş günlük aktiviteler al!")

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
    st.subheader("🎯 Adım 1: Seyahat Hedefini ve Tarzını Belirt")
    
    user_goal = st.text_area(
        "Planlamak istediğiniz seyahati buraya yazın:",
        height=100,
        placeholder="Örn: 'Roma'",
        value=st.session_state.user_goal
    )
    
    st.markdown("---")
    
    st.subheader("🎨 Seyahat Tarzı")
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
    
    st.subheader("📅 Seyahat Süresi")
    st.markdown("Kaç günlük bir seyahat planı istiyorsunuz? (Maksimum 7 gün)")
    
    plan_days = st.slider(
        "Gün sayısı:",
        min_value=1,
        max_value=7,
        value=st.session_state.plan_days,
        step=1
    )
    
    # Başlangıç günü seçimi
    st.markdown("**🎯 Başlangıç Günü:**")
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
    st.subheader("🎯 Adım 2: Size Özel Seyahat Planı Oluşturma")
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
        st.subheader("🔍 Kişilik Analizi Sonuçlarınız")
        
        # Analiz sonuçlarını analiz et
        from gemini_handlers import analyze_personality_from_answers
        
        personality_analysis = analyze_personality_from_answers(
            st.session_state.learning_style_answers, 
            st.session_state.user_goal
        )
        
        # Kişilik profili
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**🎭 Seyahat Kişiliğiniz:**")
            st.info(f"**{personality_analysis['personality_type']}**")
            st.write(personality_analysis['description'])
            
            st.markdown("**💡 Seyahat Tarzınız:**")
            st.success(personality_analysis['travel_style'])
        
        
        st.markdown("---")
        
        if st.button("🎯 Kişiselleştirilmiş Seyahat Planımı Oluştur!", type="primary"):
            st.session_state.step = 3
            st.rerun()

# Adım 3: Görevleri oluştur
elif st.session_state.step == 3:
    st.subheader("🚀 Adım 3: Kişiselleştirilmiş Seyahat Planınız Oluşturuluyor")
    
    with st.spinner("🤖 Seyahat planınız hazırlanıyor..."):
        # API'den plan al
        api_key = os.getenv('GEMINI_API_KEY')
        
        try:
            # Seyahat tarzını al
            travel_style = st.session_state.get('travel_style', 'Genel')
            
            # API'den plan al
            api_plan = generate_plan_with_gemini(st.session_state.user_goal, travel_style, st.session_state.plan_days)
            
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
                fallback_plan = generate_fallback_plan(st.session_state.user_goal, travel_style, st.session_state.plan_days)
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
            fallback_plan = generate_fallback_plan(st.session_state.user_goal, travel_style, st.session_state.plan_days)
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
        
        st.success("🎉 Seyahat planınız başarıyla oluşturuldu!")
        st.info("👈 Seyahat planlarınızı görmek ve aktivitelerinizi takip etmek için 'Planlarım' sayfasına gidin.")
        
        # Plan oluşturuldu flag'ini set et
        st.session_state.plan_created = True
        
        # Yeni plan oluştur butonu
        if st.button("🆕 Yeni Seyahat Planı Oluştur", key="new_plan_button"):
            # Session state'i tamamen temizle
            for key in ['step', 'learning_style_answers', 'user_goal', 'plan_days', 'start_day', 'travel_style', 'plan_created']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
            