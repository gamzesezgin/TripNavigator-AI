# <Trip Navigator AI> - Akıllı Seyahat Planlayıcısı

Trip Navigator AI, kullanıcıların seyahat hedeflerini yapay zeka yardımıyla yönetilebilir ve eyleme geçirilebilir günlük aktivitelere dönüştürmelerini sağlayan bir Streamlit uygulamasıdır.

## ✨ Özellikler

- **Yapay Zeka Destekli Seyahat Planlama:** Doğal dilde girilen seyahat hedefini, Google Gemini modelini kullanarak mantıksal günlük aktivitelere ayırır.
- **Seyahat Planı Yönetimi:** Oluşturulan seyahat planlarını kaydeder ve aktivite listesi olarak görüntüler.
- **Aktivite Takibi:** Tamamlanan aktivitelere göre seyahat planının ilerlemesini görsel bir grafikle gösterir.
- **Haftalık Program:** O hafta tamamlanması gereken aktiviteleri ayrı bir sekmede gösterir.

## 🚀 Kurulum ve Çalıştırma

### 1. Projeyi İndirin

```bash
git clone https://github.com/KULLANICI-ADINIZ/REPO-ADINIZ.git
cd REPO-ADINIZ
```

### 2. Python Sanal Ortamı Oluşturun

```bash
# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktif edin
# Windows için:
venv\Scripts\activate
# macOS/Linux için:
source venv/bin/activate
```

### 3. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Google Gemini API Anahtarı Alın

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşturulan API anahtarını kopyalayın

### 5. API Anahtarını Yapılandırın

Proje klasörünüzde `.env` dosyası oluşturun:

**Önemli:** `.env` dosyasına  kendi API anahtarınızı girin.

### 6. Uygulamayı Çalıştırın

```bash
streamlit run _Home.py
```

## 📁 Proje Yapısı

```
Planify/
├── _Home.py              # Ana uygulama dosyası
├── data_handler.py       # Veri yönetimi
├── gemini_handler.py     # Gemini API entegrasyonu
├── pages/
│   ├── _My_Plans.py     # Planlarım sayfası
│   └── _New_Plan.py     # Yeni plan oluşturma
├── requirements.txt      # Python bağımlılıkları
└── README.md           # Bu dosya
```