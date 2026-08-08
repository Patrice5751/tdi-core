from datetime import datetime, timedelta

from tdi.graphical.candle import Candle
from tdi.indicators.indicator_engine import IndicatorEngine


def make_candles(
    count: int,
) -> list[Candle]:
    candles = []

    for index in range(count):
        close = 100.0 + index

        candles.append(
            Candle(
                index=index,
                timestamp=(
                    datetime(2026, 1, 1)
                    + timedelta(hours=index)
                ),
                open=close - 1,
                high=close + 2,
                low=close - 2,
                close=close,
            )
        )

    return candles


def test_less_than_twenty_candles_returns_no_ma():
    result = IndicatorEngine().calculate(
        make_candles(10)
    )

    assert result.ma20 is None
    assert result.ma50 is None
    assert result.ma200 is None


def test_ma20_uses_last_twenty_closes():
    result = IndicatorEngine().calculate(
        make_candles(20)
    )

    assert result.ma20 == 109.5


def test_ma50_uses_last_fifty_closes():
    result = IndicatorEngine().calculate(
        make_candles(50)
    )

    assert result.ma50 == 124.5


def test_ma200_uses_last_two_hundred_closes():
    result = IndicatorEngine().calculate(
        make_candles(200)
    )

    assert result.ma200 == 199.5


def test_atr_requires_fifteen_candles():
    result = IndicatorEngine().calculate(
        make_candles(14)
    )

    assert result.atr is None


def test_atr_is_calculated_from_true_range():
    result = IndicatorEngine().calculate(
        make_candles(15)
    )

    assert result.atr == 4.0
    