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
from tdi.graphical.multi_timeframe_decision import (
    MultiTimeframeDecision,
)
from tdi.graphical.multi_timeframe_decision_engine import (
    MultiTimeframeDecisionEngine,
)
from tdi.graphical.wait_action_plan_engine import (
    WaitActionPlanEngine,
)


def make_context(
    direction,
    location,
    ma_bullish=False,
    ma_bearish=False,
):
    return GraphicalContext(
        direction=direction,
        direction_confidence=100,
        location_type=location,
        support=100.0,
        resistance=120.0,
        support_touches=2,
        resistance_touches=2,
        ma_confirmation_score=100,
        ma_bullish=ma_bullish,
        ma_bearish=ma_bearish,
    )


def make_momentum(momentum):
    return MomentumAnalysis(
        momentum=momentum,
        confidence=100,
        reason=[],
    )


def test_buy_decision_matches_ready_wait_plan():
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

    h4_momentum = make_momentum(Momentum.BULLISH)
    h1_momentum = make_momentum(Momentum.BULLISH)

    decision = MultiTimeframeDecisionEngine().decide(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    assert decision.decision == MultiTimeframeDecision.BUY
    assert plan.ready is True
    assert plan.conditions == []


def test_sell_decision_matches_ready_wait_plan():
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

    h4_momentum = make_momentum(Momentum.BEARISH)
    h1_momentum = make_momentum(Momentum.BEARISH)

    decision = MultiTimeframeDecisionEngine().decide(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    assert decision.decision == MultiTimeframeDecision.SELL
    assert plan.ready is True
    assert plan.conditions == []


def test_wait_for_structure_matches_non_ready_plan():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            MarketDirection.TRANSITION,
            LocationType.PULLBACK,
            ma_bullish=True,
        ),
        h1=make_context(
            MarketDirection.TRANSITION,
            LocationType.SUPPORT,
            ma_bullish=True,
        ),
        aligned=False,
    )

    h4_momentum = make_momentum(Momentum.BULLISH)
    h1_momentum = make_momentum(Momentum.BULLISH)

    decision = MultiTimeframeDecisionEngine().decide(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    assert decision.decision == MultiTimeframeDecision.WAIT
    assert plan.ready is False
    assert len(plan.conditions) > 0


def test_wait_for_missing_momentum_matches_non_ready_plan():
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
        result=result,
        h4_momentum=None,
        h1_momentum=None,
    )

    plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=None,
        h1_momentum=None,
    )

    assert decision.decision == MultiTimeframeDecision.WAIT
    assert plan.ready is False
    assert len(plan.conditions) > 0