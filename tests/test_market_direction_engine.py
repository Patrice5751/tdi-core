from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.market_direction_engine import (
    MarketDirectionEngine,
)
from tdi.graphical.swing_point import SwingPoint
from tdi.graphical.swing_type import SwingType


def test_detect_bullish_market():
    swings = [
        SwingPoint(1, 100, SwingType.HH),
        SwingPoint(2, 95, SwingType.HL),
        SwingPoint(3, 105, SwingType.HH),
        SwingPoint(4, 99, SwingType.HL),
        SwingPoint(5, 110, SwingType.HH),
        SwingPoint(6, 103, SwingType.HL),
    ]

    result = MarketDirectionEngine().detect(swings)

    assert result.direction == MarketDirection.BULLISH


def test_detect_bearish_market():
    swings = [
        SwingPoint(1, 100, SwingType.LH),
        SwingPoint(2, 95, SwingType.LL),
        SwingPoint(3, 97, SwingType.LH),
        SwingPoint(4, 90, SwingType.LL),
        SwingPoint(5, 92, SwingType.LH),
        SwingPoint(6, 85, SwingType.LL),
    ]

    result = MarketDirectionEngine().detect(swings)

    assert result.direction == MarketDirection.BEARISH


def test_detect_transition():
    swings = [
        SwingPoint(1, 100, SwingType.HH),
        SwingPoint(2, 95, SwingType.HL),
        SwingPoint(3, 96, SwingType.LH),
        SwingPoint(4, 90, SwingType.LL),
    ]

    result = MarketDirectionEngine().detect(swings)

    assert result.direction == MarketDirection.TRANSITION


def test_detect_range():
    swings = [
        SwingPoint(1, 100, SwingType.HL),
        SwingPoint(2, 98, SwingType.LH),
        SwingPoint(3, 101, SwingType.HL),
        SwingPoint(4, 99, SwingType.LH),
    ]

    result = MarketDirectionEngine().detect(swings)

    assert result.direction == MarketDirection.RANGE


def test_empty_swings_returns_range_with_zero_confidence():
    result = MarketDirectionEngine().detect([])

    assert result.direction == MarketDirection.RANGE
    assert result.structure_confidence == 0
    assert result.confidence == 0


def test_insufficient_swings_returns_transition():
    swings = [
        SwingPoint(1, 100, SwingType.HH),
        SwingPoint(2, 95, SwingType.HL),
    ]

    result = MarketDirectionEngine().detect(swings)

    assert result.direction == MarketDirection.TRANSITION
    assert result.structure_confidence < 100

def test_bullish_structure_with_one_wrong_swing():
    swings = [
        SwingPoint(1, 100, SwingType.HH),
        SwingPoint(2, 95, SwingType.HL),
        SwingPoint(3, 105, SwingType.HH),
        SwingPoint(4, 101, SwingType.LH),   # swing contradictoire
        SwingPoint(5, 110, SwingType.HH),
        SwingPoint(6, 104, SwingType.HL),
    ]

    result = MarketDirectionEngine().detect(swings)

    assert result.direction == MarketDirection.BULLISH
    assert result.structure_confidence < 100