from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_bias import MarketBias
from tdi.graphical.market_bias_engine import MarketBiasEngine
from tdi.graphical.market_direction import MarketDirection


def make_context(
    direction,
    ma_bullish=False,
    ma_bearish=False,
    ma_score=0,
):
    return GraphicalContext(
        direction=direction,
        direction_confidence=80,
        location_type=LocationType.MIDDLE,
        support=None,
        resistance=None,
        support_touches=0,
        resistance_touches=0,
        ma_confirmation_score=ma_score,
        ma_bullish=ma_bullish,
        ma_bearish=ma_bearish,
    )


def test_bullish_structure_and_ma_is_strong_bullish():
    result = MarketBiasEngine().analyze(
        make_context(
            MarketDirection.BULLISH,
            ma_bullish=True,
            ma_score=100,
        )
    )

    assert result.bias == MarketBias.STRONG_BULLISH
    assert result.preferred_side == "BUY"


def test_transition_with_bullish_ma_is_bullish():
    result = MarketBiasEngine().analyze(
        make_context(
            MarketDirection.TRANSITION,
            ma_bullish=True,
            ma_score=100,
        )
    )

    assert result.bias == MarketBias.BULLISH
    assert result.preferred_side == "BUY"


def test_bearish_structure_and_ma_is_strong_bearish():
    result = MarketBiasEngine().analyze(
        make_context(
            MarketDirection.BEARISH,
            ma_bearish=True,
            ma_score=100,
        )
    )

    assert result.bias == MarketBias.STRONG_BEARISH
    assert result.preferred_side == "SELL"


def test_transition_with_bearish_ma_is_bearish():
    result = MarketBiasEngine().analyze(
        make_context(
            MarketDirection.TRANSITION,
            ma_bearish=True,
            ma_score=100,
        )
    )

    assert result.bias == MarketBias.BEARISH
    assert result.preferred_side == "SELL"


def test_no_ma_confirmation_is_neutral():
    result = MarketBiasEngine().analyze(
        make_context(
            MarketDirection.TRANSITION,
        )
    )

    assert result.bias == MarketBias.NEUTRAL
    assert result.preferred_side is None
    