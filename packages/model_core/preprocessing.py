from __future__ import annotations

from typing import Sequence


def normalize_window(values: Sequence[float]) -> list[float]:
    if not values:
        raise ValueError("values must not be empty")

    minimum = min(values)
    maximum = max(values)

    if minimum == maximum:
        return [0.0 for _ in values]

    span = maximum - minimum
    return [(value - minimum) / span for value in values]
