import pandas as pd
from carga_dato import clientes_df, inventario_df, transacciones_df

# Submuestreo aleatorio para reducir el tamaño de los DataFrames
clientes_df = clientes_df.sample(n=1000)
inventario_df = inventario_df.sample(n=1000)
transacciones_df = transacciones_df.sample(n=1000)
#print("Columnas en clientes_df:", clientes_df.columns)
#print("Tamaño de clientes_df:", clientes_df.shape)

#print("Columnas en inventario_df:", inventario_df.columns)
#print("Tamaño de inventario_df:", inventario_df.shape)

#print("Columnas en transacciones_df:", transacciones_df.columns)
#print("Tamaño de transacciones_df:", transacciones_df.shape)

merged_df = pd.merge(transacciones_df, clientes_df, on='ID cliente')
merged_df = pd.merge(merged_df, inventario_df, on='ID producto')

merged_df = merged_df.iloc[:, :-3]
print("Columnas en merged_df después del merge:", merged_df.columns)
#print("Tamaño de merged_df:", merged_df.shape)
#print(merged_df.isnull().any())
#Data orininal

data=merged_df