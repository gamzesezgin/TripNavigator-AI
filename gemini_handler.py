import streamlit as st
import json
import requests

def generate_plan_with_gemini(goal, api_key):
    """
    Kullanıcının isteği doğrultusunda güncellenmiş prompt'u kullanarak
    Gemini API'sinden bir eylem planı oluşturur. Bu, projenin son,
    temizlenmiş versiyonudur.
    """
    if not api_key:
        st.error("API anahtarı bulunamadı. Lütfen .env dosyasını ve kodunuzu kontrol edin.")
        return None
    
    prompt = f"""
Kullanıcının belirttiği hedef: "{goal}"

Bu hedefi detaylı şekilde analiz et. Hedefin ne tür bir hedef olduğunu (örneğin akademik, kariyer, sağlık, kişisel gelişim vb.) anlamaya çalış ve buna uygun bir planlama yap.

Daha sonra bu hedefe ulaşmak için atılması gereken adımları mantıksal sıraya göre "alt görevler" olarak böl. Her bir görevin:
- Net, yapılabilir ve sonuç odaklı olması,
- Kullanıcının seviyesine uygun ve motive edici olması,
- Zamanlama açısından makul büyüklükte olması beklenmektedir.

Cevabın SADECE aşağıdaki formatta bir JSON objesi olmalıdır:
{{
  "tasks": [
    "Alt görev 1",
    "Alt görev 2",
    "...",
    "Alt görev N"
  ]
}}
"""
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    payload = {
      "contents": [{"parts": [{"text": prompt}]}],
      "generationConfig": {
        "responseMimeType": "application/json",
        "temperature": 0.5,
        "maxOutputTokens": 2048,
      }
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        # Yavaş bağlantılar için bekleme süresi 90 saniye olarak ayarlandı.
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=90)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            return json.loads(content)
        else:
            st.error("API'den beklenen formatda bir cevap alınamadı. Lütfen tekrar deneyin.")
            return None
            
    except requests.exceptions.Timeout:
        st.error("API'den cevap alınamadı (Zaman aşımı). Lütfen internet bağlantınızı kontrol edin veya daha sonra tekrar deneyin.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API isteği sırasında bir ağ hatası oluştu: {e}")
        return None
    except json.JSONDecodeError:
        st.error("API'den gelen cevap JSON formatında değil. Modelin çıktısı beklenmedik olabilir.")
        return None
    except Exception as e:
        st.error(f"Beklenmedik bir hata oluştu: {e}")
        return None