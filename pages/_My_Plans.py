import streamlit as st
from data_handler import load_plans, save_plans, get_current_week_tasks, mark_task_completed, unmark_task_completed
from datetime import datetime
from agents.recommender_agent import recommend_pois

st.set_page_config(layout="wide")
st.title("✈️ Seyahat Planlarım ve Aktivite Takibi")

if 'confirming_delete' not in st.session_state:
    st.session_state.confirming_delete = None

all_plans = load_plans()

if not all_plans:
    st.info("Henüz kaydedilmiş bir seyahat planınız yok. 'Yeni Seyahat Planı Oluştur' sayfasından ilk seyahatinizi planlayabilirsiniz!")
else:
    st.markdown("Aşağıda kayıtlı seyahat planlarınızı ve günlük aktivite durumunuzu görebilirsiniz.")
    
    for index, plan in enumerate(reversed(all_plans)):
        st.markdown("---")
        
        # Plan başlığı ve bilgileri
        with st.expander(f"✈️ **Seyahat:** {plan['goal']}", expanded=True):
            
            # Plan bilgileri
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.subheader("🗺️ Tüm Günlük Aktiviteler")
                
                if plan.get('weekly_tasks'):
                    for week_tasks in plan['weekly_tasks']:
                        st.write(f"**📆 {week_tasks['day']}**")
                        
                        for task_index, task in enumerate(week_tasks['tasks']):
                            # Bu aktivitenin tamamlanıp tamamlanmadığını kontrol et
                            is_completed = False
                            for completed_task in plan.get('completed_tasks', []):
                                if (completed_task.get('day') == week_tasks.get('day') and 
                                    completed_task.get('task_index') == task_index):
                                    is_completed = True
                                    break
                            
                            # Checkbox ile aktivite durumu
                            checkbox_key = f"task_{plan['id']}_{week_tasks['day']}_{task_index}"
                            checkbox_value = st.checkbox(
                                task,
                                value=is_completed,
                                key=checkbox_key
                            )
                            
                            # Checkbox durumu değiştiğinde işlem yap
                            if checkbox_value != is_completed:
                                if checkbox_value:
                                    # Aktiviteyi tamamlandı olarak işaretle
                                    mark_task_completed(plan['id'], week_tasks['day'], task_index)
                                else:
                                    # Aktiviteyi tamamlanmamış olarak işaretle
                                    unmark_task_completed(plan['id'], week_tasks['day'], task_index)
                                st.rerun()
                        
                        st.markdown("---")
                else:
                    st.write("Bu seyahat planı için aktivite bulunmuyor.")
            
            with col2:
                st.subheader("🌟 Önerilen Mekanlar")

                st.info("Mekan önerileri için Gemini AI kullanılıyor.")

                # Tabs oluştur
                tabs = st.tabs(["🗺️ Gezi Noktaları", "🍽️ Yemek Önerileri"])

                with tabs[0]:
                    st.caption("Gemini AI ile popüler gezi noktaları")
                    city_or_goal = plan.get('goal', '')
                    with st.spinner("Gezilecek yerler alınıyor..."):
                        try:
                            places = get_popular_attractions(city_or_goal, top_k=8)
                        except Exception:
                            places = []

                    if places:
                        cols = st.columns(2)
                        for i, p in enumerate(places):
                            with cols[i % 2]:
                                st.markdown(
                                    f"""
                                    <div style=\"border:1px solid #eee; border-radius:10px; padding:12px; margin-bottom:12px;\">
                                        <div style=\"font-weight:600; font-size:1rem;\">{p.get('name','')}</div>
                                        <div style=\"font-size:0.9rem; color:#666; margin-top:2px;\">
                                            {p.get('kind','').title()} {('• ' + p.get('city','')) if p.get('city') else ''} {('• ' + p.get('neighborhood','')) if p.get('neighborhood') else ''}
                                        </div>
                                        <div style=\"margin-top:8px;\">{p.get('short_reason','')}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                    else:
                        st.info("Gezi önerisi bulunamadı. Hedefi şehir/ülke adı içerecek şekilde yazmayı deneyin.")

                with tabs[1]:
                    st.caption("🔍 Gerçek Zamanlı Yemek Önerileri (OpenTripMap API)")
                    
                    # Yemek arama formu
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        cuisine = st.selectbox(
                            "🍽️ Mutfak Türü",
                            options=[
                                "genel",
                                "balık ekmek",
                                "kebap",
                                "lahmacun",
                                "kahve",
                                "çay",
                                "tatlı",
                                "dondurma",
                                "pizza",
                                "sushi",
                                "burger",
                                "çorba"
                            ],
                            help="Hangi tür yemek arıyorsunuz?",
                            key=f"cuisine_{plan['id']}"
                        )
                    
                    with col2:
                        search_button = st.button("🔍 Ara", type="primary", use_container_width=True, key=f"search_{plan['id']}")
                    
                    with col3:
                        st.write("")  # Boşluk için
                    
                    # Arama sonuçları
                    if search_button:
                        st.markdown("---")
                        st.subheader(f"🍽️ {plan.get('goal', '')} - {cuisine.title()} Önerileri")
                        
                        try:
                            from agents.food_recommender import get_food_recommendations
                            
                            with st.spinner("🍽️ Yemek mekanları aranıyor..."):
                                food_places = get_food_recommendations(plan.get('goal', ''), cuisine, 6)
                            
                            if food_places:
                                st.success(f"✅ {len(food_places)} yemek mekanı bulundu!")
                                
                                # Sonuçları göster
                                cols = st.columns(2)
                                for i, place in enumerate(food_places):
                                    with cols[i % 2]:
                                        # Rating yıldızları
                                        rating = place.get('rating', 0)
                                        stars = "⭐" * int(rating) if rating > 0 else "⭐"
                                        
                                        # Fiyat seviyesi
                                        price_level = place.get('price_level', '')
                                        price_display = "💰" * len(price_level) if price_level else "💰"
                                        
                                        st.markdown(f"""
                                        <div style="background: #fff; border: 2px solid #e0e0e0; border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                                <h4 style="color: #1976d2; margin: 0; font-size: 1.1rem;">{place.get('name', 'İsimsiz')}</h4>
                                                <div style="text-align: right;">
                                                    <div style="color: #ff9800; font-size: 0.9rem;">{stars} {rating:.1f}</div>
                                                    <div style="color: #4caf50; font-size: 0.8rem;">{price_display}</div>
                                                </div>
                                            </div>
                                            
                                            <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">
                                                📍 {place.get('neighborhood', '')} {place.get('city', '')}
                                            </div>
                                            
                                            <div style="color: #424242; font-size: 0.9rem; margin-bottom: 0.5rem;">
                                                🏷️ {place.get('category', '')} • {place.get('cuisine', '')}
                                            </div>
                                            
                                            {f'<div style="color: #666; font-size: 0.8rem; margin-bottom: 0.5rem;">📝 {place.get("description", "")[:100]}...</div>' if place.get('description') else ''}
                                            
                                            <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                                                {f'<a href="{place.get("website", "")}" target="_blank" style="background: #2196f3; color: white; padding: 0.3rem 0.6rem; border-radius: 15px; text-decoration: none; font-size: 0.8rem;">🌐 Site</a>' if place.get('website') else ''}
                                                {f'<span style="background: #4caf50; color: white; padding: 0.3rem 0.6rem; border-radius: 15px; font-size: 0.8rem;">📞 {place.get("phone", "")}</span>' if place.get('phone') else ''}
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                            else:
                                st.warning("❌ Bu konumda yemek mekanı bulunamadı. Farklı bir mutfak türü deneyin.")
                                
                        except ImportError:
                            st.error("❌ Yemek önerisi sistemi yüklenemedi. Lütfen daha sonra tekrar deneyin.")
                        except Exception as e:
                            st.error(f"❌ Arama sırasında hata oluştu: {str(e)}")
            
            # Silme butonu
            if st.session_state.confirming_delete == plan['id']:
                st.warning("Bu seyahat planı kalıcı olarak silinecektir. Emin misiniz?")
                c1, c2, _ = st.columns([1, 1, 4])
                if c1.button("✅ Evet, Sil", key=f"confirm_delete_{plan['id']}", type="primary"):
                    original_plan_index = len(all_plans) - 1 - index
                    all_plans.pop(original_plan_index)
                    save_plans(all_plans)
                    st.session_state.confirming_delete = None
                    st.rerun()
                if c2.button("❌ İptal", key=f"cancel_delete_{plan['id']}"):
                    st.session_state.confirming_delete = None
                    st.rerun()
            else:
                if st.button("🗑️ Seyahat Planını Sil", key=f"delete_{plan['id']}"):
                    st.session_state.confirming_delete = plan['id']
                    st.rerun()