from datetime import datetime, timedelta

from tdi.graphical.candle import Candle
from tdi.graphical.graphical_context_engine import (
    GraphicalContextEngine,
)
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection


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


def test_graphical_context_contains_direction():
    candles = [
        make_candle(0, 10, 5),
        make_candle(1, 11, 6),
        make_candle(2, 15, 7),
        make_candle(3, 12, 6),
        make_candle(4, 11, 5),
    ]

    result = GraphicalContextEngine().analyze(
        candles=candles,
        current_price=12,
        atr=2,
        ma20=11,
        market_direction=MarketDirection.BULLISH,
        direction_confidence=85,
    )

    assert result.direction == MarketDirection.BULLISH
    assert result.direction_confidence == 85


def test_graphical_context_contains_support_and_resistance():
    candles = [
        make_candle(0, 10, 5),
        make_candle(1, 12, 7),
        make_candle(2, 16, 8),
        make_candle(3, 13, 7),
        make_candle(4, 11, 6),
        make_candle(5, 14, 8),
        make_candle(6, 18, 9),
        make_candle(7, 15, 8),
        make_candle(8, 13, 7),
    ]

    result = GraphicalContextEngine().analyze(
        candles=candles,
        current_price=14,
        atr=2,
        ma20=13,
        market_direction=MarketDirection.BULLISH,
        direction_confidence=90,
    )

    assert result.support is not None
    assert result.resistance is not None


def test_graphical_context_returns_valid_location_type():
    candles = [
        make_candle(0, 10, 5),
        make_candle(1, 11, 6),
        make_candle(2, 15, 7),
        make_candle(3, 12, 6),
        make_candle(4, 11, 5),
    ]

    result = GraphicalContextEngine().analyze(
        candles=candles,
        current_price=12,
        atr=2,
        ma20=11.5,
        market_direction=MarketDirection.BULLISH,
        direction_confidence=80,
    )

    assert isinstance(result.location_type, LocationType)


def test_graphical_context_keeps_missing_levels():
    candles = []

    result = GraphicalContextEngine().analyze(
        candles=candles,
        current_price=100,
        atr=10,
        ma20=100,
        market_direction=MarketDirection.RANGE,
        direction_confidence=40,
    )

    assert result.support is None
    assert result.resistance is None


def test_graphical_context_accepts_breakout_level():
    candles = [
        make_candle(0, 90, 80),
        make_candle(1, 95, 85),
        make_candle(2, 110, 90),
        make_candle(3, 100, 88),
        make_candle(4, 96, 86),
    ]

    result = GraphicalContextEngine().analyze(
        candles=candles,
        current_price=102,
        atr=10,
        ma20=95,
        market_direction=MarketDirection.BULLISH,
        direction_confidence=90,
        breakout_level=100,
    )

    assert result.location_type == LocationType.BREAKOUT

def test_graphical_context_contains_bullish_ma_confirmation():
    candles = [
        make_candle(0, 100, 90),
        make_candle(1, 101, 91),
        make_candle(2, 105, 92),
        make_candle(3, 102, 91),
        make_candle(4, 101, 90),
    ]

    result = GraphicalContextEngine().analyze(
        candles=candles,
        current_price=120,
        atr=5,
        ma20=115,
        ma50=110,
        ma200=100,
        market_direction=MarketDirection.BULLISH,
        direction_confidence=80,
    )

    assert result.ma_bullish is True
    assert result.ma_bearish is False
    assert result.ma_confirmation_score == 100


def test_graphical_context_contains_bearish_ma_confirmation():
    candles = [
        make_candle(0, 100, 90),
        make_candle(1, 101, 91),
        make_candle(2, 105, 92),
        make_candle(3, 102, 91),
        make_candle(4, 101, 90),
    ]

    result = GraphicalContextEngine().analyze(
        candles=candles,
        current_price=80,
        atr=5,
        ma20=85,
        ma50=90,
        ma200=100,
        market_direction=MarketDirection.BEARISH,
        direction_confidence=80,
    )

    assert result.ma_bearish is True
    assert result.ma_bullish is False
    assert result.ma_confirmation_score == 100
    
