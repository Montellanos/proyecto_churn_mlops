from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

RAW_DATA = DATA_DIR / "churn_clientes.csv"
TRAIN_DATA = DATA_DIR / "train.csv"
TEST_DATA = DATA_DIR / "test.csv"


def crear_dataset_demo():
    """
    Crea un dataset pequeño de ejemplo para la práctica.
    Este dataset permite ejecutar el flujo inicial sin descargar datos externos.
    """

    datos = [
        {"edad": 25, "antiguedad": 6, "cargo_mensual": 120.0, "reclamos": 3, "usa_app": 0, "churn": 1},
        {"edad": 34, "antiguedad": 24, "cargo_mensual": 350.0, "reclamos": 0, "usa_app": 1, "churn": 0},
        {"edad": 45, "antiguedad": 36, "cargo_mensual": 500.0, "reclamos": 1, "usa_app": 1, "churn": 0},
        {"edad": 22, "antiguedad": 4, "cargo_mensual": 80.0, "reclamos": 4, "usa_app": 0, "churn": 1},
        {"edad": 52, "antiguedad": 60, "cargo_mensual": 700.0, "reclamos": 0, "usa_app": 1, "churn": 0},
        {"edad": 29, "antiguedad": 8, "cargo_mensual": 150.0, "reclamos": 2, "usa_app": 0, "churn": 1},
        {"edad": 40, "antiguedad": 30, "cargo_mensual": 420.0, "reclamos": 1, "usa_app": 1, "churn": 0},
        {"edad": 31, "antiguedad": 10, "cargo_mensual": 160.0, "reclamos": 3, "usa_app": 0, "churn": 1},
        {"edad": 48, "antiguedad": 48, "cargo_mensual": 600.0, "reclamos": 0, "usa_app": 1, "churn": 0},
        {"edad": 27, "antiguedad": 7, "cargo_mensual": 110.0, "reclamos": 4, "usa_app": 0, "churn": 1},
        {"edad": 36, "antiguedad": 26, "cargo_mensual": 390.0, "reclamos": 1, "usa_app": 1, "churn": 0},
        {"edad": 23, "antiguedad": 5, "cargo_mensual": 90.0, "reclamos": 5, "usa_app": 0, "churn": 1},
        {"edad": 55, "antiguedad": 72, "cargo_mensual": 820.0, "reclamos": 0, "usa_app": 1, "churn": 0},
        {"edad": 33, "antiguedad": 14, "cargo_mensual": 210.0, "reclamos": 2, "usa_app": 0, "churn": 1},
        {"edad": 41, "antiguedad": 33, "cargo_mensual": 460.0, "reclamos": 0, "usa_app": 1, "churn": 0},
        {"edad": 30, "antiguedad": 9, "cargo_mensual": 130.0, "reclamos": 3, "usa_app": 0, "churn": 1},
    ]

    df = pd.DataFrame(datos)
    df.to_csv(RAW_DATA, index=False)


def preparar_datos():
    """
    Prepara los datos para entrenamiento y prueba.
    """

    DATA_DIR.mkdir(exist_ok=True)

    # Forzamos la creación del dataset para asegurar que las columnas
    # coincidan con la versión actual (antiguedad, cargo_mensual)
    crear_dataset_demo()

    df = pd.read_csv(RAW_DATA)

    df = df.drop_duplicates()
    df = df.dropna()

    train_df, test_df = train_test_split(
        df,
        test_size=0.25,
        random_state=42,
        stratify=df["churn"]
    )

    train_df.to_csv(TRAIN_DATA, index=False)
    test_df.to_csv(TEST_DATA, index=False)

    print("Datos preparados correctamente.")
    print(f"Archivo de entrenamiento: {TRAIN_DATA}")
    print(f"Archivo de prueba: {TEST_DATA}")


if __name__ == "__main__":
    preparar_datos()
