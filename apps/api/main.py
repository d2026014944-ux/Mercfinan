from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from model_core.inference import InferenceService
from model_core.input_schema import MODEL_INPUT_SIZE

app = FastAPI(title="Market Predictor")
inference_service = InferenceService()


class PredictionRequest(BaseModel):
    values: list[float] = Field(min_length=MODEL_INPUT_SIZE, max_length=MODEL_INPUT_SIZE)


class PredictionResponse(BaseModel):
    prediction: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    return PredictionResponse(prediction=inference_service.predict(payload.values))
