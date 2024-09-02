import pandas as pd
import os

def load_data_from_folder(folder_path='data'):
    """
    Carga todos los archivos CSV desde una carpeta y los combina en un solo DataFrame.
    
    Args:
        folder_path (str): Ruta de la carpeta donde están los archivos CSV.
    
    Returns:
        pd.DataFrame: DataFrame combinado con todos los datos.
    """
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = []
    
    for file in all_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def preprocess_data(df):
    """
    Preprocesa los datos, incluyendo la conversión de tipos de datos y la limpieza.
    """
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df.sort_values(by='Fecha', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df