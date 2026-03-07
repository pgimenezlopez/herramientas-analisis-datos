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

# --- NUEVO: SECCIÓN DE COMPLIANCE Y LEGAL ---
st.divider()
st.warning("⚖️ **Aviso de Responsabilidad Clínica:** Esta herramienta utiliza inteligencia artificial para asistir en la redacción. No sustituye el juicio clínico profesional. El usuario es 100% responsable de revisar, editar y validar la exactitud de este informe antes de anexarlo a cualquier historia médica oficial.")

# El checkbox es nuestro "candado legal"
consentimiento = st.checkbox("Declaro que los datos ingresados están anonimizados o cuento con el consentimiento explícito del paciente para procesar esta información.")
st.divider()

# --- LÓGICA DE GENERACIÓN MODIFICADA ---
# Añadimos type="primary" para que el botón resalte más
if st.button("Generar Informe", type="primary"):
    
    # 1. Validación de notas vacías
    if not notas_sesion:
        st.error("📝 Por favor, ingresa las notas de la sesión primero.")
        
    # 2. Validación legal (¡El candado!)
    elif not consentimiento:
        st.error("🛑 Debes confirmar el consentimiento marcando la casilla de arriba para generar el informe.")
        
    # 3. Si todo está en orden, ejecutamos la IA
    else:
        with st.spinner("Procesando formato clínico..."):
            try:
                # Prompt Engineering (Instrucciones estrictas)
                config = genai.types.GenerateContentConfig(
                    system_instruction="Eres un psicólogo clínico experto. Redacta un informe estructurado estrictamente en tres secciones: 1. Motivo de Consulta, 2. Evaluación del Estado Mental, 3. Plan de Acción. Mantén un tono formal, objetivo y médico."
                )

                # Llamada a Gemini
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=notas_sesion,
                    config=config
                )
                
                st.subheader("Informe Final:")
                st.markdown(response.text)
                st.success("✅ Generación completada con éxito.")
                
                # Botón de exportación
                st.download_button(
                    label="📥 Descargar Informe Clínico (.txt)",
                    data=response.text,
                    file_name="informe_clinico.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error de generación: {e}")
                # (Aquí puedes dejar el bloque except de diagnóstico que ya tenías)