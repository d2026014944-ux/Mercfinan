from __future__ import annotations

from typing import Any

import httpx
import pandas as pd


class BinanceClient:
    def __init__(self, http_client: Any | None = None, base_url: str = "https://api.binance.com") -> None:
        self._http_client = http_client or httpx.Client()
        self._base_url = base_url.rstrip("/")

    def get_ohlcv(self, symbol: str, interval: str = "1m", limit: int = 500) -> pd.DataFrame:
        response = self._http_client.get(
            f"{self._base_url}/api/v3/klines",
            params={"symbol": symbol, "interval": interval, "limit": limit},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()

        columns = ["open_time", "open", "high", "low", "close", "volume"]
        records = [
            {
                "open_time": row[0],
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5]),
            }
            for row in payload
        ]

        frame = pd.DataFrame(records, columns=columns)
        frame.index = pd.to_datetime(frame.pop("open_time"), unit="ms", utc=True)
        return frame
