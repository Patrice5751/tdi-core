from tdi.adapters.mt5_multi_timeframe_pipeline import (
    MT5MultiTimeframePipeline,
)
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection


class FakePipeline:
    def __init__(
        self,
        h4_direction,
        h1_direction,
    ):
        self.h4_direction = h4_direction
        self.h1_direction = h1_direction
        self.calls = []

    def analyze(
        self,
        symbol,
        timeframe,
        count,
    ):
        self.calls.append(timeframe)

        direction = (
            self.h4_direction
            if timeframe == "H4"
            else self.h1_direction
        )

        return GraphicalContext(
            direction=direction,
            direction_confidence=90,
            location_type=LocationType.MIDDLE,
            support=100.0,
            resistance=120.0,
            support_touches=2,
            resistance_touches=2,
        )


def test_pipeline_analyzes_h4_and_h1():
    fake = FakePipeline(
        MarketDirection.BULLISH,
        MarketDirection.BULLISH,
    )

    MT5MultiTimeframePipeline(
        pipeline=fake
    ).analyze(
        symbol="XAUUSD"
    )

    assert fake.calls == ["H4", "H1"]


def test_same_directions_are_aligned():
    fake = FakePipeline(
        MarketDirection.BULLISH,
        MarketDirection.BULLISH,
    )

    result = MT5MultiTimeframePipeline(
        pipeline=fake
    ).analyze(
        symbol="XAUUSD"
    )

    assert result.aligned is True


def test_different_directions_are_not_aligned():
    fake = FakePipeline(
        MarketDirection.BULLISH,
        MarketDirection.BEARISH,
    )

    result = MT5MultiTimeframePipeline(
        pipeline=fake
    ).analyze(
        symbol="XAUUSD"
    )

    assert result.aligned is False
    