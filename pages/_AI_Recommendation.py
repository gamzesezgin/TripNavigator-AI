import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from gemini_handler import generate_plan_with_gemini, generate_ai_destination_recommendation, generate_recommendation_reasoning
from data_handler import load_plans, save_plans, create_new_plan

# .env dosyasındaki değişkenleri yükle
load_dotenv()

st.set_page_config(layout="wide")
st.title("🤖 AI Destinasyon Önerisi")
st.markdown("Birkaç soruyla sana en uygun seyahat destinasyonunu önereyim!")

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

# AI Öneri Soruları
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

# Adım 1: AI Soruları
if st.session_state.ai_step == 1:
    st.subheader("🎯 Adım 1: Seyahat Tercihlerinizi Belirleyelim")
    st.markdown("Size en uygun destinasyonu önerebilmek için birkaç soru soralım.")
    
    # Mevcut cevapları göster
    if st.session_state.ai_answers:
        st.info("📝 Daha önce verdiğiniz cevaplar:")
        for q_id, answer in st.session_state.ai_answers.items():
            question = next((q for q in ai_questions if q["id"] == q_id), None)
            if question:
                st.write(f"**{question['question']}** → {question['options'][answer]}")
        st.markdown("---")
    
    # Mevcut soru
    current_question_index = len(st.session_state.ai_answers)
    if current_question_index < len(ai_questions):
        current_question = ai_questions[current_question_index]
        
        st.write(f"**{current_question['question']}**")
        
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
        if st.button("🤖 Destinasyon Önerimi Al!", type="primary"):
            st.session_state.ai_step = 2
            st.rerun()

# Adım 2: Destinasyon Önerisi
elif st.session_state.ai_step == 2:
    st.subheader("🤖 Adım 2: AI Destinasyon Önerisi")
    st.markdown("Cevaplarınıza göre size en uygun destinasyonları öneriyorum...")
    
    with st.spinner("🤖 AI analiz yapıyor ve en uygun destinasyonları buluyor..."):
        # AI'dan destinasyon önerisi al
        api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key:
            try:
                # Kullanıcı cevaplarını analiz et ve destinasyon öner
                recommended_destinations = generate_ai_destination_recommendation(
                    st.session_state.ai_answers, api_key
                )
                
                if recommended_destinations and len(recommended_destinations) >= 3:
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
                            <h3 style="color: white; margin-bottom: 0.5rem;">{recommended_destinations[0]['name']}</h3>
                            <p style="color: white; font-size: 0.9rem;">{recommended_destinations[0]['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"✅ {recommended_destinations[0]['name']} Seç", key="dest1", use_container_width=True):
                            st.session_state.recommended_destination = recommended_destinations[0]['name']
                            st.session_state.selected_destination_description = recommended_destinations[0]['description']
                            st.rerun()
                    
                    with col2:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                   padding: 1.5rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;">
                            <h4 style="color: white; margin-bottom: 1rem;">🥈 2. Seçenek</h4>
                            <h3 style="color: white; margin-bottom: 0.5rem;">{recommended_destinations[1]['name']}</h3>
                            <p style="color: white; font-size: 0.9rem;">{recommended_destinations[1]['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"✅ {recommended_destinations[1]['name']} Seç", key="dest2", use_container_width=True):
                            st.session_state.recommended_destination = recommended_destinations[1]['name']
                            st.session_state.selected_destination_description = recommended_destinations[1]['description']
                            st.rerun()
                    
                    with col3:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                   padding: 1.5rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;">
                            <h4 style="color: white; margin-bottom: 1rem;">🥉 3. Seçenek</h4>
                            <h3 style="color: white; margin-bottom: 0.5rem;">{recommended_destinations[2]['name']}</h3>
                            <p style="color: white; font-size: 0.9rem;">{recommended_destinations[2]['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"✅ {recommended_destinations[2]['name']} Seç", key="dest3", use_container_width=True):
                            st.session_state.recommended_destination = recommended_destinations[2]['name']
                            st.session_state.selected_destination_description = recommended_destinations[2]['description']
                            st.rerun()
                    
                    # Seçim yapıldıysa devam et
                    if 'recommended_destination' in st.session_state and st.session_state.recommended_destination:
                        st.markdown("---")
                        st.success(f"🎯 **Seçilen Destinasyon:** {st.session_state.recommended_destination}")
                        
                        # Öneri gerekçesi
                        st.info("💡 **Öneri Gerekçesi:**")
                        st.write(generate_recommendation_reasoning(st.session_state.ai_answers, st.session_state.recommended_destination))
                        
                        st.markdown("---")
                        
                        # Seyahat süresi seçimi
                        st.subheader("📅 Seyahat Süresi")
                        st.markdown("Seçilen destinasyon için kaç günlük bir seyahat planı istiyorsunuz?")
                        
                        plan_days = st.slider(
                            "Gün sayısı:",
                            min_value=1,
                            max_value=7,
                            value=5,
                            step=1
                        )
                        
                        # Başlangıç günü seçimi
                        st.markdown("**🎯 Başlangıç Günü:**")
                        day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
                        
                        start_day = st.radio(
                            "Seyahatiniz hangi günden başlasın?",
                            options=day_names,
                            index=0,
                            horizontal=True
                        )
                        
                        if st.button("🎯 Bu Destinasyon İçin Plan Oluştur!", type="primary"):
                            st.session_state.plan_days = plan_days
                            st.session_state.start_day = day_names.index(start_day)
                            st.session_state.ai_step = 3
                            st.rerun()
                
                else:
                    st.error("❌ AI servisi şu anda yanıt veremiyor. Lütfen daha sonra tekrar deneyin.")
                    if st.button("🔄 Tekrar Dene"):
                        st.session_state.ai_step = 1
                        st.rerun()
                        
            except Exception as e:
                st.error(f"❌ AI servisi hatası: {e}")
                if st.button("🔄 Tekrar Dene"):
                    st.session_state.ai_step = 1
                    st.rerun()
        else:
            st.error("❌ API anahtarı bulunamadı. Lütfen sistem yöneticisi ile iletişime geçin.")

# Adım 3: Plan Oluşturma
elif st.session_state.ai_step == 3:
    st.subheader("🚀 Adım 3: Kişiselleştirilmiş Seyahat Planınız Oluşturuluyor")
    
    with st.spinner("🤖 Seyahat planınız hazırlanıyor..."):
        # API'den plan al
        api_key = os.getenv('GEMINI_API_KEY')
        
        if api_key:
            try:
                api_plan = generate_plan_with_gemini(
                    st.session_state.recommended_destination, 
                    api_key, 
                    st.session_state.plan_days, 
                    st.session_state.start_day
                )
                
                if api_plan and 'weekly_tasks' in api_plan:
                    # API'den gelen planı kullan
                    weekly_tasks = api_plan['weekly_tasks']
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
        
        st.success("🎉 Seyahat planınız başarıyla oluşturuldu!")
        st.info("👈 Seyahat planlarınızı görmek ve aktivitelerinizi takip etmek için 'Planlarım' sayfasına gidin.")
        
        # Plan oluşturuldu flag'ini set et
        st.session_state.ai_plan_created = True
        
        # Yeni plan oluştur butonu
        if st.button("🆕 Yeni AI Önerisi Al", key="new_ai_plan_button"):
            # Session state'i tamamen temizle
            for key in ['ai_step', 'ai_answers', 'recommended_destination', 'selected_destination_description', 'plan_days', 'start_day', 'ai_plan_created']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
