import streamlit as st
from PIL import Image

# Configuración de la página (Título de la pestaña y layout)
st.set_page_config(
    page_title="Portfolio Pablo Giménez",
    page_icon="🚲",
    layout="wide"
)

# --- HEADER (TU PRESENTACIÓN) ---
col1, col2 = st.columns([1, 2])

with col1:
    # Si tienes una foto tuya o un logo, podrías ponerlo aquí.
    # Por ahora usamos un emoji gigante o un placeholder.
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=150)

with col2:
    st.title("Pablo Giménez López")
    st.subheader("Ingeniero & Consultor de Automatización de Datos")
    st.markdown("""
    **Transformo el caos de datos manuales en decisiones estratégicas automáticas.**
    
    Ayudo a empresas y gerentes a eliminar el trabajo repetitivo en Excel mediante 
    Ingeniería de Datos y Aplicaciones Web a medida.
    """)
    
    # Enlaces a redes (pon tus links reales)
    st.markdown("[LinkedIn](https://www.linkedin.com/) | [GitHub](https://github.com/) | [Email](mailto:tu@email.com)")

st.divider()

# --- SECCIÓN DE SERVICIOS / PORTAFOLIO ---
st.header("🛠️ Herramientas & Soluciones")
st.markdown("Explora mis desarrollos seleccionando una opción en el **menú lateral** o haciendo clic abajo:")

# Usamos columnas para crear "Tarjetas" de productos
c1, c2, c3 = st.columns(3)

with c1:
    st.info("📊 **Business Intelligence**")
    st.markdown("### Monitor de Transporte")
    st.markdown("Dashboard interactivo para análisis de flujos de movilidad urbana (STM). Detecta patrones de congestión y uso.")
    st.page_link("pages/01_📊_Analisis_STM.py", label="Ver Demo STM", icon="🚍")

with c2:
    st.success("⚡ **Automatización**")
    st.markdown("### Consolidador de Excel")
    st.markdown("Herramienta que unifica cientos de reportes dispersos en segundos. Ideal para ventas, stock y contabilidad.")
    st.page_link("pages/02_📂_Consolidador_Excel.py", label="Probar Automatización", icon="📂")

st.divider()

# --- FOOTER / CONTACTO RÁPIDO ---
st.markdown("""
### ¿Tienes un Excel que te quita el sueño?
No necesitas contratar un equipo de desarrollo costoso. 
**[Contáctame]** para una consultoría rápida y automaticemos tu problema en menos de 48hs.
""")