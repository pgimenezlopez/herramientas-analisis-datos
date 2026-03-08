import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path
from fpdf import FPDF  # --- NUEVO IMPORT PARA EL PDF ---

# --- FUNCIÓN PARA CREAR EL PDF ---
def generar_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    
    # Título del documento
    pdf.set_font("helvetica", style="B", size=16)
    pdf.cell(0, 10, "Informe Clínico - Altiora", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5) # Salto de línea
    
    # Cuerpo del texto
    pdf.set_font("helvetica", size=11)
    
    # Limpiamos los asteriscos de negrita (**) que usa Markdown para que el PDF quede limpio
    texto_limpio = texto.replace("**", "")
    
    # multi_cell acomoda el texto automáticamente a los márgenes
    pdf.multi_cell(0, 6, texto_limpio)
    
    # --- AQUÍ ESTÁ LA CORRECCIÓN ---
    # Convertimos el bytearray a bytes puros para que Streamlit lo acepte
    return bytes(pdf.output())

# --- CARGA DE ENTORNO (LOCAL) ---
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- LÓGICA INTELIGENTE DE API KEY (LOCAL + NUBE) ---
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

if not api_key:
    st.error("🚨 No se encontró la API Key.")
    st.info("Local: Verifica tu archivo .env | Nube: Verifica los Secrets en Streamlit Cloud")
    st.stop()

client = genai.Client(api_key=api_key)

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Informe Clínico Altiora", page_icon="🩺")
st.title("🩺 Altiora: Generador Clínico")

notas_sesion = st.text_area("Notas de la sesión:", height=300)

# --- SECCIÓN DE COMPLIANCE LEGAL ---
st.divider()
st.warning("⚖️ **Aviso de Responsabilidad Clínica:** Esta herramienta utiliza inteligencia artificial para asistir en la redacción. No sustituye el juicio clínico profesional. El usuario es 100% responsable de revisar, editar y validar la exactitud de este informe antes de anexarlo a cualquier historia médica oficial.")

consentimiento = st.checkbox("Declaro que los datos ingresados están anonimizados o cuento con el consentimiento explícito del paciente para procesar esta información.")
st.divider()

# --- LÓGICA DE GENERACIÓN ---
if st.button("Generar Informe", type="primary"):
    
    if not notas_sesion:
        st.error("📝 Por favor, ingresa las notas de la sesión primero.")
        
    elif not consentimiento:
        st.error("🛑 Debes confirmar el consentimiento marcando la casilla de arriba para generar el informe.")
        
    else:
        with st.spinner("Procesando formato clínico SOAP..."):
            try:
                # Prompt Engineering Avanzado (SOAP)
                instruccion_soap = """Eres un psicólogo clínico experto. Tu tarea es procesar las notas sueltas de la sesión y redactar un informe psicológico estructurado estrictamente bajo el estándar internacional SOAP.

                Debes incluir obligatoriamente estas cuatro secciones:
                1. [S] Subjetivo: Resume lo que el paciente reporta.
                2. [O] Objetivo: Extrae las observaciones clínicas del terapeuta. Si no hay, indica "Sin observaciones".
                3. [A] Análisis: Redacta tu evaluación profesional clínica.
                4. [P] Plan: Detalla las intervenciones y foco para la próxima sesión.

                Reglas estrictas:
                - Mantén un tono formal, objetivo, empático y médico.
                - No inventes datos que no estén explícitos o implícitos en las notas originales.
                """
                
                config = genai.types.GenerateContentConfig(
                    system_instruction=instruccion_soap
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=notas_sesion,
                    config=config
                )
                
                st.subheader("Informe Final:")
                st.markdown(response.text)
                st.success("✅ Generación completada con éxito.")
                
                # --- NUEVO: BOTÓN DE DESCARGA PDF ---
                pdf_bytes = generar_pdf(response.text)
                
                st.download_button(
                    label="📄 Descargar Informe en PDF",
                    data=pdf_bytes,
                    file_name="informe_clinico_altiora.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error de generación: {e}")