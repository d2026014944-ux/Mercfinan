from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from typing import Sequence

from database.binance_client import BinanceClient
from model_core.input_schema import MODEL_INPUT_SIZE

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WorkerSettings:
    symbol: str = os.getenv("SYMBOL", "BTCUSDT")
    interval: str = os.getenv("INTERVAL", "1m")
    window_size: int = MODEL_INPUT_SIZE
    poll_interval: float = float(os.getenv("POLL_INTERVAL", "30"))


def build_feature_window(closes: Sequence[float], window_size: int) -> list[float]:
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if len(closes) < window_size:
        raise ValueError("not enough close prices to build a feature window")
    return [float(value) for value in closes[-window_size:]]


def fetch_latest_window(client: BinanceClient, settings: WorkerSettings) -> list[float]:
    frame = client.get_ohlcv(settings.symbol, interval=settings.interval, limit=settings.window_size)
    return build_feature_window(frame["close"].tolist(), settings.window_size)


def run_loop(settings: WorkerSettings) -> None:
    client = BinanceClient()
    while True:
        window = fetch_latest_window(client, settings)
        logger.info("Fetched %d close prices for %s", len(window), settings.symbol)
        time.sleep(settings.poll_interval)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = WorkerSettings()
    run_loop(settings)


if __name__ == "__main__":
    main()
