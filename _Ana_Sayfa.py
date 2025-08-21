import streamlit as st

st.set_page_config(
    page_title="Trip Navigator AI - Akıllı Seyahat Planlayıcısı",
    page_icon="✈️",
    layout="wide",
)

# CSS stilleri
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
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
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .goal-tag {
        display: inline-block;
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .goal-tag:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .cta-button {
        background: linear-gradient(45deg, #ff7f0e, #ff6b35);
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .planning-card {
        background: linear-gradient(135deg, #3e5151 0%, #77bc74 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .planning-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .icon {
        width: 24px;
        height: 24px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 8px;
        filter: brightness(0) invert(1);
    }
    
    .icon-large {
        width: 48px;
        height: 48px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 12px;
        filter: brightness(0) invert(1);
    }
    
    .floating-animation {
        animation: float 3s ease-in-out infinite;
        margin-right: 15px;
        font-size: 3rem;
    }
    
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }
</style>
""", unsafe_allow_html=True)

# 1. Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3.5rem; margin-bottom: 1.5rem; font-weight: 700;">
        <i class="fas fa-plane-departure floating-animation"></i> Trip Navigator AI
    </h1>
    <h2 style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">Yapay Zekâ Destekli Kişiselleştirilmiş Seyahat Planlayıcın</h2>
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">Hayalindeki seyahati detaylı günlük planlara dönüştüren akıllı asistanın.</p>
    <p style="margin-top: 2rem; font-size: 1.1rem;">
        <i class="fas fa-rocket" style="margin-right: 8px; font-size: 1.2rem;"></i>
        Mükemmel seyahat planını oluşturmaya başlayalım!
    </p>
</div>
""", unsafe_allow_html=True)

# 2. Nasıl Çalışır Bölümü
st.markdown("---")
st.markdown("""
<h3 style="display: flex; align-items: center;">
    <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z"/>
    </svg>
    Nasıl Çalışır
</h3>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="step-card">
        <i class="fas fa-map-marker-alt step-icon"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Seyahat Hedefini Belirt</h4>
        <p style="color: white;">Nereye gitmek istediğini veya ne yapmak istediğini söyle</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <i class="fas fa-search step-icon"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Seyahat Tarzını Keşfet</h4>
        <p style="color: white;">Birkaç soruyla sana en uygun seyahat planını bulalım</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <i class="fas fa-cog step-icon"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Planını Kişiselleştir</h4>
        <p style="color: white;">Her gün için özel olarak hazırlanmış aktiviteler</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="step-card">
        <i class="fas fa-check-circle step-icon"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Seyahatini Takip Et</h4>
        <p style="color: white;">Günlük aktiviteler ve önerileri deneyimle</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Seyahat Planlama Seçenekleri Bölümü
st.markdown("---")
st.markdown("""
<h3 style="display: flex; align-items: center;">
    <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M13,2.05V4.05C17.39,4.59 20.5,8.58 19.96,12.97C19.5,16.61 16.64,19.5 13,19.93V21.93C18.5,21.38 22.5,16.5 21.95,11C21.5,6.25 17.73,2.5 13,2.03V2.05M5.67,19.74C7.18,21 9.04,21.79 11,22V20C9.58,19.82 8.23,19.25 7.1,18.37L5.67,19.74M7.1,5.74C8.22,4.84 9.57,4.26 11,4.06V2.06C9.05,2.25 7.19,3 5.67,4.26L7.1,5.74M5.69,7.1L4.26,5.67C3,7.19 2.25,9.04 2.05,11H4.05C4.24,9.58 4.8,8.23 5.69,7.1M4.06,13H2.06C2.26,14.96 3.03,16.81 4.27,18.33L5.69,16.9C4.81,15.77 4.24,14.42 4.06,13M10,16.5L16,14L16.5,15.5L14,16.5L10,16.5M16,12.5L10,10.5L9.5,12L12,13L16,12.5M16,9.5L10,7.5L9.5,9L12,10L16,9.5M16,6.5L10,4.5L9.5,6L12,7L16,6.5M16,3.5L10,1.5L9.5,3L12,4L16,3.5"/>
    </svg>
    Seyahat Planlama Seçeneklerin
</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="planning-card">
        <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">Kendi Hedefini Belirle</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Nereye gitmek istediğini biliyorsan, hemen seyahat tarzını keşfet ve kişiselleştirilmiş planını oluştur!</p>
        <a href="/_New_Plan" class="cta-button" style="text-decoration: none; display: inline-block; margin-top: 1rem;"> Plan Oluştur</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="planning-card">
        <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M7.5,13A2.5,2.5 0 0,0 5,15.5A2.5,2.5 0 0,0 7.5,18A2.5,2.5 0 0,0 10,15.5A2.5,2.5 0 0,0 7.5,13M16.5,13A2.5,2.5 0 0,0 14,15.5A2.5,2.5 0 0,0 16.5,18A2.5,2.5 0 0,0 19,15.5A2.5,2.5 0 0,0 16.5,13Z"/>
            </svg>
            AI Destinasyon Önerisi
        </h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Nereye gideceğini bilmiyorsan, birkaç soruyla sana en uygun destinasyonu önereyim!</p>
        <a href="/_AI_Recommendation" class="cta-button" style="text-decoration: none; display: inline-block; margin-top: 1rem;">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
                <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M7.5,13A2.5,2.5 0 0,0 5,15.5A2.5,2.5 0 0,0 7.5,18A2.5,2.5 0 0,0 10,15.5A2.5,2.5 0 0,0 7.5,13M16.5,13A2.5,2.5 0 0,0 14,15.5A2.5,2.5 0 0,0 16.5,18A2.5,2.5 0 0,0 19,15.5A2.5,2.5 0 0,0 16.5,13Z"/>
            </svg>
            AI Önerisi Al
        </a>
    </div>
    """, unsafe_allow_html=True)

# 4. Örnek Hedefler Bölümü
st.markdown("---")
st.markdown("""
<h3 style="display: flex; align-items: center;">
    <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"/>
    </svg>
    Örnek Seyahat Hedefleri
</h3>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M12,2L2,7V10H4V19L6,18V10H8V19L10,18V10H12V19L14,18V10H16V19L18,18V10H20V7L12,2M12,4.5L18,7.5V8H6V7.5L12,4.5Z"/>
        </svg>
        Roma'da 3 günlük kültür turu
    </span>
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M12,2C13.1,2 14,2.9 14,4C14,5.1 13.1,6 12,6C10.9,6 10,5.1 10,4C10,2.9 10.9,2 12,2M21,9V7L15,1H5C3.89,1 3,1.89 3,3V21A2,2 0 0,0 5,23H19A2,2 0 0,0 21,21V9M19,9H14V4H5V21H19V9Z"/>
        </svg>
        Bali'de 5 günlük tatil
    </span>
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M12,2C13.1,2 14,2.9 14,4C14,5.1 13.1,6 12,6C10.9,6 10,5.1 10,4C10,2.9 10.9,2 12,2M21,9V7L15,1H5C3.89,1 3,1.89 3,3V21A2,2 0 0,0 5,23H19A2,2 0 0,0 21,21V9M19,9H14V4H5V21H19V9Z"/>
        </svg>
        New York'ta 4 günlük şehir turu
    </span>
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M14,6L15.25,7.25L16.59,5.91L18,7.33L16.66,8.67L18,10L16.59,11.41L15.25,10.08L14,11.33L12.75,10.08L11.41,11.41L10,10L11.34,8.67L10,7.33L11.41,5.91L12.75,7.25L14,6M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z"/>
        </svg>
        İsviçre'de 7 günlük doğa turu
    </span>
    <br>
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
        </svg>
        Tokyo'da 6 günlük gastronomi turu
    </span>
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M12,2L2,7V10H4V19L6,18V10H8V19L10,18V10H12V19L14,18V10H16V19L18,18V10H20V7L12,2M12,4.5L18,7.5V8H6V7.5L12,4.5Z"/>
        </svg>
        Mısır'da 5 günlük tarih turu
    </span>
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,2L14.39,5.42C13.65,5.15 12.84,5 12,5C11.16,5 10.35,5.15 9.61,5.42L12,2M3.34,7L7.5,6.65C6.9,7.16 6.36,7.78 5.94,8.5L3.34,7M3.36,17L5.94,15.5C6.36,16.22 6.9,16.84 7.5,17.35L3.36,17M20.65,7L18.06,8.5C17.64,7.78 17.1,7.16 16.5,6.65L20.65,7M20.64,17L16.5,17.35C17.1,16.84 17.64,16.22 18.06,15.5L20.64,17M12,22L9.59,18.56C10.33,18.83 11.14,19 12,19C12.82,19 13.63,18.83 14.37,18.56L12,22Z"/>
        </svg>
        Santorini'de 4 günlük romantik tatil
    </span>
    <span class="goal-tag">
        <svg class="icon" viewBox="0 0 24 24" fill="currentColor" style="width: 16px; height: 16px; margin-right: 4px;">
            <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/>
        </svg>
        Paris'te 3 günlük sanat turu
    </span>
</div>
""", unsafe_allow_html=True)


# Kişilik analizi ve özel öneriler bölümü ana sayfadan kaldırıldı - artık My Plans sayfasında her plan için gösteriliyor