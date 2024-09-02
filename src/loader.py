import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ast
import time

def extract_data_from_chart(url, start_date, end_date):
    """
    Extrae los datos del gráfico para un rango de fechas específico.
    
    Args:
        url (str): La URL de la página web donde está el gráfico.
        start_date (str): La fecha de inicio en formato 'YYYY-MM-DD'.
        end_date (str): La fecha de fin en formato 'YYYY-MM-DD'.
    
    Returns:
        pd.DataFrame: DataFrame con las fechas y precios para el rango especificado.
    """
    
    # Configuración del WebDriver (usando Chrome en este ejemplo)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar en modo headless (sin ventana gráfica)
    driver = webdriver.Chrome(options=options)
    
    try:
        # Accede a la página web
        driver.get(url)
        
        # Espera a que el overlay esté presente y cierra el overlay si es necesario
        wait = WebDriverWait(driver, 10)
        try:
            # Espera y encuentra el botón para cerrar el overlay
            close_overlay_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.cc-nb-reject')))
            print("Overlay detectado, intentando cerrarlo...")
            close_overlay_button.click()
            time.sleep(3)  # Espera para asegurarse de que el overlay ha desaparecido
        except Exception as e:
            print(f"No se pudo encontrar o cerrar el overlay: {e}")
        
        # Espera a que el botón 'Elegir fechas' sea visible e interactuable
        elegir_fechas_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-years="-1"]')))
        
        # Desplazar el botón a la vista para asegurarse de que se puede hacer clic
        driver.execute_script("arguments[0].scrollIntoView(true);", elegir_fechas_button)
        
        # Hacer clic en el botón 'Elegir fechas'
        elegir_fechas_button.click()
        
        # Espera a que los campos de fecha sean visibles e interactuables
        fecha_ini_input = wait.until(EC.element_to_be_clickable((By.ID, 'fecha_ini')))
        fecha_fin_input = wait.until(EC.element_to_be_clickable((By.ID, 'fecha_fin')))
        time.sleep(1)
        
        # Establece las fechas en los campos de entrada
        fecha_ini_input.clear()
        fecha_ini_input.send_keys(start_date)
        
        time.sleep(1)
        fecha_fin_input.clear()
        fecha_fin_input.send_keys(end_date)
        time.sleep(1)
        
        # Clic en un elemento fuera de los campos de entrada para aplicar las fechas
        body = driver.find_element(By.TAG_NAME, 'body')
        body.click()
        
        # Espera a que el gráfico se actualice
        time.sleep(6)  # Ajusta el tiempo según sea necesario
        
        # Extrae los datos para cada línea (datasets[0], datasets[1], datasets[2])
        data_line_1 = driver.execute_script('return myChart.data.datasets[0].data')
        data_line_2 = driver.execute_script('return myChart.data.datasets[1].data')
        data_line_3 = driver.execute_script('return myChart.data.datasets[2].data')
        
        # Extrae las etiquetas (nombre de las líneas)
        label_line_1 = driver.execute_script('return myChart.data.datasets[0].label')
        label_line_2 = driver.execute_script('return myChart.data.datasets[1].label')
        label_line_3 = driver.execute_script('return myChart.data.datasets[2].label')
        
        # Asegúrate de que todas las fechas están presentes en cada conjunto de datos
        fechas = set(ast.literal_eval(str(item))['x'] for item in data_line_1)
        fechas.update(ast.literal_eval(str(item))['x'] for item in data_line_2)
        fechas.update(ast.literal_eval(str(item))['x'] for item in data_line_3)
        fechas = sorted(fechas)
        
        # Crea un DataFrame para almacenar los datos alineados
        df = pd.DataFrame({'Fecha': fechas})
        
        def extract_prices(data, fechas):
            prices = []
            data_dict = {ast.literal_eval(str(item))['x']: float(ast.literal_eval(str(item))['y']) for item in data}
            for fecha in fechas:
                prices.append(data_dict.get(fecha, None))  # Usar None para los valores faltantes
            return prices
        
        # Añade precios al DataFrame para cada línea
        df[f'Precio {label_line_1}'] = extract_prices(data_line_1, fechas)
        df[f'Precio {label_line_2}'] = extract_prices(data_line_2, fechas)
        df[f'Precio {label_line_3}'] = extract_prices(data_line_3, fechas)
        
        return df
    
    finally:
        # Cierra el navegador
        driver.quit()

def save_data_to_csv(df, file_path):
    """
    Guarda los datos en un archivo CSV.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de las tres líneas.
        file_path (str): Ruta del archivo CSV donde se guardarán los datos.
    """
    df.to_csv(file_path, index=False)
    print(f'Datos guardados en {file_path}')

def download_data_for_dates(url, year, redownload, folder_path='data'):
    """
    Descarga los datos para un rango de fechas y guarda en archivo CSV.
    
    Args:
        url (str): La URL de la página web donde está el gráfico.
        year (int): El año que se desea descargar
        folder_path (str): Carpeta donde guardar los archivos CSV.
    """
    
    start_date = f'01/01/{year}'
    end_date = f'31/12/{year}'

    # Asegurarse de que el directorio de destino exista
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Formatear las fechas para el nombre del archivo
    formatted_start_date = start_date.replace('/', '_')
    formatted_end_date = end_date.replace('/', '_')
    
    # Crear el nombre del archivo
    file_name = f"{folder_path}/olive_prices_{year}.csv"
    
    if not os.path.exists(file_name):
        print(f"Descargando datos desde {start_date} hasta {end_date}...")
        df = extract_data_from_chart(url, start_date, end_date)
        save_data_to_csv(df, file_name)
    elif redownload:
        print(f'El archivo {file_name} ya existe. ¿Deseas descargarlo nuevamente?')
        opcion = input("(S)i/(N)o: ")
        if (opcion.lower() == 's') or (opcion.lower() == 'si') or (opcion.lower() == 'sí'):
            print(f"Descargando datos desde {start_date} hasta {end_date}...")
            df = extract_data_from_chart(url, start_date, end_date)
            save_data_to_csv(df, file_name)
        else:
            print("No se descargarán nuevos datos")
        
    
    return file_name
