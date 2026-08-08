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

def test_wilder_atr_applies_smoothing():
    candles = make_candles(15)

    last = candles[-1]

    candles.append(
        Candle(
            index=15,
            timestamp=last.timestamp
            + timedelta(hours=1),
            open=114.0,
            high=124.0,
            low=112.0,
            close=120.0,
        )
    )

    result = IndicatorEngine().calculate(
        candles
    )

    expected = (
        (4.0 * 13) + 12.0
    ) / 14

    assert result.atr == expected


def test_wilder_atr_uses_all_new_true_ranges():
    candles = make_candles(15)

    candles.append(
        Candle(
            index=15,
            timestamp=(
                datetime(2026, 1, 1)
                + timedelta(hours=15)
            ),
            open=114.0,
            high=124.0,
            low=112.0,
            close=120.0,
        )
    )

    candles.append(
        Candle(
            index=16,
            timestamp=(
                datetime(2026, 1, 1)
                + timedelta(hours=16)
            ),
            open=120.0,
            high=125.0,
            low=119.0,
            close=123.0,
        )
    )

    result = IndicatorEngine().calculate(
        candles
    )

    first_atr = (
        (4.0 * 13) + 12.0
    ) / 14

    expected = (
        (first_atr * 13) + 6.0
    ) / 14

    assert result.atr == expected

def test_rsi_is_available_with_enough_history():
    result = IndicatorEngine().calculate(
        make_candles(30)
    )

    assert result.rsi is not None
    assert 0 <= result.rsi <= 100


def test_rsi_is_100_on_only_rising_closes():
    result = IndicatorEngine().calculate(
        make_candles(30)
    )

    assert result.rsi == 100.0


def test_macd_is_available_with_enough_history():
    result = IndicatorEngine().calculate(
        make_candles(50)
    )

    assert result.macd is not None
    assert result.macd_signal is not None
    assert result.macd_histogram is not None


def test_macd_histogram_matches_difference():
    result = IndicatorEngine().calculate(
        make_candles(50)
    )

    assert result.macd_histogram == (
        result.macd - result.macd_signal
    )

