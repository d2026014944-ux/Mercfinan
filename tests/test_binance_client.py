import pandas as pd
import pytest

from database.binance_client import BinanceClient


class _StubResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


class _StubHttpClient:
    def __init__(self, payload):
        self._payload = payload
        self.request = None

    def get(self, url, params=None, timeout=None):
        self.request = {"url": url, "params": params, "timeout": timeout}
        return _StubResponse(self._payload)


def test_get_ohlcv_converts_klines_to_dataframe() -> None:
    payload = [
        [
            1716854400000,
            "68000.0",
            "68100.0",
            "67950.0",
            "68050.0",
            "12.34",
            1716854459999,
            "0",
            0,
            "0",
            "0",
            "0",
        ],
        [
            1716854460000,
            "68050.0",
            "68200.0",
            "68000.0",
            "68150.0",
            "15.67",
            1716854519999,
            "0",
            0,
            "0",
            "0",
            "0",
        ],
    ]
    http_client = _StubHttpClient(payload)

    client = BinanceClient(http_client=http_client)

    df = client.get_ohlcv("BTCUSDT", interval="1m", limit=2)

    assert http_client.request is not None
    assert http_client.request["params"] == {"symbol": "BTCUSDT", "interval": "1m", "limit": 2}
    assert http_client.request["url"].endswith("/api/v3/klines")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 2
    assert isinstance(df.index, pd.DatetimeIndex)

    expected_index = pd.to_datetime([1716854400000, 1716854460000], unit="ms", utc=True)
    assert pd.to_datetime(df.index, utc=True).view("int64").tolist() == expected_index.view("int64").tolist()

    expected_values = {
        "open": [68000.0, 68050.0],
        "high": [68100.0, 68200.0],
        "low": [67950.0, 68000.0],
        "close": [68050.0, 68150.0],
        "volume": [12.34, 15.67],
    }
    for column, values in expected_values.items():
        assert df[column].tolist() == pytest.approx(values)
        assert pd.api.types.is_float_dtype(df[column])
