import pandas as pd
import numpy as np
import os

# Creamos una carpeta para simular el "desorden" del cliente
os.makedirs('archivos_cliente', exist_ok=True)

# Función para crear datos falsos
def crear_sucursal(nombre_sucursal, cantidad_ventas):
    data = {
        'Fecha': pd.date_range(start='2025-01-01', periods=cantidad_ventas, freq='D'),
        'Producto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor'], cantidad_ventas),
        'Vendedor': np.random.choice(['Ana', 'Carlos', 'Beatriz'], cantidad_ventas),
        'Monto': np.random.randint(50, 1500, cantidad_ventas),
        'Sucursal': nombre_sucursal # Esta columna es clave para no perder el origen al mezclar
    }
    return pd.DataFrame(data)

# Generamos 3 archivos distintos (El escenario típico de pesadilla administrativa)
print("🖨️  Imprimiendo archivos desordenados del cliente...")

df_centro = crear_sucursal('Sucursal Centro', 50)
df_centro.to_excel('archivos_cliente/ventas_centro.xlsx', index=False)
print(" -> Creado: ventas_centro.xlsx")

df_pocitos = crear_sucursal('Sucursal Pocitos', 40)
df_pocitos.to_excel('archivos_cliente/ventas_pocitos.xlsx', index=False)
print(" -> Creado: ventas_pocitos.xlsx")

df_carrasco = crear_sucursal('Sucursal Carrasco', 30)
df_carrasco.to_excel('archivos_cliente/ventas_carrasco.xlsx', index=False)
print(" -> Creado: ventas_carrasco.xlsx")

print("\n✅ ¡Problema generado! Revisa la carpeta 'archivos_cliente'.")