# PlanifyAI - Akıllı Ajanda

PlanifyAI, kullanıcıların büyük hedeflerini yapay zeka yardımıyla yönetilebilir ve eyleme geçirilebilir adımlara bölmelerini sağlayan bir Streamlit uygulamasıdır.

## ✨ Özellikler

- **Yapay Zeka Destekli Planlama:** Doğal dilde girilen bir hedefi, Google Gemini modelini kullanarak mantıksal alt görevlere ayırır.
- **Plan Yönetimi:** Oluşturulan planları kaydeder ve yapılacaklar listesi olarak görüntüler.
- **İlerleme Takibi:** Tamamlanan görevlere göre planın ilerlemesini görsel bir grafikle gösterir.

## 🔧 Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repoyu klonlayın (Bu linki kendi reponuzla güncelleyin):**
    ```bash
    git clone [https://github.com/KULLANICI-ADINIZ/REPO-ADINIZ.git](https://github.com/KULLANICI-ADINIZ/REPO-ADINIZ.git)
    cd REPO-ADINIZ
    ```

2.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **API Anahtarını ayarlayın:**
    - Projenin ana klasöründe `.env` adında bir dosya oluşturun.
    - Dosyanın içine Google AI Studio'dan aldığınız API anahtarınızı aşağıdaki gibi ekleyin:
      ```
      GEMINI_API_KEY="BURAYA_API_ANAHTARINIZI_YAPISTIRIN"
      ```

## 🚀 Kullanım

Kurulum tamamlandıktan sonra, uygulamayı başlatmak için terminalde aşağıdaki komutu çalıştırın:

```bash
streamlit run _Home.py