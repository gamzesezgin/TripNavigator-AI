# 🚀 Planify - Akıllı Seyahat Planlayıcısı

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
cd Planify
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

### 6. API Anahtarını Yapılandırın

Proje klasörünüzde `.env` dosyası oluşturun:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

**Önemli:** `.env` dosyasına kendi API anahtarınızı girin.

### 7. Uygulamayı Çalıştırın

```bash
streamlit run _Home.py
```

## 🌟 Destinasyonlar

Şu anda desteklenen şehirler:

- **🇹🇷 İstanbul**: Ayasofya, Topkapı Sarayı, Kapalı Çarşı
- **🇫🇷 Paris**: Louvre, Eiffel Kulesi, Montmartre
- **🇮🇹 Roma**: Colosseum, Vatikan Müzeleri, Trevi Çeşmesi
- **🇯🇵 Tokyo**: Senso-ji Tapınağı, Shibuya, Tsukiji Pazarı
- **🇺🇸 New York**: Times Square, Central Park, Empire State

## 📱 Kullanım

### Ana Sayfa
- Destinasyonları keşfedin
- Mevcut şehirlerin özelliklerini görün

### Yeni Plan Oluştur
1. Seyahat hedefinizi yazın (örn: "İstanbul'da 3 günlük kültür turu")
2. Seyahat tarzınızı belirleyin
3. AI size özel plan oluştursun

### Mevcut Planlarım
- Daha önce oluşturduğunuz planları görüntüleyin
- Planları düzenleyin ve güncelleyin

## 🔧 Teknik Detaylar

### Mimari
- **Frontend**: Streamlit
- **AI Planlama**: Google Gemini API
- **Öneriler**: RAG (Retrieval-Augmented Generation) sistemi
- **Veri**: Yerel JSONL corpus

### RAG Sistemi
- Yerel veritabanından akıllı arama
- Şehir bazlı filtreleme
- Kategori bazlı öneriler
- Anahtar kelime eşleştirme

## 🚀 Gelecek Özellikler

- [ ] Daha fazla şehir ekleme
- [ ] Görsel harita entegrasyonu
- [ ] Sosyal medya entegrasyonu
- [ ] Çoklu dil desteği
- [ ] Mobil uygulama

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Sorularınız için issue açın veya [email] adresine yazın.

---

**Not:** Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım için lütfen gerekli izinleri alın.