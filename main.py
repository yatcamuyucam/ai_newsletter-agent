import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# ==========================================
# 1. SAYFA VE ARAYÜZ YAPILANDIRMASI
# ==========================================
# Streamlit sayfa ayarları: Başlık, ikon ve geniş düzen (wide layout) kullanımı.
st.set_page_config(
    page_title="Kişisel Bülten Asistanı",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# Özel CSS Stilleri: Buton renkleri, input alanları ve arka plan özelleştirmeleri.
st.markdown("""
<style>
    .main { background-color: #f9fafb; }
    .stButton>button { width: 100%; background-color: #4a90e2; color: white; font-weight: bold; }
    .stTextInput>div>div>input { padding: 10px; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# Ana Başlık ve Açıklama
st.title("🕵️‍♂️ Kişisel Araştırma İçin Bülten Ajanı")
st.markdown(
    "Merak ettiğiniz bir konuyu girin, yapay zeka ajanları sizin için araştırıp bülten oluşturacak."
)

# ==========================================
# 2. YAN MENÜ VE GÜVENLİK KONTROLLERİ
# ==========================================
with st.sidebar:
    st.header("⚙️ Sistem Durumu")
    
    # Çevresel değişkenlerin (.env) yüklenmesi
    load_dotenv()
    
    # API Anahtarlarının getirilmesi
    gemini_key = os.getenv("GEMINI_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")

    # Kullanıcıya API bağlantı durumunun gösterilmesi
    st.markdown("### API Bağlantıları")
    st.success("✅ Gemini API: Bağlı" if gemini_key else "❌ Gemini API: Eksik")
    st.success("✅ Serper API: Bağlı" if serper_key else "❌ Serper API: Eksik")
    
    st.markdown("---")
    st.markdown(f"**Kullanılan Model:** gemini-2.5-flash-lite")

# ==========================================
# 3. ÇEKİRDEK FONKSİYON (İŞ MANTIĞI)
# ==========================================
def run_research(topic):
    """
    CrewAI ajanlarını başlatır ve verilen konu üzerinde araştırma yapıp bülten oluşturur.
    Args:
        topic (str): Kullanıcının girdiği araştırma konusu.
    Returns:
        str: Oluşturulan markdown formatındaki bülten metni.
    """
    
    # 3.1. LLM (Büyük Dil Modeli) Yapılandırması
    # Google Gemini 2.5 Flash Lite modeli kullanılıyor.
    # Temperature 0.2 ile halüsinasyon riski azaltıldı.
    gemini_llm = LLM(
        model="gemini/gemini-2.5-flash-lite", 
        api_key=gemini_key,
        temperature=0.2,
        verbose=True
    )
    
    # 3.2. Araçlar (Tools)
    # Google aramaları için SerperDevTool entegrasyonu.
    search_tool = SerperDevTool()
    
    # 3.3. Ajan Tanımlamaları (Agents)
    
    # Araştırmacı Ajan: Veri toplama ve doğrulama uzmanı.
    news_researcher = Agent(
        role='Kıdemli Haber Araştırmacısı',
        goal=f"'{topic}' hakkında en güncel ve gerçek 3 haberi bulmak.",
        verbose=True,
        memory=True,
        backstory="Sen interneti tarayan bir uzmansın...",
        tools=[search_tool],
        llm=gemini_llm,
        allow_delegation=False
    )

    # Editör Ajan: İçerik üretimi ve formatlama uzmanı.
    newsletter_writer = Agent(
        role='Teknoloji Bülten Editörü',
        goal='Haberleri akıcı ve Türkçe sun',
        verbose=True,
        memory=True,
        backstory="Sen ödüllü bir haber yazarısın...",
        tools=[],
        llm=gemini_llm,
        allow_delegation=False
    )

    # 3.4. Görev Tanımlamaları (Tasks)
    
    # Araştırma Görevi: Konuyla ilgili 3 ana başlık ve detay toplama.
    research_task = Task(
        description=f"'{topic}' konusuyla ilgili internetteki en son 3 gelişmeyi bul. Her haber için detaylı bilgi topla.",
        expected_output='3 haberin başlığı, detaylı içeriği ve linklerini içeren rapor.',
        agent=news_researcher
    )

    # Yazma Görevi: Toplanan veriyi markdown formatında bültene çevirme.
    write_task = Task(
        description="Araştırmacıdan gelen raporu kullanarak bir bülten oluştur. Kurallar: 3 haber, --- ile ayrılmış, her haber en az 2 paragraf, kaynak linki.",
        expected_output='Markdown formatında uzun Türkçe bülten.',
        agent=newsletter_writer
    )

    # 3.5. Ekip Kurulumu ve Başlatma (Crew Orchestration)
    # İşlemler sırasıyla (Sequential) yürütülür: Önce araştır, sonra yaz.
    newsletter_crew = Crew(
        agents=[news_researcher, newsletter_writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True
    )

    return newsletter_crew.kickoff(inputs={'topic': topic})

# ==========================================
# 4. KULLANICI ETKİLEŞİMİ VE SONUÇ GÖSTERİMİ
# ==========================================

# Form Yapısı: Enter tuşu ile gönderimi desteklemek için st.form 
with st.form("bulten_form"):
    user_topic = st.text_input(
        "Araştırma Konusu 🔍",
        placeholder="Lütfen bülten konusu girin (Örn: Yapay Zeka, Sinema Endüstrisi...)",
        key="user_topic_form"
    )
    submit_btn = st.form_submit_button("🚀 Araştırmayı Başlat")

# Butona basıldığında çalışacak mantık
if submit_btn:
    # Giriş kontrolü (Validation)
    if not user_topic.strip():
        st.warning("Lütfen bir konu giriniz!")
    else:
        st.info("🤖 Ajanlar göreve başladı. Lütfen bekleyin...")
        
        # İşlem sırasında kullanıcıya geri bildirim (Spinner)
        try:
            with st.spinner("📄 Haberler toplanıyor ve bülten oluşturuluyor..."):
                # Ana fonksiyonu çağır ve sonucu al
                result = run_research(user_topic)
            
            # Session State Kullanımı:
            # Sayfa yeniden yüklendiğinde verilerin kaybolmaması için sonuçları sakla.
            st.session_state['bulten'] = result
            st.session_state['topic'] = user_topic

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

# Sonuçların Ekrana Basılması
# Eğer session_state içinde bülten varsa (daha önce üretilmişse) göster.
if 'bulten' in st.session_state:
    st.success("✨ Bülten hazır!")
    st.subheader(f"📄 {st.session_state.get('topic', 'Bülten')} bülteni❗")
    
    # Markdown formatında içeriği render et
    st.markdown(st.session_state['bulten'])

    # İndirme Butonu: Kullanıcının .md dosyası olarak çıktıyı almasını sağlar.
    st.download_button(
        label="💾 Bülteni İndir (.md)",
        data=str(st.session_state['bulten']),
        file_name=f"{st.session_state.get('topic', 'bulten')}_bulteni.md",
        mime="text/markdown"
    )