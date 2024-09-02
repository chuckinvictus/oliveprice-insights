# OlivePrice Insights

Este proyecto está diseñado para analizar los precios del aceite de oliva en origen, utilizando datos históricos desde 2012 hasta la actualidad. Las herramientas incluyen visualización de datos, análisis de componentes principales (PCA), clustering, y predicción mediante Random Forest.

## Estructura del Proyecto

```bash
├── data/                     # Carpeta donde se almacenan los archivos CSV de datos
├── src/
│   ├── loader.py             # Funciones para descargar datos
│   ├── visualization.py      # Funciones para la visualización de datos
│   ├── pca.py                # Análisis de Componentes Principales (PCA)
│   ├── clustering.py         # Funciones para clustering (K-Means)
│   ├── prediction.py         # Predicción de precios usando Random Forest
│   ├── utils.py              # Funciones auxiliares para carga y preprocesamiento de datos
├── app.py                    # Archivo principal para ejecutar la aplicación
├── README.md                 # Documentación del proyecto
└── requirements.txt          # Lista de dependencias del proyecto
```

## Utilidad del Proyecto

El objetivo principal de este proyecto es proporcionar un conjunto de herramientas para el análisis exploratorio y predictivo de los precios del aceite de oliva, permitiendo a los usuarios:

- Visualizar tendencias históricas de los precios.
- Realizar análisis de componentes principales para entender la variabilidad en los datos.
- Agrupar los precios utilizando técnicas de clustering.
- Predecir precios futuros utilizando modelos de machine learning, específicamente Random Forest.

## Cómo Ejecutarlo

1. **Clona el Repositorio**:

   ```bash
   git clone https://github.com/chuckinvictus/oliveprice-insights
   cd oliveprice-insights
   ```

2. **Instala las Dependencias**:

   Asegúrate de tener `pip` instalado y ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la Aplicación**:

   Para analizar y visualizar los datos de precios, ejecuta:

   ```bash
   python app.py
   ```

   Este comando cargará los datos para el año especificado (o todos los años si se selecciona el histórico completo), preprocesará los datos, y realizará análisis de PCA, clustering, y predicción usando Random Forest.

   Para cambiar el año de análisis, modifica la variable `year` en el código.
