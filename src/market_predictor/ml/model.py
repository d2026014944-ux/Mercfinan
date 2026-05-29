from __future__ import annotations

import torch
from torch import nn


class MarketPredictor(nn.Module):
    def __init__(self, input_size: int = 4) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features)


def create_model(input_size: int = 4) -> MarketPredictor:
    model = MarketPredictor(input_size=input_size)
    model.eval()
    return model
