from datetime import datetime, timedelta

from tdi.graphical.candle import Candle
from tdi.graphical.pivot_detector import PivotDetector
from tdi.graphical.pivot_type import PivotType


def make_candle(
    index: int,
    high: float,
    low: float,
) -> Candle:
    return Candle(
        index=index,
        timestamp=datetime(2026, 1, 1) + timedelta(hours=index),
        open=low,
        high=high,
        low=low,
        close=high,
    )


def test_detect_clear_pivot_high():
    candles = [
        make_candle(0, 10, 5),
        make_candle(1, 11, 6),
        make_candle(2, 15, 7),
        make_candle(3, 12, 6),
        make_candle(4, 11, 5),
    ]

    pivots = PivotDetector().detect(candles)

    assert len(pivots) == 1
    assert pivots[0].index == 2
    assert pivots[0].price == 15
    assert pivots[0].pivot_type == PivotType.HIGH


def test_detect_clear_pivot_low():
    candles = [
        make_candle(0, 15, 10),
        make_candle(1, 14, 9),
        make_candle(2, 13, 5),
        make_candle(3, 14, 8),
        make_candle(4, 15, 9),
    ]

    pivots = PivotDetector().detect(candles)

    assert len(pivots) == 1
    assert pivots[0].index == 2
    assert pivots[0].price == 5
    assert pivots[0].pivot_type == PivotType.LOW


def test_less_than_five_candles_returns_empty():
    candles = [
        make_candle(0, 10, 5),
        make_candle(1, 11, 6),
        make_candle(2, 12, 7),
        make_candle(3, 11, 6),
    ]

    assert PivotDetector().detect(candles) == []


def test_first_two_candles_cannot_be_pivots():
    candles = [
        make_candle(0, 20, 5),
        make_candle(1, 18, 6),
        make_candle(2, 15, 7),
        make_candle(3, 14, 8),
        make_candle(4, 13, 9),
    ]

    pivots = PivotDetector().detect(candles)

    assert all(pivot.index >= 2 for pivot in pivots)


def test_last_two_candles_cannot_be_pivots():
    candles = [
        make_candle(0, 10, 5),
        make_candle(1, 11, 6),
        make_candle(2, 12, 7),
        make_candle(3, 18, 8),
        make_candle(4, 20, 9),
    ]

    pivots = PivotDetector().detect(candles)

    assert all(pivot.index <= 2 for pivot in pivots)


def test_pivots_are_returned_in_chronological_order():
    candles = [
        make_candle(0, 10, 6),
        make_candle(1, 11, 7),
        make_candle(2, 15, 8),
        make_candle(3, 12, 7),
        make_candle(4, 11, 5),
        make_candle(5, 12, 7),
        make_candle(6, 16, 8),
        make_candle(7, 13, 7),
        make_candle(8, 12, 6),
    ]

    pivots = PivotDetector().detect(candles)

    indexes = [pivot.index for pivot in pivots]

    assert indexes == sorted(indexes)

def test_pivot_below_half_atr_is_rejected():
    candles = [
        make_candle(0, 10.0, 5),
        make_candle(1, 10.5, 6),
        make_candle(2, 10.9, 7),
        make_candle(3, 10.5, 6),
        make_candle(4, 10.0, 5),
    ]

    pivots = PivotDetector().detect(
        candles,
        atr=1.0,
    )

    assert pivots == []


def test_pivot_at_exactly_half_atr_is_accepted():
    candles = [
        make_candle(0, 10.0, 5),
        make_candle(1, 10.5, 6),
        make_candle(2, 11.0, 7),
        make_candle(3, 10.5, 6),
        make_candle(4, 10.0, 5),
    ]

    pivots = PivotDetector().detect(
        candles,
        atr=1.0,
    )

    assert len(pivots) == 1
    assert pivots[0].pivot_type == PivotType.HIGH
    assert pivots[0].price == 11.0


def test_pivot_above_half_atr_is_accepted():
    candles = [
        make_candle(0, 10.0, 5),
        make_candle(1, 10.5, 6),
        make_candle(2, 11.2, 7),
        make_candle(3, 10.5, 6),
        make_candle(4, 10.0, 5),
    ]

    pivots = PivotDetector().detect(
        candles,
        atr=1.0,
    )

    assert len(pivots) == 1
    assert pivots[0].pivot_type == PivotType.HIGH