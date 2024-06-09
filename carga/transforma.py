import pandas as pd
from carga_dato import clientes_df, inventario_df, transacciones_df

def submuestreo_aleatorio(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Realiza un submuestreo aleatorio del DataFrame dado.

    Args:
        df (pd.DataFrame): DataFrame a submuestrear.
        n (int): Número de muestras a obtener.

    Returns:
        pd.DataFrame: DataFrame submuestreado.
    """
    return df.sample(n=n)

# Submuestreo aleatorio para reducir el tamaño de los DataFrames
clientes_df = submuestreo_aleatorio(clientes_df, 1000)
inventario_df = submuestreo_aleatorio(inventario_df, 1000)
transacciones_df = submuestreo_aleatorio(transacciones_df, 1000)

def merge_dataframes(transacciones_df: pd.DataFrame, clientes_df: pd.DataFrame, inventario_df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza la unión de los DataFrames de transacciones, clientes e inventario.

    Args:
        transacciones_df (pd.DataFrame): DataFrame de transacciones.
        clientes_df (pd.DataFrame): DataFrame de clientes.
        inventario_df (pd.DataFrame): DataFrame de inventario.

    Returns:
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
