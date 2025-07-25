import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from gemini_handler import generate_plan_with_gemini
from data_handler import load_plans, save_plans

# .env dosyasındaki değişkenleri yükle
load_dotenv()

st.set_page_config(layout="wide")
st.title("📝 Yeni Bir Plan Oluştur")
st.markdown("Aklındaki hedefi yaz, yapay zekâ senin için yol haritanı çıkarsın!")

# API anahtarını .env dosyasından güvenli bir şekilde al
api_key = os.getenv("GEMINI_API_KEY")

user_goal = st.text_area(
    "🎯 Başarmak istediğiniz hedefi buraya yazın:",
    height=100,
    placeholder="Örn: '3 ay içinde İspanyolca A2 seviyesine gelmek istiyorum.'"
)

if st.button("🚀 Planımı Oluştur!"):
    if not api_key:
        st.error("API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.")
    elif user_goal:
        with st.spinner("🤖 Yapay zeka sizin için en iyi planı hazırlıyor..."):
            generated_plan = generate_plan_with_gemini(user_goal, api_key)
            if generated_plan and 'tasks' in generated_plan:
                
                # Yeni plan için bir yapı oluştur
                new_plan_obj = {
                    "id": str(uuid.uuid4()), # Her plan için benzersiz bir ID
                    "goal": user_goal,
                    "tasks": [
                        {"description": task, "completed": False} for task in generated_plan['tasks']
                    ]
                }

                # Mevcut planları yükle, yenisini ekle ve kaydet
                all_plans = load_plans()
                all_plans.append(new_plan_obj)
                save_plans(all_plans)

                st.success("Planınız başarıyla oluşturuldu ve kaydedildi!")
                st.info("👈 Planlarınızı görmek ve yönetmek için 'Planlarım' sayfasına gidin.")
            else:
                st.error("Plan oluşturulurken bir sorun oluştu. Lütfen tekrar deneyin.")
    else:
        st.warning("Lütfen bir hedef girin.")

