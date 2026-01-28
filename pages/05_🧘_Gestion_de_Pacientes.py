import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard Terapéutico", layout="wide")

# Título y Descripción
st.title("🧠 Monitor de Progreso de Clientes")
st.markdown("""
Esta herramienta transforma tus planillas de Excel en **visualizaciones claras** para monitorear la evolución de tus pacientes/coachees.
""")

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("1. Carga de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel", type=["xlsx"])

# --- LÓGICA PRINCIPAL ---
if uploaded_file is not None:
    try:
        # Cargar datos con Pandas
        df = pd.read_excel(uploaded_file)

        # Verificar que existan las columnas mínimas necesarias
        required_columns = ['Fecha', 'Cliente', 'Puntaje']
        if not all(col in df.columns for col in required_columns):
            st.error(f"El Excel debe tener al menos estas columnas: {', '.join(required_columns)}")
        else:
            # Asegurar que la fecha sea datetime
            df['Fecha'] = pd.to_datetime(df['Fecha'])

            # --- FILTROS ---
            st.sidebar.header("2. Filtros")
            lista_clientes = df['Cliente'].unique()
            cliente_seleccionado = st.sidebar.selectbox("Selecciona un Cliente:", lista_clientes)

            # Filtrar el DataFrame por el cliente seleccionado
            df_cliente = df[df['Cliente'] == cliente_seleccionado].sort_values(by='Fecha')

            # --- DASHBOARD DEL CLIENTE ---
            st.divider()
            st.header(f"📊 Evolución de: {cliente_seleccionado}")

            # 1. KPIs (Indicadores Clave)
            total_sesiones = len(df_cliente)
            promedio_puntaje = df_cliente['Puntaje'].mean()
            ultimo_puntaje = df_cliente.iloc[-1]['Puntaje']
            
            delta = 0
            if len(df_cliente) > 1:
                delta = ultimo_puntaje - df_cliente.iloc[-2]['Puntaje']

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Sesiones", total_sesiones)
            col2.metric("Puntaje Actual", f"{ultimo_puntaje:.1f}", delta=f"{delta:.1f}")
            col3.metric("Promedio Histórico", f"{promedio_puntaje:.1f}")

            # 2. Gráfico de Evolución (Plotly)
            st.subheader("Tendencia en el tiempo")
            fig = px.line(df_cliente, x='Fecha', y='Puntaje', markers=True, 
                          title=f"Progreso de {cliente_seleccionado}",
                          labels={'Puntaje': 'Nivel de Bienestar/Progreso'},
                          template="plotly_white")
            fig.update_traces(line_color='#4AA96C', line_width=3)
            st.plotly_chart(fig, use_container_width=True)

            # 3. Tabla de Datos
            with st.expander("Ver detalle de sesiones y notas"):
                st.dataframe(df_cliente[['Fecha', 'Puntaje', 'Notas' if 'Notas' in df.columns else 'Puntaje']], use_container_width=True)

            # --- 4. Heatmap: Mejores días de la semana ---
            st.subheader("🗓️ ¿Qué días de la semana te sientes mejor? (Heatmap)")

            # Crear columna con nombre del día en Inglés (para asegurar compatibilidad)
            df_cliente['Dia_Ingles'] = df_cliente['Fecha'].dt.day_name()

            # Diccionario manual para traducir a Español (más robusto que usar locale)
            traduccion_dias = {
                'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
                'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
            }
            
            # Aplicar traducción
            df_cliente['Dia_Espanol'] = df_cliente['Dia_Ingles'].map(traduccion_dias)

            # Definir el orden correcto para el gráfico
            orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            
            # Calcular promedio agrupando por día
            heatmap_data = df_cliente.groupby('Dia_Espanol')['Puntaje'].mean().reindex(orden_dias)

            # Graficar heatmap
            fig_heat = go.Figure(data=go.Heatmap(
                z=[heatmap_data.values], # Los valores del puntaje (color)
                x=orden_dias,            # Los días (eje X)
                y=['Promedio'],          # Etiqueta eje Y
                colorscale='Greens',     # Escala de colores
                showscale=True
            ))
            
            fig_heat.update_layout(
                title='Intensidad de bienestar por día',
                xaxis_title='Día de la Semana',
                yaxis_title='',
                height=300
            )
            st.plotly_chart(fig_heat, use_container_width=True)

            # --- 5. Análisis de Texto: Nube de Palabras ---
            st.divider()
            st.subheader("🗣️ Temas recurrentes en las notas")

            if 'Notas' in df_cliente.columns and not df_cliente['Notas'].dropna().empty:
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt

                # 1. Unir todas las notas en un solo texto gigante
                texto_completo = " ".join(df_cliente['Notas'].dropna().astype(str))

                # 2. Configurar la nube (quitando palabras comunes irrelevantes)
                # "stopwords" son palabras como: el, la, de, que... que no aportan significado
                stopwords_es = set(['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como'])
                
             
                wordcloud = WordCloud(width=800, height=400, 
                                    background_color='white', 
                                    colormap='Greens',  # <--- CAMBIO AQUÍ (estaba 'TealGrn')
                                    stopwords=stopwords_es,
                                    min_font_size=10).generate(texto_completo)

                # 3. Mostrar gráfico con Matplotlib
                fig_wc, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off") # Quitar ejes X e Y
                st.pyplot(fig_wc)
            else:
                st.info("No hay suficientes notas de texto para generar la nube de palabras.")

    except Exception as e:
        # Aquí capturamos cualquier error que ocurra dentro del TRY
        st.error(f"Hubo un error al procesar el archivo: {e}")

else:
    # --- MENSAJE DE BIENVENIDA ---
    st.info("👋 Por favor, sube un archivo Excel en la barra lateral para comenzar.")
    st.write("El archivo debe tener las columnas: **Fecha, Cliente, Puntaje**.")