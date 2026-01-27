import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Vet Alert System", page_icon="🐾", layout="wide")

st.title("🐾 Sistema de Alertas Veterinarias")
st.markdown("""
**Problema:** Pérdida de clientes por olvido de fechas de vacunación.
**Solución:** Automatización del cálculo de fechas y generación de recordatorios.
""")

# --- PESTAÑAS DEL SISTEMA ---
tab1, tab2 = st.tabs(["📝 Nuevo Registro", "📅 Próximos Vencimientos"])

# --- PESTAÑA 1: REGISTRAR PACIENTE ---
with tab1:
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("Datos del Paciente")
        dueno = st.text_input("Nombre del Dueño", placeholder="Ej: Juan Pérez")
        email = st.text_input("Contacto (Email/Tel)", placeholder="juan@email.com")
        mascota = st.text_input("Nombre Mascota", placeholder="Ej: Luna, Thor, Max")
    
    with col_der:
        st.subheader("Datos Clínicos")
        vacuna = st.selectbox("Tipo de Vacuna", ["Quíntuple", "Sextuple", "Antirrábica", "Tos de las Perreras"])
        fecha_aplicacion = st.date_input("Fecha de Aplicación", date.today())
        
        # Lógica de Negocio: Calcular vencimiento automático (1 año después)
        fecha_vencimiento = fecha_aplicacion + timedelta(days=365)
        st.metric("Próximo Vencimiento (Calculado)", fecha_vencimiento.strftime("%d/%m/%Y"))

    # Botón de Guardar (Simulado)
    if st.button("Guardar Registro", type="primary"):
        if dueno and mascota:
            st.success(f"✅ Paciente {mascota} registrado exitosamente. Alerta programada para el {fecha_vencimiento.strftime('%d/%m/%Y')}.")
        else:
            st.error("⚠️ Por favor completa el nombre del dueño y la mascota.")

# --- PESTAÑA 2: MONITOR DE ALERTAS ---
with tab2:
    st.subheader("⚠️ Vencimientos de este mes")
    st.info("Esta tabla muestra a los clientes que se deben contactar esta semana.")
    
    # DATOS SIMULADOS (Para que el demo no se vea vacío)
    datos_demo = {
        "Mascota": ["Rocky", "Lola", "Coco", "Simba"],
        "Dueño": ["Ana García", "Carlos Ruiz", "Maria Paz", "Jorge Lima"],
        "Vacuna": ["Antirrábica", "Sextuple", "Quíntuple", "Sextuple"],
        "Vencimiento": [
            date.today() + timedelta(days=2),  # Vence en 2 días (URGENTE)
            date.today() + timedelta(days=5),  # Vence en 5 días
            date.today() + timedelta(days=30), # Vence en un mes
            date.today() - timedelta(days=10)  # Ya venció (PERDIDO)
        ],
        "Estado": ["🔴 URGENTE", "🟡 Próximo", "🟢 En fecha", "⚫ Vencido"]
    }
    
    df = pd.DataFrame(datos_demo)
    
    # Mostramos la tabla interactiva
    st.dataframe(
        df,
        column_config={
            "Vencimiento": st.column_config.DateColumn("Fecha Vencimiento", format="DD/MM/YYYY"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("### Acciones Rápidas")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📧 Enviar Recordatorios Automáticos"):
            st.toast("Enviando correos a Ana García y Carlos Ruiz...", icon="📨")
    with c2:
        st.download_button("📥 Descargar Reporte (Excel)", df.to_csv(), "vencimientos.csv")