# Proyecto Churn MLOps

Este proyecto corresponde a una práctica inicial del módulo de MLOps.

El objetivo es construir una estructura básica de trabajo para un proyecto de Machine Learning que permita:

- Preparar datos.
- Entrenar un modelo.
- Evaluar métricas.
- Guardar el modelo entrenado.
- Exponer el modelo mediante una API.
- Ejecutar pruebas básicas.

## Problema del proyecto

Se trabajará con un caso simplificado de predicción de abandono de clientes, conocido como churn.

El modelo intentará predecir si un cliente podría abandonar un servicio, utilizando variables como antigüedad, cargo mensual y reclamos.

## Estructura del proyecto

```text
proyecto_churn_mlops
├── data
├── notebooks
├── src
├── models
├── api
├── tests
├── docs
├── README.md
└── requirements.txt
```

## Carpetas principales

- `data`: contiene los datos del proyecto.
- `notebooks`: contiene análisis exploratorios.
- `src`: contiene los scripts principales del modelo.
- `models`: contiene el modelo entrenado.
- `api`: contiene la API del modelo.
- `tests`: contiene pruebas automáticas.
- `docs`: contiene documentación y métricas.

## Flujo inicial del proyecto

El flujo básico será:

1. Preparar los datos.
2. Entrenar el modelo.
3. Evaluar el modelo.
4. Guardar las métricas.
5. Crear una API básica.
6. Probar el funcionamiento inicial.

## Experimento adicional

Para este mini experimento se agregó soporte para un segundo algoritmo de clasificación, `RandomForestClassifier`, junto con un ajuste controlado de hiperparámetros.

También se amplió la evaluación del modelo para incluir la métrica AUC ROC, que mide la capacidad del clasificador para distinguir entre clientes con churn y sin churn.

El entrenamiento por defecto sigue siendo `LogisticRegression`, pero es posible probar el nuevo algoritmo con el parámetro `algoritmo="random_forest"` en `src/entrenar_modelo.py`.

## Uso de la API

Para ejecutar la API, levanta el servidor con Uvicorn:

```bash
d:/Github/proyecto_churn_mlops/.venv/Scripts/python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Endpoints principales:

- `GET /`: estado del servicio
- `GET /health`: estado y versión del modelo disponible
- `GET /info`: información del modelo, versión del servicio, autor, variables utilizadas y fecha de entrenamiento
- `POST /predict`: predicción de churn

El endpoint `GET /info` devuelve campos adicionales como:

- `version_modelo`
- `version_servicio`
- `autor`
- `variables`
- `fecha_entrenamiento`

Ejemplo de `POST /predict`:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"antiguedad": 12, "cargo_mensual": 95.5, "reclamos": 3}'
```

## Control de versiones

Este proyecto utiliza Git para registrar cambios y GitHub para respaldar el repositorio en la nube.

El uso de commits permite mantener trazabilidad sobre los cambios realizados en el código, la documentación y la estructura del proyecto.
