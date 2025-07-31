import streamlit as st

st.set_page_config(
    page_title="PlanifyAI - Akıllı Kişiselleştirilmiş Planlama",
    page_icon="🤖",
    layout="wide",
)

# CSS stilleri
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #2196f3 0%, #4caf50 100%);
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
    }
    
    .goal-tag {
        display: inline-block;
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-weight: bold;
    }
    
    .cta-button {
        background: linear-gradient(45deg, #ff7f0e, #ff6b35);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# 1. Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3rem; margin-bottom: 1rem;">🤖 PlanifyAI'ye Hoş Geldin!</h1>
    <h2 style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">Yapay Zekâ Destekli Kişiselleştirilmiş Planlama Asistanın</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">PlanifyAI, hedeflerini kişiselleştirilmiş günlük görevlere dönüştüren akıllı asistanın.</p>
    <p style="margin-top: 2rem; font-size: 1.1rem;">🚀 Hedeflerine giden yolda ilk adımı atalım!</p>
</div>
""", unsafe_allow_html=True)

# 2. Nasıl Çalışır Bölümü
st.markdown("---")
st.subheader("🎯 Nasıl Çalışır")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="step-card">
        <h3 style="font-size: 2rem; margin-bottom: 1rem;">1️⃣</h3>
        <h4 style="color: white; margin-bottom: 0.5rem;">Hedefini Belirt</h4>
        <p style="color: white;">Ne öğrenmek veya başarmak istediğini söyle</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <h3 style="font-size: 2rem; margin-bottom: 1rem;">2️⃣</h3>
        <h4 style="color: white; margin-bottom: 0.5rem;">Öğrenme Tarzını Keşfet</h4>
        <p style="color: white;">Birkaç soruyla sana en uygun yöntemi bulalım</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <h3 style="font-size: 2rem; margin-bottom: 1rem;">3️⃣</h3>
        <h4 style="color: white; margin-bottom: 0.5rem;">Planını Kişiselleştir</h4>
        <p style="color: white;">Her gün için özel olarak hazırlanmış görevler</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="step-card">
        <h3 style="font-size: 2rem; margin-bottom: 1rem;">4️⃣</h3>
        <h4 style="color: white; margin-bottom: 0.5rem;">İlerlemeni Takip Et</h4>
        <p style="color: white;">Haftalık başarı yüzdeni ve motivasyon mesajları</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Örnek Hedefler Bölümü
st.markdown("---")
st.subheader("💡 Örnek Hedefler")

st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <span class="goal-tag">🌍 İngilizce</span>
    <span class="goal-tag">🧘 Yoga</span>
    <span class="goal-tag">🎸 Gitar</span>
    <span class="goal-tag">🥗 Sağlıklı Beslenme</span>
    <br>
    <span class="goal-tag">📚 Çalışma</span>
    <span class="goal-tag">🏃 Spor</span>
    <span class="goal-tag">🎨 Sanat</span>
    <span class="goal-tag">💰 Tasarruf</span>
</div>
""", unsafe_allow_html=True)

