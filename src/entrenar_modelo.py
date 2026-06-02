from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

TRAIN_DATA = DATA_DIR / "train.csv"
MODEL_FILE = MODELS_DIR / "modelo_churn.pkl"


def obtener_modelo(algoritmo: str = "logistic") -> Pipeline:
    """Construye un pipeline de modelo según el algoritmo seleccionado."""

    if algoritmo == "random_forest":
        clasificador = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
    else:
        clasificador = LogisticRegression(
            solver="liblinear",
            C=0.5,
            random_state=42,
            max_iter=1000
        )

    return Pipeline(
        steps=[
            ("escalado", StandardScaler()),
            ("clasificador", clasificador)
        ]
    )


def entrenar_modelo(algoritmo: str = "logistic"):
    """
    Entrena un modelo de clasificación para predecir churn.

    Parámetros:
    - algoritmo: "logistic" o "random_forest".
    """

    if not TRAIN_DATA.exists():
        raise FileNotFoundError(
            "No se encontró data/train.csv. Primero ejecuta src/preparar_datos.py"
        )

    MODELS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(TRAIN_DATA)

    X = df.drop(columns=["churn"])
    y = df["churn"]

    modelo = obtener_modelo(algoritmo)
    modelo.fit(X, y)

    joblib.dump(modelo, MODEL_FILE)

    print("Modelo entrenado correctamente.")
    print(f"Algoritmo entrenado: {algoritmo}")
    print(f"Modelo guardado en: {MODEL_FILE}")


if __name__ == "__main__":
    entrenar_modelo()
