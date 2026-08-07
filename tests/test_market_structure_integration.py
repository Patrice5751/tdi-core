from datetime import datetime, timedelta

from tdi.graphical.candle import Candle
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.market_direction_engine import (
    MarketDirectionEngine,
)
from tdi.graphical.pivot_detector import PivotDetector
from tdi.graphical.swing_classifier import SwingClassifier


def make_candle(
    index: int,
    high: float,
    low: float,
) -> Candle:
    return Candle(
        index=index,
        timestamp=datetime(2026, 1, 1)
        + timedelta(hours=index),
        open=low,
        high=high,
        low=low,
        close=high,
    )


def test_complete_bullish_market_structure():
    candles = [
        make_candle(0, 10, 5),
        make_candle(1, 12, 7),
        make_candle(2, 20, 10),
        make_candle(3, 14, 8),
        make_candle(4, 12, 6),
        make_candle(5, 15, 9),
        make_candle(6, 25, 12),
        make_candle(7, 18, 10),
        make_candle(8, 16, 8),
        make_candle(9, 20, 12),
        make_candle(10, 30, 15),
        make_candle(11, 22, 13),
        make_candle(12, 18, 10),
        make_candle(13, 24, 15),
        make_candle(14, 35, 18),
        make_candle(15, 26, 16),
        make_candle(16, 22, 12),
        make_candle(17, 28, 18),
        make_candle(18, 40, 20),
        make_candle(19, 30, 19),
        make_candle(20, 25, 15),
    ]

    pivots = PivotDetector().detect(candles)

    swings = SwingClassifier().classify(pivots)

    analysis = MarketDirectionEngine().detect(swings)

    assert analysis.direction == MarketDirection.BULLISH


def test_complete_bearish_market_structure():
    candles = [
        make_candle(0, 40, 30),
        make_candle(1, 38, 28),
        make_candle(2, 45, 25),
        make_candle(3, 36, 24),
        make_candle(4, 34, 20),
        make_candle(5, 37, 23),
        make_candle(6, 40, 18),
        make_candle(7, 32, 17),
        make_candle(8, 30, 14),
        make_candle(9, 33, 17),
        make_candle(10, 35, 12),
        make_candle(11, 28, 11),
        make_candle(12, 26, 8),
        make_candle(13, 29, 11),
        make_candle(14, 30, 6),
        make_candle(15, 24, 5),
        make_candle(16, 22, 3),
        make_candle(17, 25, 6),
        make_candle(18, 27, 1),
        make_candle(19, 20, 0),
        make_candle(20, 18, -2),
    ]

    pivots = PivotDetector().detect(candles)

    swings = SwingClassifier().classify(pivots)

    analysis = MarketDirectionEngine().detect(swings)

    assert analysis.direction == MarketDirection.BEARISH
    