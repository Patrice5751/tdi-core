from types import SimpleNamespace

import pytest

from tdi.adapters.mt5_analysis_pipeline import (
    MT5AnalysisPipeline,
)
from tdi.graphical.candle import Candle
from tdi.graphical.graphical_context import (
    GraphicalContext,
)


class FakeAdapter:
    def __init__(
        self,
        candles,
        price=100.0,
    ):
        self._candles = candles
        self._price = price

    def get_candles(
        self,
        symbol,
        timeframe,
        count,
    ):
        return self._candles[:count]

    def get_current_price(
        self,
        symbol,
    ):
        return self._price


def make_candles(
    count: int,
) -> list[Candle]:
    candles = []

    for index in range(count):
        base = 100.0 + index

        candles.append(
            Candle(
                index=index,
                timestamp=SimpleNamespace(),
                open=base,
                high=base + 2,
                low=base - 2,
                close=base + 1,
            )
        )

    return candles


def test_pipeline_returns_graphical_context():
    adapter = FakeAdapter(
        candles=make_candles(250),
        price=350.0,
    )

    result = MT5AnalysisPipeline(
        adapter=adapter
    ).analyze(
        symbol="XAUUSD",
        timeframe="H4",
    )

    assert isinstance(
        result,
        GraphicalContext,
    )


def test_pipeline_raises_without_candles():
    adapter = FakeAdapter(
        candles=[],
    )

    with pytest.raises(ValueError):
        MT5AnalysisPipeline(
            adapter=adapter
        ).analyze(
            symbol="XAUUSD",
        )


def test_pipeline_requires_enough_history_for_atr():
    adapter = FakeAdapter(
        candles=make_candles(10),
    )

    with pytest.raises(ValueError):
        MT5AnalysisPipeline(
            adapter=adapter
        ).analyze(
            symbol="XAUUSD",
        )


def test_pipeline_requires_enough_history_for_ma20():
    adapter = FakeAdapter(
        candles=make_candles(15),
    )

    with pytest.raises(ValueError):
        MT5AnalysisPipeline(
            adapter=adapter
        ).analyze(
            symbol="XAUUSD",
        )
        