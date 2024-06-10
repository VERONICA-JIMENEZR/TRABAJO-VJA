import pandas as pd
from transforma import data  # Supongo que 'data' es un DataFrame predefinido
from typing import Tuple, Any

def calcular_cohorte(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Any]:
    """
    Calcula la cohorte de clientes, los productos más consumidos y el producto más común.

    Parámetros:
    - df (pd.DataFrame): DataFrame que contiene los datos de los clientes.

    Retorna:
    - Tuple[pd.DataFrame, pd.DataFrame, Any]: Una tupla que contiene tres elementos:
      1. DataFrame de clientes nuevos por cohorte.
      2. DataFrame de productos más consumidos por cohorte.
      3. El producto más común en general.
    """
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

# Guardar los resultados en un archivo CSV
# Solo tomamos los datos necesarios para el archivo de productos más vendidos por mes
productos_mas_vendidos_por_mes = consumidos[['Año', 'Mes', 'Consumido']]
productos_mas_vendidos_por_mes.to_csv('resultados_cohorte.csv', index=False)
