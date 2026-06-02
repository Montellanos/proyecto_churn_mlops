from pathlib import Path

import joblib
import pandas as pd
from fastapi.testclient import TestClient
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import api.main as main


client = TestClient(main.app)


def test_inicio():
    response = client.get("/")

    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert "estado" in response.json()
    assert "modelo_disponible" in response.json()


def test_predict_with_model(monkeypatch, tmp_path):
    modelo = Pipeline(
        steps=[
            ("escalado", StandardScaler()),
            (
                "clasificador",
                LogisticRegression(solver="liblinear", C=1.0, random_state=42),
            ),
        ]
    )

    X = pd.DataFrame(
        [
            {
                "edad": 30,
                "antiguedad_meses": 12,
                "saldo_promedio": 1000.0,
                "reclamos": 0,
                "usa_app": 1,
            }
        ]
    )

    modelo.fit(X, [0])

    modelo_path = tmp_path / "modelo_churn.pkl"
    joblib.dump(modelo, modelo_path)
    monkeypatch.setattr(main, "MODEL_FILE", modelo_path)

    response = client.post(
        "/predict",
        json={
            "edad": 30,
            "antiguedad_meses": 12,
            "saldo_promedio": 1000.0,
            "reclamos": 0,
            "usa_app": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["churn_predicho"] in {0, 1}
    assert isinstance(response.json()["probabilidad_churn"], float)
