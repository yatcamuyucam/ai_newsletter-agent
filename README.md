# 🕵️‍♂️ Kişisel AI Bülten Asistanı (AI Newsletter Agent)

> **"Bilgi kirliliğini otonom ajanlarla aşın. Siz konuyu söyleyin, yapay zeka araştırsın, derlesin ve profesyonel bir bülten olarak sunsun."**

Bu proje, **Multi-Agent (Çoklu Ajan)** mimarisi üzerine kurulu, internetten gerçek zamanlı veri toplayıp analiz eden ve kullanıcıya özel raporlar sunan, **Streamlit** tabanlı bir yapay zeka uygulamasıdır.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/Orchestration-CrewAI-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

<img width="1397" height="842" alt="Ekran görüntüsü 2025-11-29 025725" src="https://github.com/user-attachments/assets/c1133d1f-689b-4fd7-8808-60ddf558893d" />
<img width="1896" height="811" alt="Ekran görüntüsü 2025-11-29 025642" src="https://github.com/user-attachments/assets/3fea94e7-679c-4e73-b2a0-582a141f965f" />


## 🏗️ Proje Mimarisi

Sistem, görevleri paylaşan iki otonom ajandan oluşur:

1.  **🕵️‍♂️ Kıdemli Haber Araştırmacısı (The Researcher):**
    * Google Search API (`SerperDevTool`) kullanarak interneti gerçek zamanlı tarar.
    * Konuyla ilgili en güncel 3 gelişmeyi bulur.
    * Haberlerin doğruluğunu ve kaynaklarını (URL) teyit eder.

2.  **✍️ Teknoloji Bülten Editörü (The Writer):**
    * Araştırmacıdan gelen ham verileri analiz eder.
    * Verileri akıcı, edebi ve profesyonel bir İstanbul Türkçesine çevirir.
    * Markdown formatında, okunabilirliği yüksek bir bülten oluşturur.

---

## 🛠️ Karşılaşılan Zorluklar ve Mühendislik Çözümleri

Bu projenin geliştirilme sürecinde performans, maliyet ve donanım kısıtları üzerine yoğun optimizasyonlar yapılmıştır:

### 1. Yerel LLM Kaynak Yönetimi & Halüsinasyon Sorunu
* **Sorun:** Proje ilk olarak yerel modellerle çalışacak şekilde tasarlandı. `Llama 3.1 (8B)` modeli donanım kaynaklarını (RAM/CPU) tüketti. Daha küçük modeller (`Llama 3.2 1B`, `Qwen 1.5B`) denendiğinde ise "Code-Switching" (Yarı Türkçe, yarı İngilizce konuşma) ve halüsinasyon sorunları yaşandı.
* **Çözüm:** Hibrit yapıya geçildi. Donanım bağımlılığını ortadan kaldırmak için bulut tabanlı modellere yönelindi.

### 2. Rate Limit (Hız Sınırı) Optimizasyonu
* **Sorun:** Ajanların detaylı ve uzun içerik üretmesi istendiğinde `RateLimitError` (Dakikalık Token Sınırı) ile karşılaşıldı.
* **Çözüm:** Model stratejisi değiştirildi. Yüksek hız, geniş bağlam penceresi ve cömert ücretsiz kota sunan **Google Gemini 2.5 Flash** modeline geçildi.

---

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Ön Gereksinimler
* Python 3.10 veya üzeri
* Google AI Studio API Anahtarı (Gemini için)
* Serper.dev API Anahtarı (Google Arama için)

1.  **Projeyi Klonlayın:**
    ```bash
    git clone https://github.com/KULLANICI_ADIN/ai-newsletter-agent.git
    cd ai-newsletter-agent
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```bash
    # Sanal ortamı oluştur
    python -m venv venv

    # Windows için aktifleştirme:
    .\venv\Scripts\activate
    
    # macOS/Linux için aktifleştirme:
    # source venv/bin/activate
    ```

3.  **Gerekli Paketleri Yükleyin:**
    `requirements.txt` dosyası ile projenin tüm bağımlılıklarını kurun.
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env Dosyası Oluşturun (Çok Önemli):**
    `app.py` dosyasının çalışabilmesi için Google Gemini ve Serper API anahtarlarını ekleyin. Proje ana dizininde `.env` adında bir dosya oluşturun ve içine kendi anahtarlarınızı aşağıdaki gibi ekleyin:
    ```
    GEMINI_API_KEY="buraya_google_gemini_api_key"
    SERPER_API_KEY="buraya_serper_api_key"
    ```

5.  **Uygulamayı Çalıştırın:**
    Streamlit uygulamasını başlatın:
    ```bash
    streamlit run app.py
    ```
    Uygulama, yerel tarayıcınızda (`http://localhost:8501`) açılacaktır.

6.  **Kullanım:**
    * Araştırmak istediğiniz konuyu yazın ve **Enter** veya "🚀 Araştırmayı Başlat" butonuna basın.
    * Ajanlar otomatik olarak interneti tarayacak, haberleri derleyecek ve Türkçe bir bülten oluşturacaktır.
    * Bülten ekranda görüntülenecek ve Markdown dosyası olarak indirilebilecektir.
    * Haber başlıkları büyük ve okunaklı olarak sunulur, sayfa yenilense bile bülten kaybolmaz (Session State kullanımı).
