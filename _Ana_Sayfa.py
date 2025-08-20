import streamlit as st

st.set_page_config(
    page_title="Trip Navigator AI - Akıllı Seyahat Planlayıcısı",
    page_icon="✈️",
    layout="wide",
)

# CSS stilleri
st.markdown("""
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
    <h1 style="font-size: 3rem; margin-bottom: 1rem;">✈️ Trip Navigator AI'ye Hoş Geldin!</h1>
    <h2 style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">Yapay Zekâ Destekli Kişiselleştirilmiş Seyahat Planlayıcın</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">Hayalindeki seyahati detaylı günlük planlara dönüştüren akıllı asistanın.</p>
    <p style="margin-top: 2rem; font-size: 1.1rem;">🚀 Mükemmel seyahat planını oluşturmaya başlayalım!</p>
</div>
""", unsafe_allow_html=True)

# 2. Nasıl Çalışır Bölümü
st.markdown("---")
st.subheader("🎯 Nasıl Çalışır")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="step-card">
        <h4 style="color: white; margin-bottom: 0.5rem;">Seyahat Hedefini Belirt</h4>
        <p style="color: white;">Nereye gitmek istediğini ve ne yapmak istediğini söyle</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <h4 style="color: white; margin-bottom: 0.5rem;">Seyahat Tarzını Keşfet</h4>
        <p style="color: white;">Birkaç soruyla sana en uygun seyahat planını bulalım</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <h4 style="color: white; margin-bottom: 0.5rem;">Planını Kişiselleştir</h4>
        <p style="color: white;">Her gün için özel olarak hazırlanmış aktiviteler</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="step-card">
        <h4 style="color: white; margin-bottom: 0.5rem;">Seyahatini Takip Et</h4>
        <p style="color: white;">Günlük aktiviteler ve önerileri deneyimle</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Seyahat Planlama Seçenekleri Bölümü
st.markdown("---")
st.subheader("🚀 Seyahat Planlama Seçeneklerin")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3e5151 0%, #77bc74 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;">
        <h3 style="font-size: 1.8rem; margin-bottom: 1rem;"> Kendi Hedefini Belirle</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Nereye gitmek istediğini biliyorsan, hemen seyahat tarzını keşfet ve kişiselleştirilmiş planını oluştur!</p>
        <a href="/_New_Plan" class="cta-button" style="text-decoration: none; display: inline-block; margin-top: 1rem;">🎯 Hedefimi Belirle</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3e5151 0%, #77bc74 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 1rem;">
        <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">🤖 AI Destinasyon Önerisi</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Nereye gideceğini bilmiyorsan, birkaç soruyla sana en uygun destinasyonu önereyim!</p>
        <a href="/_AI_Recommendation" class="cta-button" style="text-decoration: none; display: inline-block; margin-top: 1rem;">🤖 AI Önerisi Al</a>
    </div>
    """, unsafe_allow_html=True)

# 4. Örnek Hedefler Bölümü
st.markdown("---")
st.subheader("💡 Örnek Seyahat Hedefleri")

st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <span class="goal-tag">🏛️ Roma'da 3 günlük kültür turu</span>
    <span class="goal-tag">🏖️ Bali'de 5 günlük tatil</span>
    <span class="goal-tag">🗽 New York'ta 4 günlük şehir turu</span>
    <span class="goal-tag">🏔️ İsviçre'de 7 günlük doğa turu</span>
    <br>
    <span class="goal-tag">🍜 Tokyo'da 6 günlük gastronomi turu</span>
    <span class="goal-tag">🏺 Mısır'da 5 günlük tarih turu</span>
    <span class="goal-tag">🌅 Santorini'de 4 günlük romantik tatil</span>
    <span class="goal-tag">🎨 Paris'te 3 günlük sanat turu</span>
</div>
""", unsafe_allow_html=True)


# Kişilik analizi ve özel öneriler bölümü ana sayfadan kaldırıldı - artık My Plans sayfasında her plan için gösteriliyor