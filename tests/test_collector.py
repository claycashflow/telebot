import sys
from types import SimpleNamespace

import pandas as pd

from app.infrastructure import collector


class _HistoryOnlyTicker:
    @property
    def fast_info(self):
        return {}

    def history(self, period: str):
        return pd.DataFrame({"Close": [4.501, 4.522]})


def test_us_10y_yield_uses_yahoo_history_fallback(monkeypatch):
    monkeypatch.setattr(collector.yf, "Ticker", lambda _: _HistoryOnlyTicker())

    value, source = collector._get_us_10y_yield("")

    assert value == 4.52
    assert source == "Yahoo ^TNX (Real-time Market; history_fallback)"


class _BrokenYahooTicker:
    @property
    def fast_info(self):
        raise RuntimeError("fast info unavailable")

    def history(self, period: str):
        raise RuntimeError("history unavailable")


class _FakeFred:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_series(self, series_id: str):
        assert series_id == "DGS10"
        return pd.Series([4.47])


def test_us_10y_yield_falls_back_to_fred_with_reason(monkeypatch):
    monkeypatch.setattr(collector.yf, "Ticker", lambda _: _BrokenYahooTicker())
    monkeypatch.setitem(sys.modules, "fredapi", SimpleNamespace(Fred=_FakeFred))

    value, source = collector._get_us_10y_yield("test-key")

    assert value == 4.47
    assert source.startswith("FRED DGS10 (Daily/Delayed; Yahoo fallback:")
    assert "fast_info_error=RuntimeError" in source
    assert "history_error=RuntimeError" in source
