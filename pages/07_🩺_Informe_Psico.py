import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Carga de entorno
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Informe Clínico Altiora", page_icon="🩺")
st.title("🩺 Altiora: Generador Clínico")

notas_sesion = st.text_area("Notas de la sesión:", height=300)

if st.button("Generar Informe"):
    if notas_sesion:
        with st.spinner("Procesando..."):
            try:
                # Intentamos con el modelo más actual por defecto
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=notas_sesion
                )
                
                st.subheader("Informe Final:")
                st.markdown(response.text)
                st.success("Completado.")
                
            except Exception as e:
                st.error(f"Error de generación: {e}")
                st.info("🔍 Buscando los nombres exactos de los modelos disponibles en tu cuenta...")
                
                # --- NUEVO BLOQUE DE DIAGNÓSTICO REPARADO ---
                try:
                    models = client.models.list()
                    # Solo extraemos el nombre, que es un atributo seguro
                    nombres_modelos = [m.name for m in models]
                    
                    st.write("**Modelos que tu API Key tiene permiso para usar:**")
                    st.write(nombres_modelos[:15])  # Imprime los primeros 15
                except Exception as e2:
                    st.error(f"Error secundario al listar modelos: {e2}")