import pandas as pd
import numpy as np
import scipy.stats as stats  # <--- Esta es la línea que faltaba
import matplotlib.pyplot as plt
import seaborn as sns

# 1. CARGA
url_bici = "https://ckan-data.montevideo.gub.uy/dataset/15a3de29-2353-4d5f-9bae-e1617fa9e974/resource/6ada7fb7-cd03-4752-8b73-ef083df739aa/download/conteo_ciclovia_2025.csv"

print("🚲 Descargando y procesando datos completos...")

try:
    df = pd.read_csv(url_bici, encoding='utf-8', on_bad_lines='skip')
    df.columns = df.columns.str.strip().str.lower()
    
    # 2. LIMPIEZA
    # Fechas
    df['fecha_dt'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
    
    # Horas (tomamos el número entero antes de los dos puntos)
    df['hora_num'] = pd.to_numeric(df['hora'].astype(str).str.split(':').str[0], errors='coerce')
    
    # Total real (suma de ambos sentidos)
    df['total_bicis'] = df['hacia_ciudad_vieja'] + df['hacia_tres_cruces']
    
    # 3. ANÁLISIS DE RUTINA (HORA PICO)
    patron_horario = df.groupby('hora_num')[['total_bicis', 'hacia_ciudad_vieja', 'hacia_tres_cruces']].mean().reset_index()
    hora_pico = patron_horario.loc[patron_horario['total_bicis'].idxmax()]
    
    print(f"\n🔥 LA HORA PICO ES A LAS: {int(hora_pico['hora_num'])}:00 hs")
    print(f"🚲 Promedio total: {int(hora_pico['total_bicis'])} ciclistas")
    
    # 4. OUTLIERS (DÍAS RÉCORD)
    df_diario = df.groupby('fecha_dt')['total_bicis'].sum().reset_index()
    # Usamos stats aquí
    df_diario['z_score'] = np.abs(stats.zscore(df_diario['total_bicis']))
    dias_record = df_diario[df_diario['z_score'] > 2].sort_values(by='total_bicis', ascending=False)
    
    print("\n--- 📅 DÍAS RÉCORD (POSIBLES EVENTOS) ---")
    print(dias_record.head(3))

    # 5. VISUALIZACIÓN
    plt.figure(figsize=(12, 6))
    
    # Graficamos los flujos cruzados
    plt.plot(patron_horario['hora_num'], patron_horario['hacia_ciudad_vieja'], label='Hacia Ciudad Vieja', color='#1f77b4', marker='o') # Azul
    plt.plot(patron_horario['hora_num'], patron_horario['hacia_tres_cruces'], label='Hacia Tres Cruces', color='#ff7f0e', marker='o') # Naranja
    plt.plot(patron_horario['hora_num'], patron_horario['total_bicis'], label='Total Ciclovía', color='grey', linestyle='--', alpha=0.5)
    
    plt.title('Ritmo de la Ciclovía 18 de Julio (2025)')
    plt.xlabel('Hora del día (0-23 hs)')
    plt.ylabel('Cantidad Promedio de Ciclistas')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(range(0, 24)) 
    
    plt.show()

    # --- SECCIÓN NUEVA: ANÁLISIS DE DÍAS ---

    # 1. PREPARACIÓN DE DATOS DIARIOS
    # Agrupamos por fecha para tener el total de cada día
    df_diario = df.groupby('fecha_dt')['total_bicis'].sum().reset_index()

    # Extraemos el día de la semana (0=Lunes, 6=Domingo)
    df_diario['dia_num'] = df_diario['fecha_dt'].dt.dayofweek
    # Diccionario para traducir a español (detalle de calidad)
    nombres_dias = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    df_diario['nombre_dia'] = df_diario['dia_num'].map(nombres_dias)

    # 2. VISUALIZACIÓN (PANEL DOBLE)
    plt.figure(figsize=(14, 10)) # Hacemos el gráfico más alto para que quepan los dos

    # GRÁFICO A: Evolución Temporal (La Cronología)
    plt.subplot(2, 1, 1) # 2 filas, 1 columna, gráfico n° 1
    sns.lineplot(data=df_diario, x='fecha_dt', y='total_bicis', marker='o', color='teal', linewidth=2)

    # Destacamos el día de máximo tráfico
    dia_max = df_diario.loc[df_diario['total_bicis'].idxmax()]
    plt.annotate(f'Récord: {int(dia_max["total_bicis"])} bicis\n({dia_max["nombre_dia"]})', 
                xy=(dia_max['fecha_dt'], dia_max['total_bicis']), 
                xytext=(dia_max['fecha_dt'], dia_max['total_bicis'] + 100),
                arrowprops=dict(facecolor='black', shrink=0.05),
                fontsize=10, ha='center')

    plt.title('Evolución del Tráfico Diario (¿Hubo días de lluvia?)', fontsize=12)
    plt.ylabel('Total Ciclistas')
    plt.grid(True, alpha=0.3)

    # GRÁFICO B: Promedio por Día de la Semana (Comportamiento)
    plt.subplot(2, 1, 2) # 2 filas, 1 columna, gráfico n° 2

    # Calculamos el promedio para cada día de la semana
    patron_semanal = df_diario.groupby(['dia_num', 'nombre_dia'])['total_bicis'].mean().reset_index()

    sns.barplot(data=patron_semanal, x='nombre_dia', y='total_bicis', palette='viridis')

    plt.title('Perfil Semanal: ¿Uso Recreativo o Laboral?', fontsize=12)
    plt.xlabel('Día de la Semana')
    plt.ylabel('Promedio de Ciclistas')

    plt.tight_layout() # Ajusta los espacios para que no se encimen
    plt.show()

except Exception as e:
    print(f"❌ Error: {e}")