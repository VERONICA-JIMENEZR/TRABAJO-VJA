import pandas as pd
from tranfroma import data
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

# Crear un DataFrame para el análisis de segmentación
df_segmentacion = data.groupby('ID cliente').agg({
    'Cantidad': 'sum',
    'Precio final': 'sum'
}).rename(columns={'Cantidad': 'Total_Cantidad', 'Precio final': 'Valor_Monetario'})

# Aplicar el algoritmo K-means para segmentación
kmeans = KMeans(n_clusters=4, random_state=42)
df_segmentacion['Segmento'] = kmeans.fit_predict(df_segmentacion)

# Visualizar los segmentos
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_segmentacion, x='Total_Cantidad', y='Valor_Monetario', hue='Segmento', palette='Set1')
plt.title('Segmentación de Clientes')
plt.xlabel('Cantidad Total')
plt.ylabel('Valor Monetario')
plt.legend(title='Segmento')
plt.show()
