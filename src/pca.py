# data_pca.py
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

def perform_pca(df, n_components=2):
    """
    Realiza PCA en los datos de precios y muestra los componentes principales.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de precios.
        n_components (int): Número de componentes principales a extraer.
    
    Returns:
        pd.DataFrame: DataFrame transformado con los componentes principales.
    """
    # Seleccionar columnas de precios para PCA
    price_columns = ['Precio Virgen extra', 'Precio Virgen', 'Precio Lampante']
    
    # Eliminar filas con valores nulos en las columnas de precios
    df = df.dropna(subset=price_columns)
    
    # Aplicar PCA
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(df[price_columns])
    
    # Crear un DataFrame con los componentes principales
    pca_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])
    pca_df = pd.concat([pca_df, df[['Fecha']]], axis=1)
    
    # Visualización de los primeros dos componentes principales
    plt.figure(figsize=(14, 8))
    sns.scatterplot(x='PC1', y='PC2', data=pca_df, hue=df['Fecha'].dt.year, palette='viridis', legend='full')
    plt.title('PCA de Precios del Aceite de Oliva')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.legend(title='Año')
    plt.show()
    
    # Explicar la varianza
    explained_variance = pca.explained_variance_ratio_
    print(f'Varianza explicada por cada componente principal: {explained_variance}')
    
    return pca_df, explained_variance
