import streamlit as st
import plotly.graph_objects as go
from data_handler import load_plans, save_plans, get_current_week_tasks, mark_task_completed, unmark_task_completed, get_weekly_stats
from datetime import datetime

st.set_page_config(layout="wide")
st.title("📊 Planlarım ve İlerleme Takibi")

if 'confirming_delete' not in st.session_state:
    st.session_state.confirming_delete = None

all_plans = load_plans()

if not all_plans:
    st.info("Henüz kaydedilmiş bir planınız yok. 'Yeni Plan Oluştur' sayfasından ilk hedefinizi belirleyebilirsiniz!")
else:
    st.markdown("Aşağıda kayıtlı hedeflerinizi ve haftalık ilerleme durumunuzu görebilirsiniz.")
    
    for index, plan in enumerate(reversed(all_plans)):
        st.markdown("---")
        
        # Plan başlığı ve bilgileri
        with st.expander(f"🎯 **Hedef:** {plan['goal']}", expanded=True):
            
            # Plan bilgileri
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.subheader("📋 Tüm Haftalık Görevler")
                
                if plan.get('weekly_tasks'):
                    for week_tasks in plan['weekly_tasks']:
                        st.write(f"**📆 {week_tasks['day']}**")
                        
                        for task_index, task in enumerate(week_tasks['tasks']):
                            # Bu görevin tamamlanıp tamamlanmadığını kontrol et
                            is_completed = False
                            for completed_task in plan.get('completed_tasks', []):
                                if (completed_task.get('day') == week_tasks.get('day') and 
                                    completed_task.get('task_index') == task_index):
                                    is_completed = True
                                    break
                            
                            # Checkbox ile görev durumu
                            checkbox_key = f"task_{plan['id']}_{week_tasks['day']}_{task_index}"
                            checkbox_value = st.checkbox(
                                task,
                                value=is_completed,
                                key=checkbox_key
                            )
                            
                            # Checkbox durumu değiştiğinde işlem yap
                            if checkbox_value != is_completed:
                                if checkbox_value:
                                    # Görevi tamamlandı olarak işaretle
                                    mark_task_completed(plan['id'], week_tasks['day'], task_index)
                                else:
                                    # Görevi tamamlanmamış olarak işaretle
                                    unmark_task_completed(plan['id'], week_tasks['day'], task_index)
                                st.rerun()
                        
                        st.markdown("---")
                else:
                    st.write("Bu plan için görev bulunmuyor.")
            
            with col2:
                st.subheader("📊 Haftalık İlerleme")
                
                # Haftalık istatistikleri hesapla
                stats = get_weekly_stats(plan)
                
                if stats['total_tasks'] > 0:
                    # İlerleme göstergesi
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = stats['progress_percentage'],
                        title = {'text': f"{stats['completed_tasks']} / {stats['total_tasks']} Görev"},
                        delta = {'reference': 0},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#28a745"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{plan['id']}")
                    
                    # Başarı mesajı - Daha motivasyonel ve gerçekçi
                    if stats['progress_percentage'] >= 90:
                        st.success("🏆 Olağanüstü! Haftanın neredeyse tamamını tamamladınız!")
                    elif stats['progress_percentage'] >= 75:
                        st.success("🎉 Harika! Haftanın büyük kısmını tamamladınız!")
                    elif stats['progress_percentage'] >= 60:
                        st.info("👍 Çok iyi gidiyorsunuz! Haftanın yarısından fazlasını tamamladınız!")
                    elif stats['progress_percentage'] >= 40:
                        st.info("💪 İyi başlangıç! Haftanın önemli bir kısmını tamamladınız!")
                    elif stats['progress_percentage'] >= 25:
                        st.info("🌟 Başladınız! Her küçük adım önemli, devam edin!")
                    elif stats['progress_percentage'] >= 10:
                        st.info("🚀 Yolculuğa başladınız! Her görev size yaklaştırıyor!")
                    else:
                        st.info("💫 Hafta yeni başladı! İlk adımları atmaya hazırsınız!")
                else:
                    st.write("Görev bulunmuyor.")
            
            with col3:
                st.subheader("ℹ️ Plan Bilgileri")
                
                # Öğrenme tarzı
                if plan.get('learning_style'):
                    st.write(f"**Öğrenme Tarzı:**")
                    st.info(plan['learning_style'])
                
                # Motivasyon mesajı
                if plan.get('motivation_message'):
                    st.write(f"**💪 Motivasyon:**")
                    st.success(plan['motivation_message'])
                
                # Oluşturulma tarihi
                if plan.get('created_date'):
                    created_date = datetime.fromisoformat(plan['created_date'])
                    st.write(f"**📅 Oluşturulma:** {created_date.strftime('%d.%m.%Y')}")
                
                # Hafta bilgisi
                st.write(f"**📊 Hafta:** {plan.get('current_week', 1)}")
            

            
            # Silme butonu
            if st.session_state.confirming_delete == plan['id']:
                st.warning("Bu plan kalıcı olarak silinecektir. Emin misiniz?")
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
                if st.button("🗑️ Planı Sil", key=f"delete_{plan['id']}"):
                    st.session_state.confirming_delete = plan['id']
                    st.rerun()
