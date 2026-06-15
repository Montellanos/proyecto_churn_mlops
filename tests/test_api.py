from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_inicio():
    response = client.get("/")

    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert "estado" in response.json()
    assert "modelo_disponible" in response.json()


def test_info():
    response = client.get("/info")

    assert response.status_code == 200
    body = response.json()
    assert body["version_modelo"] == "modelo_churn_v1"
    assert body["version_servicio"] == "1.0.0"
    assert body["autor"] == "Jorge Montellanos Diaz"
    assert body["variables"] == ["antiguedad", "cargo_mensual", "reclamos"]
    assert "fecha_entrenamiento" in body


def test_predict_incoherente_antiguedad_cargo():
    response = client.post(
        "/predict",
        json={"antiguedad": 0, "cargo_mensual": 950.0, "reclamos": 1},
    )

    assert response.status_code == 422
    assert any(
        "cargo_mensual" in error["loc"] or "cargo_mensual" in error["msg"]
        for error in response.json()["detail"]
    )


def test_predict_incoherente_cargo_reclamos():
    response = client.post(
        "/predict",
        json={"antiguedad": 12, "cargo_mensual": 0.0, "reclamos": 2},
    )

    assert response.status_code == 422
    assert any(
        "reclamos" in error["loc"] or "cargo_mensual" in error["msg"]
        for error in response.json()["detail"]
    )


def test_predict_response_fields():
    response = client.post(
        "/predict",
        json={"antiguedad": 12, "cargo_mensual": 95.5, "reclamos": 3},
    )

    assert response.status_code == 200
    body = response.json()
    assert "prediccion" in body
    assert "probabilidad" in body
    assert "nivel_riesgo" in body
    assert "descripcion" in body
    assert "recomendacion" in body
    assert body["version_modelo"] == "modelo_churn_v1"
    assert body["autor"] == "Jorge Montellanos Diaz"
