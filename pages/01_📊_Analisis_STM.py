import streamlit as st
import pandas as pd
import plotly.express as px  # <--- LA NUEVA ESTRELLA INTERACTIVA
import plotly.graph_objects as go # Para gráficos más complejos

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Monitor Ciclovía 18 de Julio", page_icon="🚲", layout="wide")

# TÍTULO
st.title("🚲 Monitor de Movilidad: Ciclovía 18 de Julio")
st.markdown("Tablero interactivo: **Haz zoom**, selecciona áreas y pasa el mouse sobre los datos.")

# 1. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    url_bici = "https://ckan-data.montevideo.gub.uy/dataset/15a3de29-2353-4d5f-9bae-e1617fa9e974/resource/6ada7fb7-cd03-4752-8b73-ef083df739aa/download/conteo_ciclovia_2025.csv"
    df = pd.read_csv(url_bici, encoding='utf-8', on_bad_lines='skip')
    df.columns = df.columns.str.strip().str.lower()
    
    # Procesamiento
    df['fecha_dt'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
    df['hora_num'] = pd.to_numeric(df['hora'].astype(str).str.split(':').str[0], errors='coerce')
    df['total_bicis'] = df['hacia_ciudad_vieja'] + df['hacia_tres_cruces']
    
    return df

with st.spinner('Cargando datos...'):
    df = cargar_datos()

# 2. KPIS
total_mes = df['total_bicis'].sum()
promedio_diario = df.groupby('fecha_dt')['total_bicis'].sum().mean()
dia_pico_fecha = df.groupby('fecha_dt')['total_bicis'].sum().idxmax()
dia_pico_valor = df.groupby('fecha_dt')['total_bicis'].sum().max()

col1, col2, col3 = st.columns(3)
col1.metric("Total Viajes (Mes)", f"{total_mes:,.0f}")
col2.metric("Promedio Diario", f"{promedio_diario:,.0f}")
col3.metric("Día Récord", f"{dia_pico_fecha.strftime('%d/%m')} ({dia_pico_valor:,.0f} bicis)")

st.divider()

# 3. INTERACTIVIDAD (FILTROS)
st.sidebar.header("Filtros")
sentido = st.sidebar.selectbox(
    "¿Qué flujo analizar?",
    ["Total de la Vía", "Hacia Ciudad Vieja", "Hacia Tres Cruces"]
)

# Mapeo
col_map = {
    "Total de la Vía": "total_bicis",
    "Hacia Ciudad Vieja": "hacia_ciudad_vieja",
    "Hacia Tres Cruces": "hacia_tres_cruces"
}
col_analisis = col_map[sentido]
color_grafico = "teal" if sentido == "Total de la Vía" else ("#1f77b4" if "Ciudad" in sentido else "#ff7f0e")

# 4. GRÁFICOS INTERACTIVOS (PLOTLY)
c1, c2 = st.columns(2)

with c1:
    st.subheader(f"⏱️ Perfil Horario ({sentido})")
    patron = df.groupby('hora_num')[col_analisis].mean().reset_index()
    
    # Gráfico de LÍNEA interactivo
    fig_hora = px.line(patron, x='hora_num', y=col_analisis, 
                       markers=True, title="Comportamiento Promedio por Hora")
    
    # Personalización visual (quitar fondo grid, color, etc)
    fig_hora.update_traces(line_color=color_grafico, line_width=3)
    fig_hora.update_layout(xaxis_title="Hora del día", yaxis_title="Bicis Promedio", hovermode="x unified")
    
    # RENDERIZADO INTERACTIVO
    st.plotly_chart(fig_hora, use_container_width=True)

with c2:
    st.subheader("📅 Evolución Diaria (Picos Mensuales)")
    diario = df.groupby('fecha_dt')[col_analisis].sum().reset_index()
    
    # 1. TRADUCIR DÍAS A ESPAÑOL
    diario['nombre_dia_en'] = diario['fecha_dt'].dt.day_name()
    mapa_dias = {
        'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 
        'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    diario['nombre_dia'] = diario['nombre_dia_en'].map(mapa_dias)
    
    # 2. DETECTAR EL MÁXIMO DE CADA MES
    # Creamos una columna auxiliar Mes-Año para agrupar
    diario['mes_año'] = diario['fecha_dt'].dt.to_period('M')
    
    # Buscamos los índices (filas) donde ocurre el máximo de cada mes
    idx_maximos = diario.groupby('mes_año')[col_analisis].idxmax()
    
    # 3. CREAR LA ETIQUETA (Solo para los ganadores)
    diario['etiqueta_pico'] = "" # Por defecto vacía
    # Llenamos solo las filas ganadoras con el nombre del día
    diario.loc[idx_maximos, 'etiqueta_pico'] = diario.loc[idx_maximos, 'nombre_dia']
    
    # 4. GRÁFICO CON TEXTO SELECTIVO
    fig_dia = px.bar(diario, x='fecha_dt', y=col_analisis,
                     title="Volumen Total por Día",
                     text='etiqueta_pico', # <--- AQUÍ ESTÁ LA MAGIA
                     hover_data=['nombre_dia']) # Para que al pasar el mouse también se vea
    
    fig_dia.update_traces(marker_color=color_grafico, textposition='outside') # Texto arriba de la barra
    fig_dia.update_layout(xaxis_title="Fecha", yaxis_title="Total Bicis", hovermode="x unified")
    
    st.plotly_chart(fig_dia, use_container_width=True)

# --- SECCIÓN NUEVA: MAPA DE CALOR ---
st.divider()
st.subheader("🔥 Mapa de Calor: Intensidad de Uso (Día vs Hora)")
st.markdown("Este gráfico muestra las **zonas rojas** de congestión combinando día y hora.")

# 1. PREPARACIÓN DE DATOS (Lógica traída del Notebook)
# Necesitamos el día de la semana para este gráfico específico
df['dia_semana_en'] = df['fecha_dt'].dt.day_name()

# Definimos orden lógico (no alfabético) y traducción
orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
mapa_espanol = {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 'Thursday': 'Jueves', 
                'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}

# Agrupamos: Promedio de bicis por combinación Día-Hora
heatmap_data = df.groupby(['dia_semana_en', 'hora_num'])['total_bicis'].mean().reset_index()

# 2. CREAMOS EL GRÁFICO CON PLOTLY
fig_heat = px.density_heatmap(
    heatmap_data, 
    x='hora_num', 
    y='dia_semana_en', 
    z='total_bicis', 
    nbinsx=24, 
    title='Intensidad Promedio (Semanal)',
    category_orders={'dia_semana_en': orden_dias}, # Forza el orden Lunes->Domingo
    labels={'dia_semana_en': 'Día', 'hora_num': 'Hora', 'total_bicis': 'Ciclistas'},
    color_continuous_scale='Viridis'
)

# Truco Pro: Traducir las etiquetas del Eje Y a español
fig_heat.update_yaxes(tickmode='array', tickvals=orden_dias, ticktext=list(mapa_espanol.values()))
fig_heat.update_layout(xaxis_title="Hora del día", hovermode="y unified")

# 3. RENDERIZAR EN LA APP
st.plotly_chart(fig_heat, use_container_width=True)

# 5. DETALLE DE HORA PICO (GRAFICO AVANZADO DE FLUJOS)
st.divider()
st.subheader("🔄 Análisis de Flujos Cruzados (Hora Pico)")

# Preparamos los datos para el gráfico de doble línea
patron_total = df.groupby('hora_num')[['hacia_ciudad_vieja', 'hacia_tres_cruces']].mean().reset_index()

fig_cruce = go.Figure()
fig_cruce.add_trace(go.Scatter(x=patron_total['hora_num'], y=patron_total['hacia_ciudad_vieja'], 
                    mode='lines+markers', name='Hacia Ciudad Vieja', line=dict(color='#1f77b4')))
fig_cruce.add_trace(go.Scatter(x=patron_total['hora_num'], y=patron_total['hacia_tres_cruces'], 
                    mode='lines+markers', name='Hacia Tres Cruces', line=dict(color='#ff7f0e')))

fig_cruce.update_layout(title="Comparativa de Sentidos (Zoom disponible)", 
                       xaxis_title="Hora", yaxis_title="Cantidad Promedio", hovermode="x unified")

st.plotly_chart(fig_cruce, use_container_width=True)

# --- SECCIÓN NUEVA: TABLA DE DATOS DETALLADA ---
st.divider()
st.subheader("📋 Auditoría de Datos (Tabla Detallada)")

# Usamos un 'expander' para que la tabla esté oculta por defecto y no ensucie la vista
with st.expander("🔎 Ver Tabla Completa de Registros"):
    
    # 1. PREPARACIÓN DE LA VISTA
    # Seleccionamos solo las columnas que importan para mostrar
    columnas_visibles = ['fecha', 'hora', 'total_bicis', 'hacia_ciudad_vieja', 'hacia_tres_cruces', 'dia_semana_en']
    
    # Creamos una copia para no romper el dataframe original
    df_tabla = df[columnas_visibles].copy()
    
    # Traducimos el día para que se vea bien en la tabla
    df_tabla['dia_semana_en'] = df_tabla['dia_semana_en'].map(mapa_espanol)
    df_tabla.rename(columns={'dia_semana_en': 'Día', 'total_bicis': 'TOTAL'}, inplace=True)
    
    # 2. MOSTRAR TABLA INTERACTIVA
    # 'use_container_width=True' hace que ocupe todo el ancho
    st.dataframe(
        df_tabla.sort_values(by='TOTAL', ascending=False), # Ordenado por los récords primero
        use_container_width=True,
        hide_index=True # Ocultamos el número de fila (0, 1, 2...) que no aporta mucho
    )
    
    # 3. BOTÓN DE DESCARGA (BONUS DE PRODUCTIVIDAD)
    # Convertimos el DF a CSV
    csv = df_tabla.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Descargar datos filtrados como CSV",
        data=csv,
        file_name='auditoria_ciclovia_2025.csv',
        mime='text/csv',
    )