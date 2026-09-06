from tdi.analysis.trend_analysis import Trend
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.intermarket_direction_adapter import (
    IntermarketDirectionAdapter,
)


def test_bullish_market_direction_maps_to_bullish_trend():
    result = IntermarketDirectionAdapter.to_trend(
        MarketDirection.BULLISH
    )

    assert result == Trend.BULLISH


def test_bearish_market_direction_maps_to_bearish_trend():
    result = IntermarketDirectionAdapter.to_trend(
        MarketDirection.BEARISH
    )

    assert result == Trend.BEARISH


def test_range_market_direction_maps_to_neutral_trend():
    result = IntermarketDirectionAdapter.to_trend(
        MarketDirection.RANGE
    )

    assert result == Trend.NEUTRAL


def test_transition_market_direction_maps_to_neutral_trend():
    result = IntermarketDirectionAdapter.to_trend(
        MarketDirection.TRANSITION
    )

    assert result == Trend.NEUTRAL