import pandas as pd
from pandas import DataFrame, Series
from transforma import data

def obtener_informacion_transacciones(df: DataFrame) -> tuple[int, int, int, float, Series, Series]:
    """
    Obtiene información relevante de un DataFrame de transacciones.

    Arguentos:
        df (DataFrame): DataFrame que contiene las transacciones. Se espera que tenga las columnas
                        'Stock maximo', 'Stock minimo', 'ID cliente', 'Precio final', 'Nombre producto' y 'ID transaccion'.

    Returns:
        tuple: Una tupla que contiene la siguiente información:
            - stock_max (int): El valor máximo de 'Stock maximo'.
            - stock_min (int): El valor mínimo de 'Stock minimo'.
            - total_clientes (int): El número total de clientes únicos.
            - promedio_valor_transaccion (float): El valor promedio de 'Precio final'.
            - productos_mas_vendidos (Series): Una Serie con los 15 productos más vendidos y sus cuentas.
            - productos_menos_vendidos (Series): Una Serie con los 15 productos menos vendidos y sus cuentas.
    """
    # Stock máximo y mínimo
    stock_max = df['Stock maximo'].max()
    stock_min = df['Stock minimo'].min()

    # Total de clientes
    total_clientes = df['ID cliente'].nunique()

    # Promedio del valor de transacción
    promedio_valor_transaccion = df['Precio final'].mean()

    # Los 15 productos más vendidos
    productos_mas_vendidos = df.groupby('Nombre producto')['ID transaccion'].count().nlargest(15)

    # Los 15 productos menos vendidos
    productos_menos_vendidos = df.groupby('Nombre producto')['ID transaccion'].count().nsmallest(15)

    return stock_max, stock_min, total_clientes, promedio_valor_transaccion, productos_mas_vendidos, productos_menos_vendidos

# Obtener la información de las transacciones
stock_max, stock_min, total_clientes, promedio_valor_transaccion, productos_mas_vendidos, productos_menos_vendidos = obtener_informacion_transacciones(data)

# Guardar los resultados de los productos más vendidos en un archivo CSV
productos_mas_vendidos.to_csv('productos_mas_vendidos.csv', header=['Producto'])

# Guardar los resultados de los productos menos vendidos en un archivo CSV
productos_menos_vendidos.to_csv('productos_menos_vendidos.csv', header=['Producto'])
