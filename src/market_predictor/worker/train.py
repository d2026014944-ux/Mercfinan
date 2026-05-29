from __future__ import annotations

import torch
from torch import nn
from torch.optim import Adam

from market_predictor.ml.model import MarketPredictor
from market_predictor.ml.preprocessing import normalize_window


class TrainingPipeline:
    def __init__(self, learning_rate: float = 1e-3) -> None:
        self.model = MarketPredictor()
        self.loss_fn = nn.MSELoss()
        self.optimizer = Adam(self.model.parameters(), lr=learning_rate)

    def train_step(self, values: list[float], target: float) -> float:
        normalized = normalize_window(values)
        features = torch.tensor(normalized, dtype=torch.float32).unsqueeze(0)
        expected = torch.tensor([[target]], dtype=torch.float32)

        self.model.train()
        prediction = self.model(features)
        loss = self.loss_fn(prediction, expected)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return float(loss.detach().item())
