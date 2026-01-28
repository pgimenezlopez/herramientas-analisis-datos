import pandas as pd
import random
from datetime import datetime, timedelta

# Configuración de datos ficticios
clientes = ["Ana García", "Carlos López", "Sofia Martínez", "Pedro Silva"]
notas_base = [
    "Sesión productiva, buen ánimo.", 
    "Reporta ansiedad leve por trabajo.", 
    "Avance significativo en objetivos.", 
    "Se siente estancado, revisamos estrategia.", 
    "Muy motivado hoy.",
    "Problemas de sueño esta semana.",
    "Mejora en la comunicación familiar."
]

data = []

# Generar historia para cada cliente
for cliente in clientes:
    # Fecha de inicio aleatoria hace unos meses
    dias_atras = random.randint(60, 120)
    fecha_actual = datetime.now() - timedelta(days=dias_atras)
    
    # Puntaje inicial aleatorio
    puntaje = random.uniform(3, 6)
    
    # Generar entre 15 y 25 sesiones por cliente
    num_sesiones = random.randint(15, 25)
    
    for i in range(num_sesiones):
        # Variación del puntaje (sube o baja un poco)
        cambio = random.uniform(-0.8, 1.2) 
        puntaje += cambio
        puntaje = max(1, min(10, puntaje)) # Mantener entre 1 y 10
        
        data.append({
            "Fecha": fecha_actual,
            "Cliente": cliente,
            "Puntaje": round(puntaje, 1),
            "Notas": random.choice(notas_base)
        })
        
        # EL CAMBIO CLAVE: Avanzar entre 3 y 10 días aleatoriamente
        # Esto hará que caigan en diferentes días de la semana
        dias_salto = random.randint(3, 10)
        fecha_actual += timedelta(days=dias_salto)

# Crear DataFrame y guardar
df = pd.DataFrame(data)
nombre_archivo = "pacientes_mock_random.xlsx"
df.to_excel(nombre_archivo, index=False)

print(f"✅ Archivo '{nombre_archivo}' regenerado con fechas variadas.")