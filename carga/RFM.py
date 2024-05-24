import pandas as pd
from tranfroma import data
from datetime import datetime

def calcular_RFM_segmentacion(df):
    # Convertimos las fechas a formato datetime
    df['Fecha ultima compra'] = pd.to_datetime(df['Fecha ultima compra'])
    df['Fecha transaccion'] = pd.to_datetime(df['Fecha transaccion'])

    # Calculamos Recency, Frequency y Monetary
    rfm = df.groupby('ID cliente').agg({
        'Fecha transaccion': lambda x: (datetime.now() - x.max()).days,  # Recency
        'ID transaccion': 'count',  # Frequency
        'Precio final': 'sum'  # Monetary
    })

    # Renombramos las columnas
    rfm.rename(columns={
        'Fecha transaccion': 'Recency',
        'ID transaccion': 'Frequency',
        'Precio final': 'Monetary'
    }, inplace=True)

    # Eliminar filas con valores duplicados en la columna de frecuencia (si existen)
    rfm = rfm[~rfm.index.duplicated(keep='first')]

    # Creamos las etiquetas para la segmentación
    etiquetas = ['Bronce', 'Plata', 'Oro']

    # Creamos las divisiones para cada categoría
    rfm['R_quartile'] = pd.qcut(rfm['Recency'], 3, labels=etiquetas)
    rfm['F_quartile'] = pd.qcut(rfm['Frequency'].rank(method='first'), 3, labels=etiquetas)
    rfm['M_quartile'] = pd.qcut(rfm['Monetary'], 3, labels=etiquetas)

    # Creamos una nueva columna para la segmentación final
    rfm['RFM_Segment'] = rfm['R_quartile'].astype(str) + rfm['F_quartile'].astype(str) + rfm['M_quartile'].astype(str)

    return rfm

def contar_clientes_rfms(rfm):
    # Contar el número de clientes en cada categoría RFM
    clientes_oro = rfm[rfm['RFM_Segment'] == 'OroOroOro'].shape[0]
    clientes_plata = rfm[rfm['RFM_Segment'] == 'PlataPlataPlata'].shape[0]
    clientes_bronce = rfm[rfm['RFM_Segment'] == 'BronceBronceBronce'].shape[0]
    
    return clientes_oro, clientes_plata, clientes_bronce

def obtener_nombres_clientes_por_segmento(rfm, df, segmento):
    # Obtener los IDs de los clientes en el segmento especificado
    ids_clientes_segmento = rfm[rfm['RFM_Segment'] == segmento].index

    # Filtrar el DataFrame original para obtener solo los clientes del segmento
    clientes_segmento_df = df[df['ID cliente'].isin(ids_clientes_segmento)]

    # Obtener los nombres únicos de los clientes del segmento
    nombres_clientes_segmento = clientes_segmento_df['Nombre'].unique()

    return nombres_clientes_segmento

# Llamamos a la función con el DataFrame combinado
resultado_RFM = calcular_RFM_segmentacion(data)
print(resultado_RFM)

# Llamamos a la función para contar los clientes más importantes en cada categoría RFM
clientes_oro, clientes_plata, clientes_bronce = contar_clientes_rfms(resultado_RFM)

# Imprimimos los resultados
print(f"El número de clientes con la secuencia RFM 'OroOroOro' es: {clientes_oro}")
print(f"El número de clientes con la secuencia RFM 'PlataPlataPlata' es: {clientes_plata}")


# Obtener nombres de clientes en cada segmento
nombres_clientes_oro = obtener_nombres_clientes_por_segmento(resultado_RFM, data, 'OroOroOro')
nombres_clientes_plata = obtener_nombres_clientes_por_segmento(resultado_RFM, data, 'PlataPlataPlata')

# Imprimimos los resultados
print(f"Los nombres de los clientes con la secuencia RFM 'OroOroOro' son: {nombres_clientes_oro}")
print(f"Los nombres de los clientes con la secuencia RFM 'PlataPlataPlata' son: {nombres_clientes_plata}")
