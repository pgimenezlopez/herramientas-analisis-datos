import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import random
import math
import folium
from streamlit_folium import st_folium

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Logística Pyme", page_icon="🚚", layout="wide")

# --- CONSTANTES DE DATOS ---
FILE_PUNTOS = "reparto_puntos.csv"
FILE_RUTA = "reparto_ruta.csv"

# Coordenadas Base (Montevideo)
COORDENADAS_BARRIOS = {
    "Centro": [-34.905, -56.190],
    "Ciudad Vieja": [-34.907, -56.205],
    "Aguada": [-34.890, -56.190],
    "Pocitos": [-34.908, -56.145],
    "Punta Carretas": [-34.920, -56.160],
    "Buceo": [-34.900, -56.130],
    "Malvín": [-34.895, -56.110],
    "Carrasco": [-34.885, -56.058],
    "La Blanqueada": [-34.880, -56.150],
    "Unión": [-34.870, -56.140],
    "Prado": [-34.855, -56.200],
    "Cerro": [-34.880, -56.250]
}

# --- FUNCIONES AUXILIARES ---

def obtener_coordenadas(barrio):
    lat, lon = COORDENADAS_BARRIOS.get(barrio, [-34.90, -56.16])
    lat += random.uniform(-0.002, 0.002)
    lon += random.uniform(-0.002, 0.002)
    return lat, lon

def calcular_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def cargar_datos(archivo, columnas):
    """Carga datos y asegura que siempre existan las columnas necesarias."""
    if os.path.exists(archivo):
        try:
            df = pd.read_csv(archivo)
            for col in columnas:
                if col not in df.columns:
                    valor = "Pendiente" if col == "Estado" else ""
                    df[col] = valor
            
            if "Fecha" in df.columns: df["Fecha"] = df["Fecha"].astype(str)
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=columnas)
            
    return pd.DataFrame(columns=columnas)

def optimizar_ruta_automatica(df_ruta, lat_inicio, lon_inicio):
    ruta_optimizada = []
    puntos_pendientes = df_ruta.copy()
    curr_lat, curr_lon = lat_inicio, lon_inicio
    
    while not puntos_pendientes.empty:
        distancia_minima = float('inf')
        indice_ganador = -1
        
        for idx, row in puntos_pendientes.iterrows():
            dist = calcular_km(curr_lat, curr_lon, row['lat'], row['lon'])
            if dist < distancia_minima:
                distancia_minima = dist
                indice_ganador = idx
        
        fila_ganadora = puntos_pendientes.loc[indice_ganador]
        ruta_optimizada.append(fila_ganadora)
        curr_lat, curr_lon = fila_ganadora['lat'], fila_ganadora['lon']
        puntos_pendientes = puntos_pendientes.drop(indice_ganador)
    
    return pd.DataFrame(ruta_optimizada)

# --- INTERFAZ PRINCIPAL ---
st.title("🚚 Logística & Reparto Pyme")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🏭 Depósito")
    mi_base = st.selectbox("Salida", list(COORDENADAS_BARRIOS.keys()), index=2)
    lat_base, lon_base = COORDENADAS_BARRIOS[mi_base]
    
    st.divider()
    fecha_seleccionada = st.date_input("Fecha:", date.today())
    
    # Carga Segura de Datos (Agregamos "Notas_Ruta" a las columnas)
    col_puntos = ["Cliente", "Barrio", "Direccion", "Notas"]
    col_ruta = ["Fecha", "Orden", "Cliente", "Barrio", "Pedido", "lat", "lon", "Estado", "Notas_Ruta"]
    
    df_puntos = cargar_datos(FILE_PUNTOS, col_puntos)
    df_ruta = cargar_datos(FILE_RUTA, col_ruta)
    
    ruta_del_dia = df_ruta[df_ruta["Fecha"] == str(fecha_seleccionada)].reset_index(drop=True)
    
    if not ruta_del_dia.empty:
        pendientes = len(ruta_del_dia[ruta_del_dia["Estado"] == "Pendiente"])
        
        # --- CÁLCULO DE KM TOTALES ---
        km_total = 0
        prev_lat, prev_lon = lat_base, lon_base
        for _, row in ruta_del_dia.iterrows():
            dist = calcular_km(prev_lat, prev_lon, row['lat'], row['lon'])
            km_total += dist
            prev_lat, prev_lon = row['lat'], row['lon']
            
    else:
        pendientes = 0
        km_total = 0
        
    st.metric("Entregas Pendientes", pendientes)
    st.metric("📍 Recorrido Est.", f"{round(km_total, 1)} km")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📋 Planificación", "🚛 Ejecución (Chofer)", "👥 Base Datos"])

# ==============================================================================
# TAB 1: PLANIFICADOR
# ==============================================================================
with tab1:
    col_mapa, col_form = st.columns([2, 1])
    
    with col_form:
        st.subheader("➕ Cargar Camioneta")
        with st.form("form_carga"):
            if df_puntos.empty:
                st.warning("Carga puntos en la pestaña 3.")
                cliente = None
            else:
                cliente = st.selectbox("Cliente", df_puntos["Cliente"].unique())
            
            pedido = st.text_input("Pedido", "Caja #")
            
            if st.form_submit_button("Agregar"):
                if cliente:
                    row_c = df_puntos[df_puntos["Cliente"] == cliente].iloc[0]
                    lat, lon = obtener_coordenadas(row_c["Barrio"])
                    nuevo = {
                        "Fecha": str(fecha_seleccionada),
                        "Orden": len(ruta_del_dia) + 1,
                        "Cliente": cliente, "Barrio": row_c["Barrio"], 
                        "Pedido": pedido, "lat": lat, "lon": lon, 
                        "Estado": "Pendiente", "Notas_Ruta": ""
                    }
                    pd.concat([df_ruta, pd.DataFrame([nuevo])], ignore_index=True).to_csv(FILE_RUTA, index=False)
                    st.rerun()

        st.write("")
        if not ruta_del_dia.empty:
            if st.button("⚡ Optimizar Ruta", type="primary", use_container_width=True):
                pendientes_df = ruta_del_dia[ruta_del_dia["Estado"] == "Pendiente"]
                completados_df = ruta_del_dia[ruta_del_dia["Estado"] != "Pendiente"]
                
                if not pendientes_df.empty:
                    optimizado = optimizar_ruta_automatica(pendientes_df, lat_base, lon_base)
                    df_final_dia = pd.concat([completados_df, optimizado], ignore_index=True)
                    
                    df_global = cargar_datos(FILE_RUTA, col_ruta)
                    df_otros_dias = df_global[df_global["Fecha"] != str(fecha_seleccionada)]
                    
                    pd.concat([df_otros_dias, df_final_dia], ignore_index=True).to_csv(FILE_RUTA, index=False)
                    st.toast(f"Ruta optimizada: {round(km_total,1)} km.", icon="🗺️")
                    st.rerun()

    with col_mapa:
        st.subheader("Mapa de Ruta")
        if ruta_del_dia.empty:
            st.info("Camioneta vacía.")
        else:
            m = folium.Map(location=[lat_base, lon_base], zoom_start=12)
            folium.Marker([lat_base, lon_base], popup="Depósito", icon=folium.Icon(color="black", icon="industry", prefix="fa")).add_to(m)
            
            puntos = [[lat_base, lon_base]]
            for i, row in ruta_del_dia.iterrows():
                color = "green" if row['Estado'] == "Completado" else "blue"
                icono = "check" if row['Estado'] == "Completado" else "box"
                
                # En el popup mostramos la nota si existe
                nota_txt = f"<br>⚠️ {row['Notas_Ruta']}" if row['Notas_Ruta'] else ""
                
                folium.Marker(
                    [row['lat'], row['lon']],
                    popup=f"{row['Cliente']} ({row['Pedido']}){nota_txt}",
                    tooltip=f"{i+1}. {row['Cliente']}",
                    icon=folium.Icon(color=color, icon=icono, prefix="fa")
                ).add_to(m)
                if row['Estado'] == "Pendiente":
                    puntos.append([row['lat'], row['lon']])
            
            folium.PolyLine(puntos, color="blue", weight=3, opacity=0.6).add_to(m)
            st_folium(m, width=800, height=500)

# ==============================================================================
# TAB 2: EJECUCIÓN (FLEXIBLE + NOTAS)
# ==============================================================================
with tab2:
    st.subheader("🚛 Modo Chofer")
    if ruta_del_dia.empty:
        st.info("Sin ruta hoy.")
    else:
        pendientes = ruta_del_dia[ruta_del_dia["Estado"] == "Pendiente"].reset_index(drop=True)
        
        if pendientes.empty:
            st.success("🎉 ¡Reparto finalizado!")
        else:
            siguiente = pendientes.iloc[0]
            with st.container(border=True):
                c_izq, c_der = st.columns([2, 1])
                with c_izq:
                    st.markdown(f"## {siguiente['Cliente']}")
                    st.markdown(f"📍 **{siguiente['Barrio']}**")
                    st.info(f"📦 {siguiente['Pedido']}")
                    
                    # Mostrar nota anterior si ya fue postergado alguna vez
                    if siguiente['Notas_Ruta']:
                        st.warning(f"⚠️ Nota previa: {siguiente['Notas_Ruta']}")

                with c_der:
                    st.write("")
                    # 1. COMPLETAR
                    if st.button("✅ Entregado", key="btn_done", type="primary", use_container_width=True):
                        mask = (df_ruta["Fecha"] == str(fecha_seleccionada)) & (df_ruta["Cliente"] == siguiente["Cliente"]) & (df_ruta["Pedido"] == siguiente["Pedido"])
                        df_ruta.loc[mask, "Estado"] = "Completado"
                        df_ruta.to_csv(FILE_RUTA, index=False)
                        st.rerun()
                    
                    st.divider()
                    
                    # 2. POSTERGAR CON NOTA
                    motivo = st.text_input("¿Por qué postergas?", placeholder="Ej: No estaba...", key="txt_motivo")
                    
                    if st.button("🔄 Postergar", key="btn_skip", use_container_width=True):
                        # Identificar fila
                        mask = (df_ruta["Fecha"] == str(fecha_seleccionada)) & (df_ruta["Cliente"] == siguiente["Cliente"]) & (df_ruta["Pedido"] == siguiente["Pedido"])
                        
                        # Actualizar la nota ANTES de mover
                        if motivo:
                            df_ruta.loc[mask, "Notas_Ruta"] = f"{motivo} ({datetime.now().strftime('%H:%M')})"
                        
                        # Lógica de mover al final
                        # Recargamos df_ruta actualizado con la nota
                        df_hoy = df_ruta[df_ruta["Fecha"] == str(fecha_seleccionada)]
                        idx_en_dia = df_hoy[
                            (df_hoy["Cliente"] == siguiente["Cliente"]) & 
                            (df_hoy["Pedido"] == siguiente["Pedido"])
                        ].index[0]
                        
                        # Operación de movimiento
                        fila = df_hoy.loc[[idx_en_dia]]
                        resto = df_hoy.drop(idx_en_dia)
                        nueva_ruta_dia = pd.concat([resto, fila], ignore_index=True)
                        
                        # Guardar globalmente
                        otros_dias = df_ruta[df_ruta["Fecha"] != str(fecha_seleccionada)]
                        df_final = pd.concat([otros_dias, nueva_ruta_dia], ignore_index=True)
                        df_final.to_csv(FILE_RUTA, index=False)
                        
                        st.toast("Postergado al final de la cola.", icon="⏭️")
                        st.rerun()

            st.caption("Siguientes paradas:")
            if len(pendientes) > 1:
                for i in range(1, len(pendientes)):
                    row = pendientes.iloc[i]
                    # Mostramos icono de advertencia si tiene nota
                    aviso = "⚠️" if row['Notas_Ruta'] else ""
                    st.text(f"{i+1}. {row['Cliente']} {aviso}")

# ==============================================================================
# TAB 3: BASE DE DATOS
# ==============================================================================
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Nuevo Punto")
        with st.form("alta_punto", clear_on_submit=True):
            cliente = st.text_input("Nombre")
            barrio = st.selectbox("Barrio", list(COORDENADAS_BARRIOS.keys()))
            direccion = st.text_input("Dirección")
            notas = st.text_area("Notas Fijas")
            if st.form_submit_button("Guardar"):
                nuevo = pd.DataFrame([{"Cliente": cliente, "Barrio": barrio, "Direccion": direccion, "Notas": notas}])
                pd.concat([df_puntos, nuevo], ignore_index=True).to_csv(FILE_PUNTOS, index=False)
                st.rerun()
    with c2:
        st.dataframe(df_puntos, hide_index=True)