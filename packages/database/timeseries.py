from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketPoint:
    timestamp: str
    close: float


class TimescaleReadRepository:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    def build_recent_prices_query(self, limit: int = 128) -> str:
        if limit <= 0:
            raise ValueError("limit must be positive")

        return (
            "SELECT ts, close "
            "FROM market_prices "
            "WHERE symbol = %(symbol)s "
            "ORDER BY ts DESC "
            f"LIMIT {limit};"
        )
