from __future__ import annotations

from typing import Sequence

MODEL_INPUT_SIZE = 4


def ensure_window_size(values: Sequence[float]) -> list[float]:
    if len(values) != MODEL_INPUT_SIZE:
        raise ValueError(
            f"expected {MODEL_INPUT_SIZE} values for the model input, received {len(values)}"
        )
    return list(values)
