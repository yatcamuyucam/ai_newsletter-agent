# 🕵️‍♂️ Kişisel AI Bülten Asistanı (AI Newsletter Agent)

> **"Bilgi kirliliğini otonom ajanlarla aşın. Siz konuyu söyleyin, yapay zeka araştırsın, derlesin ve profesyonel bir bülten olarak sunsun."**

Bu proje, **Multi-Agent (Çoklu Ajan)** mimarisi üzerine kurulu, internetten gerçek zamanlı veri toplayıp analiz eden ve kullanıcıya özel raporlar sunan, **Streamlit** tabanlı bir yapay zeka uygulamasıdır.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/Orchestration-CrewAI-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini%201.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

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

## 🛠️ Karşılaşılan Zorluklar ve Mühendislik Çözümleri (Engineering Journey)

Bu projenin geliştirilme sürecinde performans, maliyet ve donanım kısıtları üzerine yoğun optimizasyonlar yapılmıştır:

### 1. Yerel LLM Kaynak Yönetimi & Halüsinasyon Sorunu
* **Sorun:** Proje ilk olarak yerel modellerle (Local LLM) çalışacak şekilde tasarlandı. `Llama 3.1 (8B)` modeli donanım kaynaklarını (RAM/CPU) tüketti. Daha küçük modeller (`Llama 3.2 1B`, `Qwen 1.5B`) denendiğinde ise "Code-Switching" (Yarı Türkçe, yarı İngilizce konuşma) ve halüsinasyon sorunları yaşandı.
* **Çözüm:** Hibrit yapıya geçildi. Donanım bağımlılığını ortadan kaldırmak için bulut tabanlı modellere yönelindi.

### 2. Rate Limit (Hız Sınırı) Optimizasyonu
* **Sorun:** Groq (Llama 3 70B) entegrasyonunda, ajanların detaylı ve uzun içerik üretmesi istendiğinde `RateLimitError` (Dakikalık Token Sınırı) ile karşılaşıldı.
* **Çözüm:** Model stratejisi değiştirildi. Yüksek hız, geniş bağlam penceresi (Context Window) ve cömert ücretsiz kota sunan **Google Gemini 1.5 Flash** modeline migrasyon yapıldı.

---

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Ön Gereksinimler
* Python 3.10 veya üzeri
* Google AI Studio API Anahtarı (Gemini için)
* Serper.dev API Anahtarı (Google Arama için)

### Adım 1: Repoyu Klonlayın
```bash
git clone [https://github.com/KULLANICI_ADIN/ai-newsletter-agent.git](https://github.com/KULLANICI_ADIN/ai-newsletter-agent.git)
cd ai-newsletter-agent
