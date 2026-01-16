import streamlit as st
import pandas as pd
import io # Necesario para manejar archivos en la memoria (RAM) sin guardarlos en disco
from datetime import datetime

# CONFIGURACIÓN VISUAL
st.set_page_config(page_title="Consolidador Pro", page_icon="📂")

st.title("📂 Consolidador Automático de Excels")
st.markdown("""
**Instrucciones:**
1. Arrastra todos los archivos de ventas (Sucursales, Vendedores, etc).
2. El sistema detectará automáticamente las columnas.
3. Descarga el reporte unificado y limpio.
""")

# 1. EL WIDGET DE SUBIDA (LA MAGIA)
uploaded_files = st.file_uploader(
    "Sube tus archivos Excel aquí (.xlsx)", 
    accept_multiple_files=True, 
    type=['xlsx']
)

if uploaded_files:
    st.info(f"Has subido {len(uploaded_files)} archivos. Listos para procesar.")
    
    # Botón de acción para no procesar hasta que el usuario quiera
    if st.button("🚀 Unificar Archivos Ahora"):
        
        lista_dfs = []
        barra_progreso = st.progress(0)
        
        # 2. PROCESAMIENTO EN MEMORIA
        for i, archivo_subido in enumerate(uploaded_files):
            try:
                # Leemos directo desde la memoria del navegador
                df_temp = pd.read_excel(archivo_subido)
                
                # Agregamos la columna de origen (Auditoría)
                df_temp['Origen_Archivo'] = archivo_subido.name
                
                lista_dfs.append(df_temp)
                
                # Actualizar barra de progreso
                barra_progreso.progress((i + 1) / len(uploaded_files))
                
            except Exception as e:
                st.error(f"Error en el archivo {archivo_subido.name}: {e}")

        # 3. CONSOLIDACIÓN
        if lista_dfs:
            df_final = pd.concat(lista_dfs, ignore_index=True)
            
            # --- TUS TRUCOS DE LIMPIEZA ---
            # 1. Formato de Fechas (Si existe la columna)
            if 'Fecha' in df_final.columns:
                 # Convertimos a datetime primero por si acaso
                df_final['Fecha'] = pd.to_datetime(df_final['Fecha'], errors='coerce')
                # Formateamos a texto limpio DD/MM/AAAA
                df_final['Fecha'] = df_final['Fecha'].dt.strftime('%d/%m/%Y')
            
            # 2. Relleno de vacíos (Opcional, muy útil para clientes)
            df_final = df_final.fillna(0) # Pone 0 en lugares vacíos numéricos
            
            st.success("✅ ¡Proceso Terminado con Éxito!")
            
            # Mostrar una vista previa
            st.subheader("Vista Previa del Resultado:")
            st.dataframe(df_final.head(5), use_container_width=True)
            
            # 4. BOTÓN DE DESCARGA (EL ENTREGABLE)
            # Truco de Ingeniero: Guardar en un buffer de memoria, no en disco
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Consolidado')
                
                # Auto-ajuste de columnas (Un detalle de lujo)
                worksheet = writer.sheets['Consolidado']
                for idx, col in enumerate(df_final.columns):
                    max_len = max(df_final[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(idx, idx, max_len)

            # Preparamos el botón
            st.download_button(
                label="📥 Descargar Excel Unificado",
                data=buffer.getvalue(),
                file_name=f"Reporte_Consolidado_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.ms-excel"
            )