from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from market_predictor.ml.inference import InferenceService

app = FastAPI(title="Market Predictor Alpha")
inference_service = InferenceService()


class PredictionRequest(BaseModel):
    values: list[float] = Field(min_length=4, max_length=4)


class PredictionResponse(BaseModel):
    prediction: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    return PredictionResponse(prediction=inference_service.predict(payload.values))
