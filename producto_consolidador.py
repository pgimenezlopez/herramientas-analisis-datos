import pandas as pd
import glob # Librería nativa para buscar archivos como un sabueso
import os

print("🤖 Iniciando el Consolidador Automático...")

# 1. BUSCAR LOS ARCHIVOS
# El *.xlsx significa "cualquier cosa que termine en Excel"
ruta_busqueda = 'archivos_cliente/*.xlsx'
archivos_encontrados = glob.glob(ruta_busqueda)

print(f"📂 Archivos detectados: {len(archivos_encontrados)}")
print(archivos_encontrados)

# 2. PROCESO DE FUSIÓN (EL BUCLE MÁGICO)
lista_de_dataframes = []

for archivo in archivos_encontrados:
    print(f"   -> Leyendo: {archivo}...")
    try:
        # Leemos el excel
        df_temporal = pd.read_excel(archivo)
        
        # Opcional: Agregar el nombre del archivo por si el cliente se olvidó de poner la sucursal
        nombre_archivo = os.path.basename(archivo)
        df_temporal['Origen_Archivo'] = nombre_archivo
        
        # Lo guardamos en la lista
        lista_de_dataframes.append(df_temporal)
    except Exception as e:
        print(f"❌ Error leyendo {archivo}: {e}")

# 3. CONSOLIDACIÓN FINAL
if lista_de_dataframes:
    df_maestro = pd.concat(lista_de_dataframes, ignore_index=True)
    
    # --- EL TRUCO DE SENIOR ---
    # Convertimos la fecha "científica" a fecha "humana" (DD/MM/AAAA)
    # Esto asegura que en el Excel final se vea perfecto, sin horas 00:00:00
    print("💅 Maquillando las fechas para el cliente...")
    
    # Verificamos si existe la columna Fecha antes de intentar formatearla
    if 'Fecha' in df_maestro.columns:
        # dt.strftime es "Date Time String Format"
        df_maestro['Fecha'] = df_maestro['Fecha'].dt.strftime('%d/%m/%Y')

    # 4. GUARDAR EL RESULTADO
    nombre_salida = 'REPORTE_CONSOLIDADO_GLOBAL.xlsx'
    df_maestro.to_excel(nombre_salida, index=False)
    
    print("\n" + "="*40)
    print(f"✅ ¡LISTO! Se generó: {nombre_salida}")
    print(f"📊 Total de filas procesadas: {len(df_maestro)}")
    print(f"💰 Suma total de ventas: ${df_maestro['Monto'].sum():,.0f}")
    print("="*40)
    
else:
    print("⚠️ No se encontraron archivos para unir.")