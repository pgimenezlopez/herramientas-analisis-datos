import streamlit as st

st.set_page_config(page_title="Portafolio de Pablo", page_icon="🚀")

st.title("🚀 Portafolio de Ingeniería de Datos")
st.markdown("""
Hola, soy Pablo. Este es mi laboratorio de herramientas de automatización y análisis.
Selecciona una herramienta del menú lateral para probarla en vivo.
""")

# MENÚ LATERAL
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", ["Inicio", "Monitor de Transporte (STM)", "Consolidador de Excel", "Auditor de RRHH"])

if opcion == "Inicio":
    st.header("Bienvenido")
    st.image("https://media.licdn.com/dms/image/v2/D4D12AQFvGvj5s.../profile-displayphoto-shrink_800_800/0/170...?e=174...") # (Aquí puedes poner tu foto de LinkedIn si quieres)
    st.info("Estas herramientas fueron construidas con Python, Pandas y Streamlit.")

elif opcion == "Monitor de Transporte (STM)":
    # TRUCO: Ejecutar el otro script dentro de este
    import app
    # Nota: Para que esto funcione perfecto, a veces hay que ajustar el código de app.py
    # pero como primera aproximación sirve.
    
elif opcion == "Consolidador de Excel":
    st.warning("⚠️ Para usar esta herramienta, por favor ve a la aplicación dedicada:")
    st.link_button("Abrir Consolidador Pro", "https://TU-LINK-DEL-CONSOLIDADOR.streamlit.app")

elif opcion == "Auditor de RRHH":
    st.warning("⚠️ Herramienta de Auditoría:")
    st.link_button("Abrir Auditor RRHH", "https://TU-LINK-DE-RRHH.streamlit.app")