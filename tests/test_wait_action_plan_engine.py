from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.wait_action_plan_engine import (
    WaitActionPlanEngine,
)
from tdi.graphical.wait_condition import WaitCondition


def make_context(
    direction,
    location,
    ma_bullish=False,
    ma_bearish=False,
):
    return GraphicalContext(
        direction=direction,
        direction_confidence=80,
        location_type=location,
        support=None,
        resistance=None,
        support_touches=0,
        resistance_touches=0,
        ma_confirmation_score=100,
        ma_bullish=ma_bullish,
        ma_bearish=ma_bearish,
    )


def make_momentum(
    momentum,
):
    return MomentumAnalysis(
        momentum=momentum,
        confidence=100,
        reason=[],
    )


def test_real_like_buy_wait_plan():
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

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=make_momentum(
            Momentum.BULLISH
        ),
        h1_momentum=make_momentum(
            Momentum.BULLISH
        ),
    )

    assert plan.preferred_side == "BUY"
    assert plan.ready is False

    assert WaitCondition.H4_STRUCTURE in plan.conditions
    assert WaitCondition.H1_STRUCTURE in plan.conditions
    assert WaitCondition.H4_PULLBACK in plan.conditions
    assert WaitCondition.H1_SUPPORT in plan.conditions

    assert WaitCondition.MOMENTUM not in plan.conditions


def test_missing_momentum_adds_momentum_condition():
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

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=make_momentum(
            Momentum.BULLISH
        ),
        h1_momentum=make_momentum(
            Momentum.NEUTRAL
        ),
    )

    assert WaitCondition.MOMENTUM in plan.conditions
    assert plan.ready is False


def test_all_conditions_met_returns_ready():
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

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=make_momentum(
            Momentum.BULLISH
        ),
        h1_momentum=make_momentum(
            Momentum.BULLISH
        ),
    )

    assert plan.ready is True
    assert plan.conditions == []


def test_conflicting_bias_waits_for_bias_alignment():
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

    plan = WaitActionPlanEngine().analyze(
        result=result,
    )

    assert plan.preferred_side is None
    assert plan.ready is False
    assert plan.conditions == [
        WaitCondition.BIAS_ALIGNMENT
    ]

    assert plan.preferred_side is None
    assert plan.ready is False

def test_missing_momentum_adds_momentum_wait_condition():
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

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=None,
        h1_momentum=None,
    )

    assert plan.preferred_side == "BUY"
    assert plan.ready is False
    assert WaitCondition.MOMENTUM in plan.conditions