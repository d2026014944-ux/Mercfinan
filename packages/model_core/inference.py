from __future__ import annotations

import torch

from model_core.input_schema import ensure_window_size
from model_core.model import create_model
from model_core.preprocessing import normalize_window


class InferenceService:
    def __init__(self) -> None:
        self._model = create_model()

    def predict(self, values: list[float]) -> float:
        ensure_window_size(values)
        normalized = normalize_window(values)
        features = torch.tensor(normalized, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            prediction = self._model(features)
        return float(prediction.squeeze().item())
