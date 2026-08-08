from types import SimpleNamespace

import pytest

from tdi.adapters.mt5_market_data_adapter import (
    MT5MarketDataAdapter,
    MT5MarketDataError,
)


class FakeMT5:
    TIMEFRAME_H1 = 1
    TIMEFRAME_H4 = 4

    def __init__(self):
        self.initialized = False
        self.shutdown_called = False

    def initialize(self):
        self.initialized = True
        return True

    def shutdown(self):
        self.shutdown_called = True

    def copy_rates_from_pos(
        self,
        symbol,
        timeframe,
        start,
        count,
    ):
        return [
            {
                "time": 1767225600,
                "open": 100.0,
                "high": 105.0,
                "low": 98.0,
                "close": 103.0,
            },
            {
                "time": 1767229200,
                "open": 103.0,
                "high": 108.0,
                "low": 101.0,
                "close": 107.0,
            },
        ][:count]

    def symbol_info_tick(self, symbol):
        return SimpleNamespace(
            bid=100.0,
            ask=102.0,
        )


def test_initialize_mt5():
    fake = FakeMT5()

    adapter = MT5MarketDataAdapter(fake)

    adapter.initialize()

    assert fake.initialized is True


def test_get_candles_converts_mt5_rates():
    adapter = MT5MarketDataAdapter(
        FakeMT5()
    )

    candles = adapter.get_candles(
        symbol="XAUUSD",
        timeframe="H4",
        count=2,
    )

    assert len(candles) == 2

    assert candles[0].open == 100.0
    assert candles[0].high == 105.0
    assert candles[0].low == 98.0
    assert candles[0].close == 103.0


def test_get_current_price_uses_mid_price():
    adapter = MT5MarketDataAdapter(
        FakeMT5()
    )

    price = adapter.get_current_price(
        "XAUUSD"
    )

    assert price == 101.0


def test_unknown_timeframe_raises_error():
    adapter = MT5MarketDataAdapter(
        FakeMT5()
    )

    with pytest.raises(
        MT5MarketDataError
    ):
        adapter.get_candles(
            symbol="XAUUSD",
            timeframe="M99",
            count=100,
        )


def test_zero_count_returns_empty_list():
    adapter = MT5MarketDataAdapter(
        FakeMT5()
    )

    candles = adapter.get_candles(
        symbol="XAUUSD",
        timeframe="H4",
        count=0,
    )

    assert candles == []
    