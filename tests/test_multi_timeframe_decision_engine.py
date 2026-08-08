from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.multi_timeframe_decision import (
    MultiTimeframeDecision,
)
from tdi.graphical.multi_timeframe_decision_engine import (
    MultiTimeframeDecisionEngine,
)


def make_context(
    direction: MarketDirection,
    location: LocationType,
    ma_bullish: bool = False,
    ma_bearish: bool = False,
):
    return GraphicalContext(
        direction=direction,
        direction_confidence=80,
        location_type=location,
        support=100.0,
        resistance=120.0,
        support_touches=2,
        resistance_touches=2,
        ma_confirmation_score=100,
        ma_bullish=ma_bullish,
        ma_bearish=ma_bearish,
    )


def test_aligned_buy_bias_with_extension_returns_wait():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            MarketDirection.TRANSITION,
            LocationType.EXTENSION,
            ma_bullish=True,
        ),
        h1=make_context(
            MarketDirection.TRANSITION,
            LocationType.MIDDLE,
            ma_bullish=True,
        ),
        aligned=False,
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result
    )

    assert decision.decision == MultiTimeframeDecision.WAIT
    assert decision.preferred_side == "BUY"
    assert decision.bias_aligned is True


def test_aligned_buy_bias_with_good_timing_returns_buy():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            MarketDirection.BULLISH,
            LocationType.PULLBACK,
            ma_bullish=True,
        ),
        h1=make_context(
            MarketDirection.BULLISH,
            LocationType.SUPPORT,
            ma_bullish=True,
        ),
        aligned=True,
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result
    )

    assert decision.decision == MultiTimeframeDecision.BUY
    assert decision.preferred_side == "BUY"


def test_aligned_sell_bias_with_good_timing_returns_sell():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            MarketDirection.BEARISH,
            LocationType.PULLBACK,
            ma_bearish=True,
        ),
        h1=make_context(
            MarketDirection.BEARISH,
            LocationType.RESISTANCE,
            ma_bearish=True,
        ),
        aligned=True,
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result
    )

    assert decision.decision == MultiTimeframeDecision.SELL
    assert decision.preferred_side == "SELL"


def test_conflicting_biases_return_wait():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            MarketDirection.TRANSITION,
            LocationType.PULLBACK,
            ma_bullish=True,
        ),
        h1=make_context(
            MarketDirection.TRANSITION,
            LocationType.PULLBACK,
            ma_bearish=True,
        ),
        aligned=False,
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result
    )

    assert decision.decision == MultiTimeframeDecision.WAIT
    assert decision.preferred_side is None


def test_buy_bias_on_h1_resistance_returns_wait():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            MarketDirection.BULLISH,
            LocationType.PULLBACK,
            ma_bullish=True,
        ),
        h1=make_context(
            MarketDirection.BULLISH,
            LocationType.RESISTANCE,
            ma_bullish=True,
        ),
        aligned=True,
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result
    )

    assert decision.decision == MultiTimeframeDecision.WAIT