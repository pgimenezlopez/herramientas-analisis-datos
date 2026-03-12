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

altura_tarjeta = 270
estilo_texto = "height: 60px; display: flex; align-items: center;"

# Definimos 3 columnas para la fila 1
c1, c2, c3 = st.columns(3)

# --- FILA 1 ---

with c1: # TRANSPORTE
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 📊 Monitor STM")
        st.markdown(f'<div style="{estilo_texto}">Análisis de movilidad urbana y patrones.</div>', unsafe_allow_html=True)
        st.progress(100, "Versión 1.0")
        if st.button("Abrir Monitor ↗️", key="btn_stm", use_container_width=True):
            st.switch_page("pages/01_📊_Analisis_STM.py")

with c2: # EXCEL
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 📂 Consolidador")
        st.markdown(f'<div style="{estilo_texto}">Unificación de reportes financieros.</div>', unsafe_allow_html=True)
        st.progress(100, "Versión 2.1")
        if st.button("Abrir Excel ↗️", key="btn_excel", use_container_width=True):
            st.switch_page("pages/02_📂_Consolidador_Excel.py")

with c3: # VETERINARIA
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 🐾 Gestión Vet")
        st.markdown(f'<div style="{estilo_texto}">Alertas de vacunas y CRM.</div>', unsafe_allow_html=True)
        st.progress(90, "Versión MVP")
        if st.button("Abrir Vet ↗️", key="btn_vet", use_container_width=True):
            st.switch_page("pages/04_🐶_Gestor_Vacunas.py")

st.write("") # Separador visual

# --- FILA 2 ---
c4, c5, c6 = st.columns(3)

with c4: # COACHING
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 🧘 Plataforma Salud")
        st.markdown(f'<div style="{estilo_texto}">Seguimiento de pacientes y métricas.</div>', unsafe_allow_html=True)
        st.progress(90, "Versión MVP")
        if st.button("Abrir Salud ↗️", key="btn_coaching", use_container_width=True):
            st.switch_page("pages/04_🧘_Gestion_de_Pacientes.py")

with c5: # ESTÉTICA (AGENDA)
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 📍 Estética Móvil")
        st.markdown(f'<div style="{estilo_texto}">Agenda inteligente y turnos.</div>', unsafe_allow_html=True)
        st.progress(100, "Versión Pro")
        if st.button("Abrir Agenda ↗️", key="btn_estetica", use_container_width=True):
            st.switch_page("pages/05_📍_Estetica_Movil.py")

with c6: # LOGÍSTICA (NUEVO)
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 🚚 Logística Pyme")
        st.markdown(f'<div style="{estilo_texto}">Rutas de reparto y control de chofer.</div>', unsafe_allow_html=True)
        st.progress(80, "Nuevo Módulo")
        # Este botón abre el archivo 06 que acabamos de crear
        if st.button("Abrir Reparto ↗️", key="btn_logistica", use_container_width=True):
            st.switch_page("pages/06_🚚_Logistica_Reparto.py")

# --- FILA 3 ---
c7, c8, c9 = st.columns(3)

with c7: # INFORME CLÍNICO IA (NUEVO)
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 🩺 Informe IA")
        st.markdown(f'<div style="{estilo_texto}">Generador clínico asistido por Gemini.</div>', unsafe_allow_html=True)
        
        # Le ponemos 100% o el valor que prefieras para destacar que es IA
        st.progress(100, "Módulo IA Activo") 
        
        # Botón con key única para evitar conflictos en Streamlit
        if st.button("Abrir Generador ↗️", key="btn_informe_ia", use_container_width=True):
            st.switch_page("pages/07_🩺_Informe_Psico.py")

with c8: # VIANDAS
    with st.container(height=altura_tarjeta, border=True):
        st.markdown("### 🍱 Pedidos Viandas")
        st.markdown(f'<div style="{estilo_texto}">Menú digital interactivo y carrito.</div>', unsafe_allow_html=True)
        # Le ponemos 33% de progreso porque es la Fase 1 de 3
        st.progress(33, "Fase 1: MVP") 
        if st.button("Abrir Viandas ↗️", key="btn_viandas", use_container_width=True):
            st.switch_page("pages/08_🍱_Viandas_App.py")