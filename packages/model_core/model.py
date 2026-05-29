from __future__ import annotations

import torch
from torch import nn

from model_core.input_schema import MODEL_INPUT_SIZE


class MarketPredictor(nn.Module):
    def __init__(self, input_size: int = MODEL_INPUT_SIZE) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features)


def create_model(input_size: int = MODEL_INPUT_SIZE) -> MarketPredictor:
    model = MarketPredictor(input_size=input_size)
    model.eval()
    return model
