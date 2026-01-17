import streamlit as st
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="PDGL: Soluciones de Datos",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Para darle un toque 'Pro') ---
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 25px;
        color: #FF4B4B;
    }
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (TU PERFIL PROFESIONAL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=120) # Tu bici
    st.title("Pablo Giménez López")
    st.caption("Ingeniero en Computación | PM | Data Enthusiast")
    
    st.markdown("---")
    
    st.markdown("📍 **Ubicación:** Uruguay 🇺🇾")
    st.markdown("🎓 **Educación:** FING / Udelar")
    st.markdown("📧 **Contacto:** [Email](mailto:tu@email.com)")
    st.markdown("🔗 **LinkedIn:** [Ver Perfil](https://www.linkedin.com/)")
    
    st.markdown("---")
    st.write("© 2026 PGL Soluciones")

# --- CUERPO PRINCIPAL ---

# 1. HEADER CON IMPACTO
st.title("🚲 Transformando Datos en Decisiones")
st.markdown("""
**Ayudo a gerentes y empresas a dejar de perder tiempo en tareas manuales.** Desarrollo herramientas de automatización y análisis que convierten planillas de Excel caóticas en tableros de control inteligentes.
""")

# 2. MÉTRICAS (Simuladas para mostrar valor)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Horas Ahorradas/Mes", "+120 h", "Automatización")
c2.metric("Precisión de Datos", "99.9%", "Sin error humano")
c3.metric("Reportes Generados", "Automático", "Tiempo Real")
c4.metric("Tecnología", "Python", "v3.12")

st.divider()

# 3. PORTAFOLIO DE SOLUCIONES (Tus Apps)
st.subheader("🛠️ Mis Herramientas")

col1, col2, col3 = st.columns(3)

with col1:
    st.container(border=True)
    st.markdown("### 🚍 Monitor STM")
    st.write("Análisis de movilidad urbana en Montevideo. Visualiza patrones de viaje, tiempos y rutas frecuentes.")
    st.progress(90, text="Estado: Producción")
    st.page_link("pages/01_📊_Analisis_STM.py", label="Ver Dashboard", icon="📊")

with col2:
    st.container(border=True)
    st.markdown("### 📂 Consolidador Pro")
    st.write("Olvídate de 'copiar y pegar'. Une cientos de archivos Excel con formatos distintos en segundos.")
    st.progress(100, text="Estado: Listo para usar")
    st.page_link("pages/02_📂_Consolidador_Excel.py", label="Unificar Excels", icon="⚡")


st.divider()

# 4. TECH STACK (Autoridad Técnica)
st.subheader("💻 Stack Tecnológico")
st.markdown("No uso macros de Excel. Uso ingeniería de software moderna:")

# Usamos columnas pequeñas para iconos
t1, t2, t3, t4, t5, t6 = st.columns(6)
t1.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=40, caption="Python")
t2.image("https://upload.wikimedia.org/wikipedia/commons/2/22/Pandas_mark.svg", width=40, caption="Pandas")
t3.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=40, caption="Streamlit")
t4.image("https://images.plot.ly/logo/new-branding/plotly-logomark.png", width=40, caption="Plotly")
t5.image("https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg", width=40, caption="Notion")
t6.image("https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png", width=40, caption="Git")

# 5. LLAMADA A LA ACCIÓN (CTA) FINAL
st.info("""
💡 **¿Tienes un proceso manual que te quita el sueño?**
Escríbeme y agendemos una llamada de 15 minutos para ver si se puede automatizar.
""")