import streamlit as st
from data_handler import load_plans, save_plans, get_current_week_tasks, mark_task_completed, unmark_task_completed
from datetime import datetime
from agents.recommender_agent import recommend_pois
from agents.wikipedia_agent import get_city_wikipedia_info

st.set_page_config(layout="wide", page_title="Seyahatlerim - TripNavigatorAI")

# Ana sayfadaki turuncudan maviye gradient kullanan CSS stilleri
st.markdown("""
<style>
    .travel-header {
        background: linear-gradient(45deg, #ff7f0e, #1f77b4);
        padding: 0.6rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: white;
        text-align: left;
    }
    
    .section-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    
    .day-section {
        background: white;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
    .city-info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #bbdefb;
    }
    
    .info-highlight {
        background: #fff3cd;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 3px solid #ffc107;
    }
    
    .delete-alert {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .main-title {
        background: linear-gradient(45deg, #ff7f0e, #1f77b4);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(255, 127, 14, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık - ana sayfadaki turuncudan maviye gradient kullanarak
st.markdown("""
<div class="main-title">
    <h1 style="margin: 0; font-size: 2.2rem;">✨ Seyahat Planlarım ve Aktivite Takibi</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Seyahatlerinizi yönetin ve aktivitelerinizi takip edin</p>
</div>
""", unsafe_allow_html=True)

if 'confirming_delete' not in st.session_state:
    st.session_state.confirming_delete = None

all_plans = load_plans()

if not all_plans:
    st.info("Henüz kaydedilmiş bir seyahat planınız yok. 'Yeni Seyahat Planı Oluştur' sayfasından ilk seyahatinizi planlayabilirsiniz!")
else:
    st.markdown("Aşağıda kayıtlı seyahat planlarınızı ve günlük aktivite durumunuzu görebilirsiniz.")
    
    for index, plan in enumerate(reversed(all_plans)):
        st.markdown("---")
        
        # Seyahat başlığı - beyaz container olmadan
        st.markdown(f"""
        <div class="travel-header">
            <h2 style="margin: 0; color: white; font-size: 1.3rem;">📌 {plan['goal']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Plan içeriği
        with st.expander(f"📋 Detayları Görüntüle", expanded=False):
            
            # Plan bilgileri
            col1, col2 = st.columns([2, 2])
            
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
                st.subheader("🏛️ Şehir Bilgileri")

                # Wikipedia'dan şehir bilgilerini al
                city_name = plan.get('goal', '')
                with st.spinner("Şehir bilgileri Wikipedia'dan alınıyor..."):
                    try:
                        city_info = get_city_wikipedia_info(city_name)
                    except Exception as e:
                        st.error(f"Şehir bilgileri alınamadı: {e}")
                        city_info = None

                if city_info:
                    st.success(f"✅ {city_info['source']} kaynağından bilgiler alındı!")
                    
                    # Şehir bilgilerini göster
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #5da35a 100%); 
                               padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
                        <h3 style="color: white; margin-bottom: 1rem;">🏛️ {city_info['title']}</h3>
                        <p style="color: white; font-size: 1rem; line-height: 1.6;">{city_info['summary']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Öne çıkan yerler
                    if city_info.get('highlights'):
                        st.markdown("**🌟 Öne Çıkan Yerler:**")
                        st.info(city_info['highlights'])
                    
                    # Koordinatlar varsa göster
                    if city_info.get('latitude') and city_info.get('longitude'):
                        st.markdown(f"**📍 Koordinatlar:** {city_info['latitude']:.4f}, {city_info['longitude']:.4f}")
                    
                    # Wikipedia linki
                    if city_info.get('wikipedia_url'):
                        st.markdown(f"**📚 Daha fazla bilgi:** [Wikipedia'da {city_info['title']}]({city_info['wikipedia_url']})")
                else:
                    st.warning("❌ Şehir bilgileri alınamadı.")
            
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