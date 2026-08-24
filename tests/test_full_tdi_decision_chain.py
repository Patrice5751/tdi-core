from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.bias_readiness import (
    BiasConvergence,
    BiasReadiness,
    BiasReadinessAnalysis,
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
from tdi.graphical.scenario_state import ScenarioState
from tdi.graphical.scenario_state_engine import (
    ScenarioStateEngine,
)
from tdi.graphical.scenario_transition import (
    ScenarioTransition,
)
from tdi.graphical.scenario_transition_engine import (
    ScenarioTransitionEngine,
)
from tdi.graphical.transition_alert import AlertLevel
from tdi.graphical.transition_alert_engine import (
    TransitionAlertEngine,
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


def make_readiness(side):
    return BiasReadinessAnalysis(
        target_side=side,
        readiness=BiasReadiness.HIGH,
        convergence=BiasConvergence.ALIGNED,
        score=100,
        reason="Test",
    )


def test_full_buy_chain_triggers_high_alert():
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

    h4_momentum = make_momentum(
        Momentum.BULLISH
    )

    h1_momentum = make_momentum(
        Momentum.BULLISH
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    wait_plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    scenario = ScenarioStateEngine().analyze(
        decision=decision,
        wait_plan=wait_plan,
        bias_readiness=make_readiness("BUY"),
    )

    transition = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=scenario.state,
        previous_target_side="BUY",
        current_target_side=scenario.target_side,
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side=scenario.target_side,
    )

    assert (
        decision.decision
        == MultiTimeframeDecision.BUY
    )

    assert wait_plan.ready is True

    assert (
        scenario.state
        == ScenarioState.READY
    )

    assert (
        transition.transition
        == ScenarioTransition.TRIGGERED
    )

    assert alert.level == AlertLevel.HIGH
    assert alert.active is True
    assert "BUY" in alert.message


def test_incomplete_buy_chain_never_triggers_high_alert():
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

    h4_momentum = make_momentum(
        Momentum.BULLISH
    )

    h1_momentum = make_momentum(
        Momentum.BULLISH
    )

    decision = MultiTimeframeDecisionEngine().decide(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    wait_plan = WaitActionPlanEngine().analyze(
        result=result,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    scenario = ScenarioStateEngine().analyze(
        decision=decision,
        wait_plan=wait_plan,
        bias_readiness=make_readiness("BUY"),
    )

    transition = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=scenario.state,
        previous_target_side="BUY",
        current_target_side=scenario.target_side,
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side=scenario.target_side,
    )

    assert (
        decision.decision
        == MultiTimeframeDecision.WAIT
    )

    assert wait_plan.ready is False

    assert (
        scenario.state
        != ScenarioState.READY
    )

    assert (
        transition.transition
        != ScenarioTransition.TRIGGERED
    )

    assert alert.level != AlertLevel.HIGH