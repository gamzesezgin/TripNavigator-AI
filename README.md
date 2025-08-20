# 🚀 Trip Navigator AI - Akıllı Seyahat Planlayıcısı

Yapay Zekâ destekli kişiselleştirilmiş seyahat planlayıcısı. Hedefinizi belirtin, AI size özel seyahat planı oluştursun!

## ✨ Özellikler

- 🎯 **Kişiselleştirilmiş Planlama**: Hedefinize göre özel seyahat planları
- 🌍 **Çoklu Destinasyon**: İstanbul, Paris, Roma, Tokyo, New York ve daha fazlası
- 🍽️ **Yemek Önerileri**: Popüler restoranlar ve gastronomi noktaları
- 🏛️ **Gezilecek Yerler**: Müzeler, tarihi yerler, parklar ve mahalleler
- 📱 **Streamlit Arayüzü**: Kullanıcı dostu web arayüzü
- 🔍 **RAG Sistemi**: Yerel veritabanından akıllı öneriler

## 🛠️ Kurulum

### 1. Projeyi Klonlayın

```bash
git clone <repository-url>
cd TripNavigatorAI
```

### 2. Sanal Ortam Oluşturun

```bash
python -m venv venv
```

### 3. Sanal Ortamı Aktifleştirin

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 5. Google Gemini API Anahtarı Alın

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Yeni API anahtarı oluşturun
3. Anahtarı kopyalayın

### 6. API Anahtarlarını Yapılandırın

Proje klasörünüzde `.env` dosyası oluşturun:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
RAPID_API_KEY=YOUR_RAPID_API_KEY
```

**Önemli:** `.env` dosyasına kendi API anahtarlarınızı girin.

#### Google Gemini API Anahtarı:
1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Yeni API anahtarı oluşturun
3. Anahtarı kopyalayın

#### Rapid API Anahtarı:
1. [RapidAPI.com](https://rapidapi.com) adresine gidin
2. Ücretsiz hesap oluşturun
3. İstediğiniz API'yi seçin (Hotels.com, vb.)
4. API anahtarınızı kopyalayın

### 7. Uygulamayı Çalıştırın

```bash
streamlit run _Home.py
```

## 🔧 Teknik Detaylar

### Mimari
- **Frontend**: Streamlit
- **AI Planlama**: Google Gemini API
- **Öneriler**: RAG (Retrieval-Augmented Generation) sistemi
- **Veri**: Yerel JSONL corpus

**Not:** Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım için lütfen gerekli izinleri alın.