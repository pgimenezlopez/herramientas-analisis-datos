import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path

# --- CARGA DE ENTORNO (LOCAL) ---
# Busca el archivo .env en la carpeta principal
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- LÓGICA INTELIGENTE DE API KEY (LOCAL + NUBE) ---
# 1. Buscamos primero en el .env local (Tu Mac)
api_key = os.getenv("GEMINI_API_KEY")

# 2. Si está vacío (porque estamos en la nube), buscamos en st.secrets
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        # Si Streamlit se queja de que no hay secrets locales, lo ignoramos en silencio
        pass

# 3. Freno de emergencia amigable
if not api_key:
    st.error("🚨 No se encontró la API Key.")
    st.info("Local: Verifica tu archivo .env | Nube: Verifica los Secrets en Streamlit Cloud")
    st.stop() # Detiene la app aquí para no mostrar errores feos al usuario

# Inicializa el cliente con la clave segura
client = genai.Client(api_key=api_key)

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Informe Clínico Altiora", page_icon="🩺")
st.title("🩺 Altiora: Generador Clínico")

notas_sesion = st.text_area("Notas de la sesión:", height=300)

# --- LÓGICA DE GENERACIÓN ---
if st.button("Generar Informe"):
    if notas_sesion:
        with st.spinner("Procesando..."):
            try:
                # Intentamos con el modelo más actual por defecto
                # 1. Le damos una directiva maestra (System Instruction)
                config = genai.types.GenerateContentConfig(
                    system_instruction="Eres un psicólogo clínico experto. Redacta un informe estructurado estrictamente en tres secciones: 1. Motivo de Consulta, 2. Evaluación del Estado Mental, 3. Plan de Acción. Mantén un tono formal, objetivo y médico."
                )

                # 2. Generamos el contenido con esa configuración
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=notas_sesion,
                    config=config
                )
                
                st.subheader("Informe Final:")
                st.markdown(response.text)
                
                # Botón para descargar el informe como archivo de texto (.txt)
                st.download_button(
                    label="📥 Descargar Informe Clínico",
                    data=response.text,
                    file_name="informe_paciente.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.success("Completado.")
                
            except Exception as e:
                st.error(f"Error de generación: {e}")
                st.info("🔍 Buscando los nombres exactos de los modelos disponibles en tu cuenta...")
                
                # --- BLOQUE DE DIAGNÓSTICO REPARADO ---
                try:
                    models = client.models.list()
                    # Solo extraemos el nombre, que es un atributo seguro
                    nombres_modelos = [m.name for m in models]
                    
                    st.write("**Modelos que tu API Key tiene permiso para usar:**")
                    st.write(nombres_modelos[:15])  # Imprime los primeros 15
                except Exception as e2:
                    st.error(f"Error secundario al listar modelos: {e2}")