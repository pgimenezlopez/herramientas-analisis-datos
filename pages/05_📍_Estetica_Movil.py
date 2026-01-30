import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, time
import random
import math
import folium
from streamlit_folium import st_folium

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Ruta Estética", page_icon="📍", layout="wide")

# --- CONSTANTES ---
FILE_CLIENTES = "clientes_db.csv"
FILE_AGENDA = "agenda_db.csv"

# Coordenadas Base (Barrios de Montevideo)
COORDENADAS_BARRIOS = {
    "Pocitos": [-34.908, -56.145],
    "Carrasco": [-34.885, -56.058],
    "Centro": [-34.905, -56.190],
    "Malvín": [-34.895, -56.110],
    "Punta Carretas": [-34.920, -56.160],
    "Cordón": [-34.900, -56.170],
    "Prado": [-34.855, -56.200],
    "Buceo": [-34.900, -56.130],
    "Ciudad Vieja": [-34.907, -56.205],
    "Parque Batlle": [-34.895, -56.155],
    "Tres Cruces": [-34.892, -56.165],
    "Punta Gorda": [-34.890, -56.090],
    "La Blanqueada": [-34.880, -56.150]
}

# --- FUNCIONES AUXILIARES ---

def obtener_coordenadas(barrio):
    """Devuelve lat/lon con ruido aleatorio para no superponer puntos."""
    lat, lon = COORDENADAS_BARRIOS.get(barrio, [-34.90, -56.16])
    lat += random.uniform(-0.002, 0.002)
    lon += random.uniform(-0.002, 0.002)
    return lat, lon

def calcular_km(lat1, lon1, lat2, lon2):
    """Fórmula Haversine para distancia real en KM."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def cargar_datos(archivo, columnas):
    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        if "Fecha" in df.columns: df["Fecha"] = df["Fecha"].astype(str)
        return df
    return pd.DataFrame(columns=columnas)

# --- CEREBRO DE LA APP: ANÁLISIS DE CONVENIENCIA ---
def analizar_conveniencia(df_agenda, cliente_zona, hora_propuesta, lat_base, lon_base):
    lat_cliente, lon_cliente = COORDENADAS_BARRIOS.get(cliente_zona, [-34.90, -56.16])
    hora_str = str(hora_propuesta)[:5] # HH:MM
    
    # 1. Si la agenda está vacía, comparamos con CASA
    if df_agenda.empty:
        dist = calcular_km(lat_base, lon_base, lat_cliente, lon_cliente)
        return {
            "color": "green" if dist < 8 else "orange",
            "titulo": "Primer Turno",
            "mensaje": f"Sales desde tu base. Distancia: {dist} km.",
            "icono": "🏠"
        }

    # 2. Ordenar agenda
    agenda = df_agenda.sort_values("Hora").copy()
    
    # Buscar citas ANTES y DESPUÉS
    citas_antes = agenda[agenda["Hora"] <= hora_str]
    cita_prev = citas_antes.iloc[-1] if not citas_antes.empty else None
    
    citas_despues = agenda[agenda["Hora"] > hora_str]
    cita_next = citas_despues.iloc[0] if not citas_despues.empty else None

    # CASO A: Es el primer turno
    if cita_prev is None:
        dist_casa = calcular_km(lat_base, lon_base, lat_cliente, lon_cliente)
        if cita_next is not None:
            dist_sig = calcular_km(lat_cliente, lon_cliente, cita_next['lat'], cita_next['lon'])
            if dist_sig > 10:
                return {"color": "red", "titulo": "Desvío Grande", "mensaje": f"Te alejas {dist_sig} km de tu siguiente cliente.", "icono": "🛑"}
        return {"color": "green", "titulo": "Buen Comienzo", "mensaje": f"Inicio de ruta. A {dist_casa} km de casa.", "icono": "🚀"}

    # CASO B: Hay un turno ANTERIOR
    dist_anterior = calcular_km(cita_prev['lat'], cita_prev['lon'], lat_cliente, lon_cliente)
    origen = f"{cita_prev['Cliente']} en {cita_prev['Zona']}"
    
    if dist_anterior < 4:
        return {"color": "green", "titulo": "Zona Ideal", "mensaje": f"¡Excelente! A solo {dist_anterior} km de {origen}.", "icono": "✅"}
    elif dist_anterior < 8:
        return {"color": "orange", "titulo": "Distancia Aceptable", "mensaje": f"Te mueves {dist_anterior} km desde {cita_prev['Zona']}.", "icono": "⚠️"}
    else:
        return {"color": "red", "titulo": "Salto Logístico", "mensaje": f"OJO: Queda muy lejos ({dist_anterior} km) de tu turno anterior.", "icono": "🛑"}

# --- INTERFAZ PRINCIPAL ---
st.title("📍 Asistente Logístico Inteligente")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuración")
    mi_base = st.selectbox("Tu Base (Casa)", list(COORDENADAS_BARRIOS.keys()), index=3) # Default Malvín
    lat_base, lon_base = COORDENADAS_BARRIOS[mi_base]
    st.divider()
    fecha_seleccionada = st.date_input("Fecha de Agenda:", date.today())
    
    # Cargar Datos
    df_clientes = cargar_datos(FILE_CLIENTES, ["Nombre", "Zona", "Contacto", "Notas Técnicas"])
    df_agenda = cargar_datos(FILE_AGENDA, ["Fecha", "Hora", "Cliente", "Zona", "Servicio", "lat", "lon", "Estado"])
    
    if not df_agenda.empty:
        ruta_del_dia = df_agenda[df_agenda["Fecha"] == str(fecha_seleccionada)].sort_values("Hora")
    else:
        ruta_del_dia = pd.DataFrame()
    
    st.metric("Turnos Hoy", len(ruta_del_dia))

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["📞 Atender Llamada (Smart)", "👥 Base Clientes", "🗺️ Ver Mapa"])

# ==============================================================================
# TAB 1: ASISTENTE VISUAL (SEMÁFORO)
# ==============================================================================
with tab1:
    col_inputs, col_resultado = st.columns([1, 1.5])
    
    # --- COLUMNA IZQUIERDA: INPUTS ---
    with col_inputs:
        st.subheader("📞 Datos de la Llamada")
        
        # 1. CLIENTE
        if df_clientes.empty:
            st.error("⚠️ Carga clientes primero.")
            cliente_select = None
        else:
            cliente_select = st.selectbox("¿Quién llama?", df_clientes["Nombre"].unique())
        
        # 2. HORA (Input + Botones Rápidos)
        # Usamos session_state para que los botones actualicen el input
        if 'hora_temporal' not in st.session_state:
            st.session_state.hora_temporal = datetime.now().time()

        hora_input = st.time_input("¿Qué hora pide?", st.session_state.hora_temporal, step=1800)
        
        st.caption("Horarios estándar:")
        c_h1, c_h2, c_h3, c_h4 = st.columns(4)
        
        # Botones para setear hora rápido
        if c_h1.button("09:00"): 
            st.session_state.hora_temporal = time(9, 0)
            st.rerun()
        if c_h2.button("11:00"): 
            st.session_state.hora_temporal = time(11, 0)
            st.rerun()
        if c_h3.button("14:00"): 
            st.session_state.hora_temporal = time(14, 0)
            st.rerun()
        if c_h4.button("17:00"): 
            st.session_state.hora_temporal = time(17, 0)
            st.rerun()

        st.write("")
        st.markdown("---")
        
        # BOTÓN CONFIRMAR
        if cliente_select:
            row_c = df_clientes[df_clientes["Nombre"] == cliente_select].iloc[0]
            zona_c = row_c["Zona"]
            
            if st.button("📅 CONFIRMAR TURNO", type="primary", use_container_width=True):
                lat, lon = obtener_coordenadas(zona_c)
                nuevo = {
                    "Fecha": str(fecha_seleccionada), 
                    "Hora": str(hora_input)[:5], 
                    "Cliente": cliente_select, "Zona": zona_c, "Servicio": "Corte",
                    "lat": lat, "lon": lon, "Estado": "Pendiente"
                }
                pd.concat([df_agenda, pd.DataFrame([nuevo])], ignore_index=True).to_csv(FILE_AGENDA, index=False)
                st.toast("Turno Agendado con éxito", icon="💾")
                st.rerun()

    # --- COLUMNA DERECHA: SEMÁFORO ---
    with col_resultado:
        st.subheader("🤖 Análisis de Rentabilidad")
        
        if cliente_select:
            row_c = df_clientes[df_clientes["Nombre"] == cliente_select].iloc[0]
            zona_c = row_c["Zona"]
            resultado = analizar_conveniencia(ruta_del_dia, zona_c, hora_input, lat_base, lon_base)
            
            color_fondo = resultado["color"]
            emoji = resultado["icono"]
            
            if color_fondo == "green": c_box = st.success
            elif color_fondo == "orange": c_box = st.warning
            else: c_box = st.error
                
            with st.container(border=True):
                st.markdown(f"### {emoji} {resultado['titulo']}")
                c_box(resultado["mensaje"])
                st.caption(f"📍 Zona del cliente: **{zona_c}**")
        else:
            st.info("Selecciona un cliente.")

    # --- LÍNEA DE TIEMPO VISUAL (MEJORADA PARA MODO OSCURO) ---
    st.write("")
    st.markdown("##### 🗓️ Referencia Visual de Ocupación")
    
    if ruta_del_dia.empty:
        st.caption("Agenda vacía. Todo libre.")
    else:
        # Mostramos tarjetas
        cols = st.columns(len(ruta_del_dia))
        for i, (idx, row) in enumerate(ruta_del_dia.iterrows()):
            with cols[i]:
                # Cálculo de cercanía
                hora_cita = int(row['Hora'][:2])
                hora_input_int = hora_input.hour
                es_cerca = abs(hora_cita - hora_input_int) < 1
                
                # COLORES MEJORADOS
                if es_cerca:
                    borde = "3px solid #FFD700" # Amarillo Oro
                    bg = "#FFF9C4" # Amarillo claro
                    escala = "transform: scale(1.05);"
                else:
                    borde = "1px solid #ccc"
                    bg = "#f0f2f6" # Gris claro standard
                    escala = ""

                # HTML con color NEGRO FORZADO
                st.markdown(f"""
                <div style="
                    border: {borde}; 
                    background-color: {bg}; 
                    color: #000000; 
                    padding: 8px; 
                    border-radius: 8px; 
                    text-align: center; 
                    font-size: 13px;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                    {escala}
                    transition: all 0.3s ease;
                ">
                    <div style="font-weight: bold; font-size: 16px;">{row['Hora']}</div>
                    <div style="margin-top: 4px;">{row['Cliente']}</div>
                    <div style="font-size: 11px; color: #444;">📍 {row['Zona']}</div>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: GESTIÓN DE CLIENTES
# ==============================================================================
with tab2:
    st.subheader("Base de Clientes")
    c1, c2 = st.columns(2)
    with c1:
        with st.form("alta_cliente", clear_on_submit=True):
            st.write("**Nuevo Cliente**")
            nombre = st.text_input("Nombre")
            zona = st.selectbox("Zona", list(COORDENADAS_BARRIOS.keys()))
            contacto = st.text_input("Contacto")
            notas = st.text_area("Ficha Técnica")
            if st.form_submit_button("Guardar"):
                if nombre:
                    nuevo = pd.DataFrame([{"Nombre": nombre, "Zona": zona, "Contacto": contacto, "Notas Técnicas": notas}])
                    pd.concat([df_clientes, nuevo], ignore_index=True).to_csv(FILE_CLIENTES, index=False)
                    st.rerun()
                else: st.error("Falta nombre.")
    with c2:
        st.dataframe(df_clientes, hide_index=True, use_container_width=True)

# ==============================================================================
# TAB 3: MAPA DE EJECUCIÓN
# ==============================================================================
with tab3:
    st.subheader(f"Mapa del {fecha_seleccionada.strftime('%d/%m')}")
    
    if not ruta_del_dia.empty:
        avg_lat = ruta_del_dia["lat"].mean()
        avg_lon = ruta_del_dia["lon"].mean()
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)
        
        # Base
        folium.Marker(
            [lat_base, lon_base], 
            popup="Base", tooltip="Inicio",
            icon=folium.Icon(color="blue", icon="home", prefix="fa")
        ).add_to(m)
        
        # Ruta
        puntos_linea = [[lat_base, lon_base]]
        contador = 1
        
        for i, row in ruta_del_dia.iterrows():
            folium.Marker(
                [row['lat'], row['lon']], 
                popup=f"{row['Hora']} - {row['Cliente']}",
                tooltip=f"{contador}. {row['Cliente']}",
                icon=folium.Icon(color="red", icon=str(contador), prefix="fa")
            ).add_to(m)
            puntos_linea.append([row['lat'], row['lon']])
            contador += 1
            
        folium.PolyLine(puntos_linea, color="blue", weight=2.5, opacity=0.8).add_to(m)
        st_folium(m, width=800, height=500)
    else:
        st.info("Agenda vacía. No hay ruta para mostrar.")