# random_forest_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

def train_random_forest(df, target_column, test_size=0.2, random_state=42):
    """
    Entrena un modelo de Random Forest para predecir los precios del aceite de oliva.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos de precios.
        target_column (str): Nombre de la columna objetivo (precio a predecir).
        test_size (float): Proporción del conjunto de datos para el conjunto de prueba.
        random_state (int): Semilla para la reproducibilidad.
    
    Returns:
        dict: Diccionario con las predicciones, el modelo entrenado y las métricas.
    """
    # Crear variables independientes (features) y la variable dependiente (target)
    features = df.drop(columns=['Fecha', target_column])
    target = df[target_column]
    
    # Dividir el conjunto de datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size, random_state=random_state)
    
    # Crear y entrenar el modelo Random Forest
    model = RandomForestRegressor(random_state=random_state)
    model.fit(X_train, y_train)
    
    # Realizar predicciones
    predictions = model.predict(X_test)
    
    # Calcular métricas de evaluación
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    
    # Visualizar resultados
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    plt.xlabel('Valores Reales')
    plt.ylabel('Predicciones')
    plt.title(f'Random Forest - Predicción de {target_column}')
    plt.show()
    
    # Retornar el modelo entrenado y las métricas
    return {
        "model": model,
        "predictions": predictions,
        "mse": mse,
        "rmse": rmse,
        "r2": r2
    }
