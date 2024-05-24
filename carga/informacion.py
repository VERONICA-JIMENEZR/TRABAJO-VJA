import pandas as pd
from tranfroma import data

def obtener_informacion_transacciones(df):
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

# Imprimir los resultados
print("\nStock máximo:", stock_max)
print("Stock mínimo:", stock_min)
print("Total de clientes:", total_clientes)
print("Promedio del valor de transacción:", promedio_valor_transaccion)
print("\nLos 15 productos más vendidos:")
print(productos_mas_vendidos)
print("\nLos 15 productos menos vendidos:")
print(productos_menos_vendidos)


