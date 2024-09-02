import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def perform_clustering(df, n_clusters=3):
    """
    Realiza un clustering K-Means en los datos de precios y muestra resultados.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de precios.
        n_clusters (int): Número de clusters para K-Means.
    
    Returns:
        pd.DataFrame: DataFrame original con una columna adicional indicando el cluster.
    """
    # Seleccionar columnas de precios para el clustering
    price_columns = ['Precio Virgen extra', 'Precio Virgen', 'Precio Lampante']
    
    # Eliminar filas con valores nulos en las columnas de precios
    df = df.dropna(subset=price_columns)
    
    # Aplicar el algoritmo K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df[price_columns])
    
    # Visualización de los clusters
    plt.figure(figsize=(14, 8))
    sns.scatterplot(x='Fecha', y='Precio Virgen extra', hue='Cluster', data=df, palette='viridis')
    plt.title('Agrupamiento de Precios del Aceite de Oliva (Virgen Extra) usando K-Means')
    plt.xlabel('Fecha')
    plt.ylabel('Precio Virgen Extra')
    plt.legend(title='Cluster')
    plt.show()
    
    return df
