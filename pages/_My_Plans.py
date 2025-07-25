import streamlit as st
import plotly.graph_objects as go
from data_handler import load_plans, save_plans

st.set_page_config(layout="wide")
st.title("📊 Kayıtlı Planların ve İlerlemen")

if 'confirming_delete' not in st.session_state:
    st.session_state.confirming_delete = None

all_plans = load_plans()

if not all_plans:
    st.info("Henüz kaydedilmiş bir planınız yok. 'Yeni Plan Oluştur' sayfasından ilk hedefinizi belirleyebilirsiniz!")
else:
    st.markdown("Aşağıda kayıtlı hedeflerinizi ve ilerleme durumunuzu görebilirsiniz.")
    
    for index, plan in enumerate(reversed(all_plans)):
        st.markdown("---")
        with st.expander(f"🎯 **Hedef:** {plan['goal']}", expanded=True):
            
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("Yapılacaklar Listesi")
                if not plan.get('tasks'):
                    st.write("Bu hedef için görev bulunmuyor.")
                else:
                    for task_index, task in enumerate(plan['tasks']):
                        new_status = st.checkbox(
                            task['description'], 
                            value=task['completed'], 
                            key=f"task_{plan['id']}_{task_index}"
                        )
                        if new_status != task['completed']:
                            original_plan_index = len(all_plans) - 1 - index
                            all_plans[original_plan_index]['tasks'][task_index]['completed'] = new_status
                            save_plans(all_plans)
                            st.rerun()

            with col2:
                st.subheader("İlerleme Durumu")
                completed_count = sum(1 for task in plan.get('tasks', []) if task['completed'])
                total_count = len(plan.get('tasks', []))
                
                if total_count > 0:
                    progress_percent = (completed_count / total_count) * 100
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number", value = progress_percent,
                        title = {'text': f"{completed_count} / {total_count} Görev Tamamlandı"},
                        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#28a745"}}
                    ))
                    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
                    
                    # --- HATA DÜZELTMESİ BURADA ---
                    # Her grafiğe, planın ID'sini kullanarak benzersiz bir anahtar (key) ekledik.
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{plan['id']}")
                    # --- DÜZELTME SONU ---
                    
                else:
                    st.write("Görev yok.")

            # Silme Butonu Mantığı
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
