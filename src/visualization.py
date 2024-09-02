import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import seaborn as sns

def plot_prices(df, year, save=False):
    """
    Crea gráficos de los precios en función de la fecha.

    Args:
        df (pd.DataFrame): DataFrame con los datos a graficar.
        year (int): Año de los datos.
        save (bool): Si True, guarda el gráfico en un archivo.
    """
    plt.figure(figsize=(14, 8))
    
    # Convertir la columna de fechas a datetime si no se ha hecho ya
    if not pd.api.types.is_datetime64_any_dtype(df['Fecha']):
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df = df.dropna(subset=['Fecha'])  # Eliminar filas con fechas inválidas

    # Graficar cada línea de datos
    for column in df.columns:
        if column != 'Fecha':
            plt.plot(df['Fecha'], df[column], label=column)
    
    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.title('Precio del Aceite de Oliva (€/kg)')
    plt.legend()
    
    # Configuración del eje x para mejorar la legibilidad
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Rotar fechas para evitar solapamientos
    
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(f'plots/olive_prices_{year}.png')
    plt.show()

def plot_prices_with_trend(df, year, save=False):
    """
    Crea gráficos de los precios en función de la fecha con líneas de tendencia.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos a graficar.
        year (int): Año de los datos.
        save (bool): Si True, guarda el gráfico en un archivo.
    """
    plt.figure(figsize=(14, 8))
    
    # Convertir la columna de fechas a datetime si no se ha hecho ya
    if not pd.api.types.is_datetime64_any_dtype(df['Fecha']):
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df = df.dropna(subset=['Fecha'])  # Eliminar filas con fechas inválidas

    # Graficar precios
    for column in df.columns:
        if column not in ['Fecha', 'Mes', 'Precio']:
            plt.plot(df['Fecha'], df[column], label=column)
            
            # Ajustar línea de tendencia
            z = np.polyfit(mdates.date2num(df['Fecha']), df[column], 1)
            p = np.poly1d(z)
            plt.plot(df['Fecha'], p(mdates.date2num(df['Fecha'])), linestyle='--', label=f'Tendencia {column}')

    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.title('Precios del Aceite de Oliva con Líneas de Tendencia (€/kg)')
    plt.legend()
    
    # Configuración del eje x para mejorar la legibilidad
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Rotar fechas para evitar solapamientos
    
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(f'plots/olive_prices_trend_{year}.png')
    plt.show()

def plot_heatmap(df, year, save=False):
    """
    Crea un mapa de calor de los precios mensuales.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos a graficar.
        year (int): Año de los datos.
        save (bool): Si True, guarda el gráfico en un archivo.
    """
    # Preparar datos para el heatmap
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Mes'] = df['Fecha'].dt.month
    df['Precio'] = df['Precio Virgen extra']  # Seleccionar columna de precio
    
    # Pivotear datos para el heatmap
    pivot_df = df.pivot_table(index='Mes', columns='Fecha', values='Precio', aggfunc='mean')
    
    # Crear heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df, annot=True, fmt='.2f', cmap='YlGnBu', cbar=True)
    
    # Personalizar título y etiquetas
    plt.title(f'Mapa de Calor de Precios Mensuales ({year})')
    plt.xlabel('Fecha')
    plt.ylabel('Mes')
    
    # Guardar gráfico si se especifica
    if save:
        plt.savefig(f'plots/olive_prices_heatmap_{year}.png')
    
    # Mostrar gráfico
    plt.show()