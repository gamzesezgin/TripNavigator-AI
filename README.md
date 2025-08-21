# 🚀 Trip Navigator AI - Akıllı Seyahat Planlayıcısı

Yapay Zekâ destekli kişiselleştirilmiş seyahat planlayıcısı. **İki farklı yöntemle** size özel seyahat planları oluşturun:

🤖 **AI Destekli Kişisel Analiz**: Kişilik analizi yaparak tercihlerinizi öğrenir ve size en uygun destinasyonları önerir

📍 **Manuel Konum Belirleme**: İstediğiniz destinasyonu seçin, AI size özel seyahat planı hazırlasın

*Hedefinizi belirtin veya AI'ın sizi tanımasına izin verin - size özel mükemmel seyahat deneyimi için!*

## ✨ Özellikler

### 🎯 Planlama Yöntemleri
- **🤖 AI Destekli Kişisel Analiz**: Kişilik analizi ile size özel seyahat profili
- **📍 Manuel Konum Belirleme**: İstediğiniz destinasyonu doğrudan seçme

### 🌍 Destinasyon ve İçerik
- **Çoklu Destinasyon**: İstanbul, Paris, Roma, Tokyo, New York ve daha fazlası
- **🍽️ Yemek Önerileri**: Popüler restoranlar ve gastronomi noktaları
- **🏛️ Gezilecek Yerler**: Müzeler, tarihi yerler, parklar ve mahalleler

### 🔧 Teknik Özellikler
- **📱 Streamlit Arayüzü**: Kullanıcı dostu web arayüzü
- **🌐 Wikipedia Entegrasyonu**: Otomatik şehir bilgisi çekme
- **🤖 AI Destekli Analiz**: Gemini API ile gelişmiş planlama
- **💾 Plan Kaydetme**: Oluşturulan planları kaydetme ve düzenleme
- **🔄 Fallback Sistemi**: API çalışmazsa yerel verilerle çalışma

## 🛠️ Kurulum

### Gereksinimler

- Python 3.8+
- Google Gemini API anahtarı

### 1. Projeyi Klonlayın

```bash
git clone <repository-url>
cd TripNavigatorAI
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Google Gemini API Anahtarı Alın

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Yeni API anahtarı oluşturun
3. Anahtarı kopyalayın

### 5. API Anahtarlarını Yapılandırın

Proje klasörünüzde `.env` dosyası oluşturun:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

**Önemli:** `.env` dosyasına kendi API anahtarlarınızı girin ve bu dosyayı git'e commit etmeyin.

### 6. Uygulamayı Çalıştırın

```bash
streamlit run _Ana_Sayfa.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde çalışacaktır.

## 📁 Proje Yapısı

```
TripNavigatorAI/
├── _Ana_Sayfa.py              # Ana uygulama dosyası
├── agents/                    # AI ajanları
│   ├── recommender_agent.py   # Yerel öneri sistemi
│   └── wikipedia_agent.py     # Wikipedia veri çekme
├── gemini_handlers/          # Gemini API işleyicileri
│   ├── ai_destination_recommender.py
│   ├── personality_analyzer.py
│   ├── plan_generator.py
│   └── recommendation_generator.py
├── pages/                    # Streamlit sayfaları
│   ├── _Akıllı_Öneriler.py   # AI kişilik analizi
│   ├── _Seyahatlerim.py      # Kayıtlı seyahatler
│   └── _Yeni_Seyahat_Planı.py # Manuel plan oluşturma
├── data_handler.py           # Veri işleme
├── plans.json               # Kayıtlı seyahat planları
├── requirements.txt          # Python bağımlılıkları
└── README.md
```

## 🔧 Teknik Detaylar

### Mimari

- **Frontend**: Streamlit
- **AI Planlama**: Google Gemini API
- **Veri Kaynakları**: Gemini API + Wikipedia API
- **Şehir Bilgileri**: Otomatik Wikipedia entegrasyonu
- **Dil**: Python 3.8+

### Kullanılan Teknolojiler

- **Streamlit**: Web arayüzü
- **Google Gemini API**: AI planlama ve öneriler
- **Wikipedia API**: Şehir bilgileri ve özetler
- **Requests**: HTTP istekleri ve API çağrıları
- **JSON**: Veri saklama ve işleme

## 🚀 Kullanım

### İki Farklı Planlama Yöntemi:

#### 🤖 AI Destekli Kişisel Analiz
1. Kişilik analizi yaparak tercihlerinizi öğrenin
2. AI size özel seyahat profili oluştursun
3. Kişiselleştirilmiş destinasyon önerileri alın
4. Profilinize uygun detaylı seyahat planı oluşturun

#### 📍 Manuel Konum Belirleme
1. İstediğiniz destinasyonu doğrudan seçin
2. Seyahat tercihlerinizi belirtin (bütçe, süre, aktiviteler)
3. AI size özel plan oluştursun
4. Önerileri inceleyin ve kaydedin

### Genel Kullanım Adımları:
- Ana sayfada planlama yönteminizi seçin
- Tercihlerinizi belirtin
- AI size özel seyahat planı oluştursun
- Planınızı kaydedin ve düzenleyin



