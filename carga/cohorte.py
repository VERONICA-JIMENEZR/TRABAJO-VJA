import pandas as pd
from tranfroma import data

def calcular_cohorte(df):
    # Convertir la columna 'Fecha ultima compra' a datetime
    df['Fecha'] = pd.to_datetime(df['Fecha ultima compra'])
    df['Mes'] = df['Fecha'].dt.month
    df['Año'] = df['Fecha'].dt.year
    
    # Obtener la primera compra por cliente
    primer_compra = df.groupby('ID cliente')['Fecha'].min().reset_index()
    primer_compra['Mes'] = primer_compra['Fecha'].dt.month
    primer_compra['Año'] = primer_compra['Fecha'].dt.year
    
    # Contar clientes nuevos por cohorte (Año y Mes de primera compra)
    clientes_nuevos = primer_compra.groupby(['Año', 'Mes']).size().reset_index(name='Nuevos')
    
    # Obtener el producto más consumido por cohorte (Año y Mes de compra)
    productos_consumidos = df.groupby(['Año', 'Mes'])['Nombre producto'].agg(lambda x: x.value_counts().index[0]).reset_index(name='Consumido')
    
    # Obtener el producto más común en general
    producto_comun = df['Nombre producto'].value_counts().idxmax()
    
    return clientes_nuevos, productos_consumidos, producto_comun

# Llamar a la función con el DataFrame combinado
nuevos, consumidos, comun = calcular_cohorte(data)

# Imprimir los resultados
print("Nuevos por Cohorte:")
print(nuevos)

print("\nProductos Más Consumidos por Cohorte:")
print(consumidos)

print("\nProducto Común:", comun)
