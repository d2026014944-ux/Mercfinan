from __future__ import annotations

import torch

from market_predictor.ml.model import create_model
from market_predictor.ml.preprocessing import normalize_window


class InferenceService:
    def __init__(self) -> None:
        self._model = create_model()

    def predict(self, values: list[float]) -> float:
        normalized = normalize_window(values)
        features = torch.tensor(normalized, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            prediction = self._model(features)
        return float(prediction.squeeze().item())
