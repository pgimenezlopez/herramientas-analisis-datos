import streamlit as st
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="PGL Centro de Soluciones",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS VISUALES (CSS) ---
st.markdown("""
<style>
    /* Títulos y fuentes */
    h1 {color: #0F172A; font-family: 'Helvetica Neue', sans-serif; font-weight: 800;}
    h3 {color: #334155;}
    
    /* Tarjetas de los módulos */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Botones destacados */
    .stButton button {
        background-color: #2563EB;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
col1, col2 = st.columns([1, 8])
with col1:
    # Logo conceptual (engranaje/tecnología)
    st.image("https://cdn-icons-png.flaticon.com/512/8637/8637106.png", width=90)
with col2:
    st.title("PGL Centro de Soluciones")
    st.caption("INGENIERÍA DE DATOS & AUTOMATIZACIÓN DE PROCESOS | PABLO GIMÉNEZ")

st.markdown("---")

st.info("💡 **Bienvenido.** Selecciona un módulo para iniciar una solución automatizada.")

# --- GRID DE MÓDULOS ---
st.subheader("🚀 Catálogo de Soluciones")

c1, c2, c3 = st.columns(3)

# Altura total de la tarjeta
altura_tarjeta = 280

# Estilo para fijar la altura del texto (aprox 3 a 4 lineas)
estilo_texto = "height: 70px; display: flex; align-items: center;"

# MÓDULO 1: TRANSPORTE
with c1:
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 📊 Monitor STM")
        # Usamos HTML para fijar la altura del texto a 70px siempre
        st.markdown(f'<div style="{estilo_texto}">Análisis de movilidad urbana y detección de patrones de transporte.</div>', unsafe_allow_html=True)
        st.progress(100, "Versión 1.0")
        st.write("") 
        if st.button("Abrir Monitor ↗️", key="btn_stm", use_container_width=True):
            st.switch_page("pages/01_📊_Analisis_STM.py")

# MÓDULO 2: EXCEL
with c2:
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 📂 Consolidador Excel")
        # El div invisible ocupa el mismo espacio aunque el texto sea mas corto
        st.markdown(f'<div style="{estilo_texto}">Unificación automática de múltiples reportes financieros y logísticos.</div>', unsafe_allow_html=True)
        st.progress(100, "Versión 2.1")
        st.write("")
        if st.button("Abrir Consolidador ↗️", key="btn_excel", use_container_width=True):
            st.switch_page("pages/02_📂_Consolidador_Excel.py")

# MÓDULO 3: VETERINARIA
with c3:
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 🐾 Gestión Veterinaria")
        st.markdown(f'<div style="{estilo_texto}">Sistema de alertas de vacunación y retención de clientes.</div>', unsafe_allow_html=True)
        st.progress(90, "Versión MVP")
        st.write("")
        if st.button("Abrir Alertas ↗️", key="btn_vet", use_container_width=True):
            st.switch_page("pages/03_🐶_Gestor_Vacunas.py")

# MÓDULO 4: COACHING
with c1:
   with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 🧘 Gestión de Pacientes")
        # Descripción con altura fija
        st.markdown(f'<div style="{estilo_texto}">Plataforma de seguimiento de pacientes, historial clínico y métricas.</div>', unsafe_allow_html=True)
        st.progress(90, "Versión MVP")
        st.write("")
        
        # AQUÍ ESTABA EL ERROR: Ahora está limpio
        if st.button("Abrir Suite ↗️", key="btn_coaching", use_container_width=True):
            st.switch_page("pages/04_🧘_Gestion_de_Pacientes.py")

# MÓDULO 5: ESTÉTICA MÓVIL
with c2:
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 📍 Estética Móvil")
        st.markdown(f'<div style="{estilo_texto}">Optimización de rutas y fichas de clientes para servicios a domicilio.</div>', unsafe_allow_html=True)
        st.progress(15, "En Diseño")
        st.write("")
        
        # AQUÍ ESTÁ EL CAMBIO:
        if st.button("Abrir Rutas ↗️", key="btn_estetica", use_container_width=True):
            st.switch_page("pages/05_📍_Estetica_Movil.py")