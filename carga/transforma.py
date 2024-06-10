import pandas as pd
from carga_dato import clientes_df1, inventario_df, transacciones_df

def s(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
   las tablas quedan con el mismo tamaño
    """
    return df.sample(n=n)

# Submuestreo aleatorio para reducir el tamaño de los DataFrames
clientes_df = s(clientes_df1, 1000)
inventario_df = s(inventario_df, 1000)
transacciones_df = s(transacciones_df, 1000)

def merge_dataframes(transacciones_df: pd.DataFrame, clientes_df: pd.DataFrame, inventario_df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza la unión de los DataFrames de transacciones, clientes e inventario.

    Parametros:
        transacciones_df (pd.DataFrame): DataFrame de transacciones.
        clientes_df (pd.DataFrame): DataFrame de clientes.
        inventario_df (pd.DataFrame): DataFrame de inventario.

    Retorna:
        pd.DataFrame: DataFrame resultante después de la unión.
    """
    merged_df = pd.merge(transacciones_df, clientes_df, on='ID cliente')
    merged_df = pd.merge(merged_df, inventario_df, on='ID producto')
    merged_df = merged_df.iloc[:, :-3]  # Elimina las últimas tres columnas
    return merged_df

# Realizar las uniones de los DataFrames
merged_df = merge_dataframes(transacciones_df, clientes_df, inventario_df)

# Imprimir columnas del DataFrame resultante
print("Columnas en merged_df después del merge:", merged_df.columns)

# Data original resultante
data = merged_df
