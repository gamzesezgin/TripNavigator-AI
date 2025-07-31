import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from gemini_handler import generate_goal_specific_questions, generate_plan_with_gemini
from data_handler import load_plans, save_plans, create_new_plan

# .env dosyasındaki değişkenleri yükle
load_dotenv()

st.set_page_config(layout="wide")
st.title("📝 Yeni Bir Plan Oluştur")
st.markdown("Hedefini belirt, öğrenme tarzını keşfet, kişiselleştirilmiş görevler al!")

# Session state'i başlat veya temizle
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

# Sayfa yeniden yüklendiğinde session state'i temizle (eğer step 3'te kalmışsa)
# Ama sadece plan oluşturma tamamlandıktan sonra
if st.session_state.step == 3 and 'plan_created' not in st.session_state:
    # Plan oluşturma sürecini başlat
    pass
elif st.session_state.step == 3 and st.session_state.get('plan_created', False):
    # Plan oluşturuldu, session state'i temizle
    st.session_state.step = 1
    st.session_state.learning_style_answers = []
    st.session_state.user_goal = ""
    st.session_state.plan_days = 7
    st.session_state.start_day = 0
    st.session_state.plan_created = False
    st.rerun()

# Demo modu için örnek görevler
def get_demo_tasks(goal, learning_style):
    """Demo modu için örnek görevler oluşturur"""
    demo_tasks = {
        "weekly_tasks": [
            {
                "day": "Pazartesi",
                "tasks": [
                    "Hedefinizle ilgili 10 dakika araştırma yapın",
                    "Bir video izleyin veya podcast dinleyin",
                    "Günlük notlarınızı tutun"
                ]
            },
            {
                "day": "Salı",
                "tasks": [
                    "Pratik bir egzersiz yapın",
                    "Yeni bir yöntem deneyin",
                    "İlerlemenizi değerlendirin"
                ]
            },
            {
                "day": "Çarşamba",
                "tasks": [
                    "Bir uzmanla görüşün veya topluluk katılın",
                    "Öğrendiklerinizi uygulayın",
                    "Motivasyonunuzu artırın"
                ]
            },
            {
                "day": "Perşembe",
                "tasks": [
                    "Tekrar ve pekiştirme yapın",
                    "Yeni bir kaynak keşfedin",
                    "Hedeflerinizi gözden geçirin"
                ]
            },
            {
                "day": "Cuma",
                "tasks": [
                    "Haftalık değerlendirme yapın",
                    "Gelecek hafta için plan yapın",
                    "Başarılarınızı kutlayın"
                ]
            },
            {
                "day": "Cumartesi",
                "tasks": [
                    "Dinlenme ve özetleme günü",
                    "Haftalık notlarınızı gözden geçirin",
                    "Yeni hedefler belirleyin"
                ]
            },
            {
                "day": "Pazar",
                "tasks": [
                    "Haftalık planınızı hazırlayın",
                    "Motivasyonunuzu artırın",
                    "Yeni haftaya hazırlanın"
                ]
            }
        ],
        "motivation_message": f"'{goal}' hedefinize ulaşmak için her gün küçük adımlar atın. Tutarlılık başarının anahtarıdır!"
    }
    return demo_tasks

# Adım 1: Hedef belirleme
if st.session_state.step == 1:
    st.subheader("🎯 Adım 1: Hedefini ve Süreni Belirt")
    
    user_goal = st.text_area(
        "Başarmak istediğiniz hedefi buraya yazın:",
        height=100,
        placeholder="Örn: 'İngilizce öğrenmek istiyorum' veya '5 günlük yurtdışı tatilim için hazırlanmak istiyorum'",
        value=st.session_state.user_goal
    )
    
    st.markdown("---")
    
    st.subheader("📅 Plan Süresi")
    st.markdown("Kaç günlük bir plan istiyorsunuz? (Maksimum 7 gün)")
    
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
        "Planınız hangi günden başlasın?",
        options=day_names,
        index=st.session_state.start_day,
        horizontal=True
    )
    
    # Seçilen günleri göster
    start_day_index = day_names.index(start_day)
    end_day_index = (start_day_index + plan_days - 1) % 7
    end_day = day_names[end_day_index]
    
    if plan_days == 1:
        st.info(f"📅 {start_day} günü için plan oluşturulacak")
    else:
        st.info(f"📅 {start_day}'dan {end_day}'a kadar {plan_days} günlük plan oluşturulacak")
    
    if st.button("İleri", type="primary"):
        if user_goal.strip():
            st.session_state.user_goal = user_goal
            st.session_state.plan_days = plan_days
            st.session_state.start_day = day_names.index(start_day)
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Lütfen bir hedef girin.")

# Adım 2: Hedef bazında sorular
elif st.session_state.step == 2:
    st.subheader("🎯 Adım 2: Size Özel Plan Oluşturma")
    st.markdown("Size en uygun görevleri oluşturmak için birkaç soru soralım.")
    
    questions = generate_goal_specific_questions(st.session_state.user_goal)
    
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
        
        if st.button("🎯 Kişiselleştirilmiş Planımı Oluştur!", type="primary"):
            st.session_state.step = 3
            st.rerun()

# Adım 3: Görevleri oluştur
elif st.session_state.step == 3:
    st.subheader("🚀 Adım 3: Kişiselleştirilmiş Planınız Oluşturuluyor")
    
    with st.spinner("🤖 Planınız hazırlanıyor..."):
        # API'den plan al
        api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key:
            api_plan = generate_plan_with_gemini(st.session_state.user_goal, api_key, st.session_state.plan_days, st.session_state.start_day)
            
            if api_plan and 'weekly_tasks' in api_plan:
                # API'den gelen planı kullan
                weekly_tasks = api_plan['weekly_tasks']
                motivation_message = f"'{st.session_state.user_goal}' hedefinize ulaşmak için her gün küçük adımlar atın. Tutarlılık başarının anahtarıdır!"
            else:
                # API başarısız olursa demo plan kullan
                weekly_tasks = get_demo_tasks(st.session_state.user_goal, "Genel")['weekly_tasks']
                motivation_message = f"'{st.session_state.user_goal}' hedefinize ulaşmak için her gün küçük adımlar atın. Tutarlılık başarının anahtarıdır!"
        else:
            # API key yoksa demo plan kullan
            weekly_tasks = get_demo_tasks(st.session_state.user_goal, "Genel")['weekly_tasks']
            motivation_message = f"'{st.session_state.user_goal}' hedefinize ulaşmak için her gün küçük adımlar atın. Tutarlılık başarının anahtarıdır!"
        
        # Planı oluştur
        new_plan = create_new_plan(
            goal=st.session_state.user_goal,
            weekly_tasks=weekly_tasks,
            learning_style="Kişiselleştirilmiş",
            motivation_message=motivation_message
        )
        
        # Planı kaydet
        all_plans = load_plans()
        all_plans.append(new_plan)
        save_plans(all_plans)
        
        st.success("🎉 Planınız başarıyla oluşturuldu!")
        st.info("👈 Planlarınızı görmek ve görevlerinizi takip etmek için 'Planlarım' sayfasına gidin.")
        
        # Plan oluşturuldu flag'ini set et
        st.session_state.plan_created = True
        
        # Yeni plan oluştur butonu
        if st.button("🆕 Yeni Plan Oluştur", key="new_plan_button"):
            # Session state'i tamamen temizle
            for key in ['step', 'learning_style_answers', 'user_goal', 'plan_days', 'start_day', 'plan_created']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

