from src.loader import download_data_for_dates
from src.utils import load_data_from_folder, preprocess_data
from src.visualization import plot_prices, plot_prices_with_trend
from src.clustering import perform_clustering
from src.pca import perform_pca
from src.prediction import train_random_forest

import pandas as pd
import os


def get_year_data(url, year):
    """
    Descarga o carga los datos de un año específico.
    """
    if year < 2012 or year > 2024:
        print(f"No hay datos disponibles para el año {year}. Introduzca un año válido.")
        return None

    filename = f"data/olive_prices_{year}.csv"
    if os.path.exists(filename):
        print(f"Cargando datos del archivo existente: {filename}")
        return pd.read_csv(filename)
    else:
        return pd.read_csv(download_data_for_dates(url, year, redownload=False))

def main():
    url = 'https://www.infaoliva.com'
    
    # Año para analizar (0 para mostrar el histórico completo)
    year = 2023

    if year == 0:
        df = load_data_from_folder('data')
    else:
        df = get_year_data(url, year)
    
    if df is None:
        print("No se pudieron cargar los datos.")
        return
    
    # Preprocesar los datos
    df = preprocess_data(df)
    
    # Mostrar precios
    plot_prices_with_trend(df, year)

    # Realizar clustering y mostrar resultados
    df_clustered = perform_clustering(df, n_clusters=4)
    plot_prices(df_clustered, year)

    # Realizar PCA y mostrar resultados
    pca_df, explained_variance = perform_pca(df, n_components=2)

    # Realizar Random Forest y mostrar resultados
    results = train_random_forest(df, target_column='Precio Virgen extra')
    print(f'MSE: {results["mse"]}, RMSE: {results["rmse"]}, R²: {results["r2"]}')


if __name__ == '__main__':
    main()
