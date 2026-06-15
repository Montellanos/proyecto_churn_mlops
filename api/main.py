"""
API de predicción de churn con FastAPI.

La API carga un modelo serializado, valida los datos de entrada
y devuelve una predicción junto con su probabilidad.
"""

from pathlib import Path
import json

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "modelo_churn_v1.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "modelo_churn_v1_metadata.json"

VERSION_MODELO = "modelo_churn_v1"
VERSION_SERVICIO = "1.0.0"
AUTOR = "Jorge Montellanos Diaz"

METADATA = {}
if METADATA_PATH.exists():
    try:
        METADATA = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        METADATA = {}


if not MODEL_PATH.exists():
    raise RuntimeError(
        "No se encontró el modelo serializado. "
        "Ejecute primero: python src\\entrenar_modelo.py"
    )

modelo = joblib.load(MODEL_PATH)


class ClienteEntrada(BaseModel):
    antiguedad: int = Field(
        ...,
        ge=0,
        le=120,
        description="Antigüedad del cliente expresada en meses",
        examples=[12],
    )
    cargo_mensual: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Cargo mensual del cliente",
        examples=[95.5],
    )
    reclamos: int = Field(
        ...,
        ge=0,
        le=50,
        description="Cantidad de reclamos recientes",
        examples=[3],
    )

    @model_validator(mode="after")
    def validar_coherencia(cls, values):
        antiguedad = values.antiguedad
        cargo_mensual = values.cargo_mensual
        reclamos = values.reclamos

        if antiguedad == 0 and cargo_mensual > 900:
            raise ValueError(
                "Con antiguedad 0 no se espera cargo_mensual mayor a 900."
            )

        if cargo_mensual == 0 and reclamos > 0:
            raise ValueError(
                "Si cargo_mensual es 0, no puede haber reclamos."
            )

        return values


class PrediccionSalida(BaseModel):
    prediccion: str
    probabilidad: float
    nivel_riesgo: str
    descripcion: str
    recomendacion: str
    version_modelo: str
    autor: str


app = FastAPI(
    title="API de predicción de churn",
    description="Servicio académico ML-Ops para estimar riesgo de abandono.",
    version="1.0.0",
)


@app.get("/")
def inicio() -> dict[str, str]:
    return {
        "mensaje": "Servicio ML-Ops activo",
        "estado": "ok",
        "autor": "Jorge Montellanos Diaz"
    }


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "estado": "ok",
        "modelo": VERSION_MODELO,
        "modelo_disponible": VERSION_MODELO,
    }


@app.get("/info")
def info() -> dict[str, object]:
    return {
        "version_modelo": VERSION_MODELO,
        "version_servicio": VERSION_SERVICIO,
        "autor": AUTOR,
        "variables": ["antiguedad", "cargo_mensual", "reclamos"],
        "fecha_entrenamiento": METADATA.get("fecha_entrenamiento", "desconocida"),
        "descripcion": "Endpoint informativo del modelo de churn",
    }


@app.post("/predict", response_model=PrediccionSalida)
def predict(datos: ClienteEntrada) -> PrediccionSalida:
    try:
        X = [[
            datos.antiguedad,
            datos.cargo_mensual,
            datos.reclamos,
        ]]

        probabilidad = float(modelo.predict_proba(X)[0][1])
        probabilidad_redondeada = round(probabilidad, 4)
        etiqueta = "alto_riesgo" if probabilidad >= 0.50 else "bajo_riesgo"

        if probabilidad >= 0.75:
            nivel_riesgo = "alto"
            descripcion = "El cliente presenta riesgo elevado de churn."
            recomendacion = "Priorizar retención con incentivos o contacto proactivo."
        elif probabilidad >= 0.50:
            nivel_riesgo = "medio"
            descripcion = "El cliente presenta riesgo moderado de churn."
            recomendacion = "Monitorear su comportamiento y ofrecer beneficios si aumenta el riesgo."
        else:
            nivel_riesgo = "bajo"
            descripcion = "El cliente presenta riesgo bajo de churn."
            recomendacion = "Mantener seguimiento habitual y enfocarse en fidelización."

        return PrediccionSalida(
            prediccion=etiqueta,
            probabilidad=probabilidad_redondeada,
            nivel_riesgo=nivel_riesgo,
            descripcion=descripcion,
            recomendacion=recomendacion,
            version_modelo=VERSION_MODELO,
            autor=AUTOR,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible generar la predicción.",
        ) from exc