import pandas as pd
from transforma import data
from datetime import datetime

def calcular_RFM_segmentacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la segmentación RFM y clasifica los clientes en Oro, Plata y Bronce.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'ID cliente', 'Fecha ultima compra', 'Fecha transaccion',
                           'ID transaccion' y 'Precio final'.

    Returns:
        pd.DataFrame: DataFrame con las columnas 'Recency', 'Frequency', 'Monetary', 'R_quartile', 'F_quartile',
                      'M_quartile', 'RFM_Segment' y 'Cliente', donde cada fila representa un cliente segmentado.
    """
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

    # Clasificamos los clientes en Oro, Plata y Bronce
    rfm['Cliente'] = rfm['RFM_Segment'].apply(
        lambda x: 'Oro' if x == 'OroOroOro' else ('Plata' if x == 'PlataPlataPlata' else 'Bronce')
    )

    return rfm

def guardar_clientes_segmentados(rfm: pd.DataFrame, df: pd.DataFrame) -> None:
    """
    Guarda los clientes segmentados en un archivo CSV y muestra nombre y cliente (la clasificación).

    Args:
        rfm (pd.DataFrame): DataFrame con la segmentación RFM.
        df (pd.DataFrame): DataFrame original con los datos de los clientes.
    """
    # Obtener los nombres únicos de los clientes de cada categoría
    nombres = df[['ID cliente', 'Nombre']].drop_duplicates().set_index('ID cliente')
    rfm = rfm.join(nombres, on='ID cliente')
    
    # Guardar en un archivo CSV
    rfm.to_csv('clientes_segmentados.csv', columns=['Nombre', 'Cliente'])

    # Mostrar el nombre y el tipo de cliente en la consola
    print(rfm[['Nombre', 'Cliente']])

# Datos
data = data
# Calcular la segmentación RFM
resultado_RFM = calcular_RFM_segmentacion(data)
guardar_clientes_segmentados(resultado_RFM, data)

