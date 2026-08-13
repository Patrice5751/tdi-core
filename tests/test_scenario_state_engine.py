from tdi.graphical.bias_readiness import (
    BiasConvergence,
    BiasReadiness,
    BiasReadinessAnalysis,
)
from tdi.graphical.multi_timeframe_decision import (
    MultiTimeframeDecision,
)
from tdi.graphical.multi_timeframe_decision_analysis import (
    MultiTimeframeDecisionAnalysis,
)
from tdi.graphical.scenario_state import ScenarioState
from tdi.graphical.scenario_state_engine import (
    ScenarioStateEngine,
)
from tdi.graphical.wait_action_plan import WaitActionPlan
from tdi.graphical.wait_condition import WaitCondition


def make_decision(
    decision=MultiTimeframeDecision.WAIT,
    preferred_side="BUY",
):
    return MultiTimeframeDecisionAnalysis(
        decision=decision,
        preferred_side=preferred_side,
        bias_aligned=False,
        structure_aligned=False,
        timing_favorable=False,
        confidence=50,
        reason="Test",
        momentum_confirmed=False,
    )


def make_readiness(
    target_side="BUY",
    readiness=BiasReadiness.LOW,
    convergence=BiasConvergence.UNDEFINED,
    score=30,
):
    return BiasReadinessAnalysis(
        target_side=target_side,
        readiness=readiness,
        convergence=convergence,
        score=score,
        reason="Test",
    )


def make_wait_plan(
    preferred_side="BUY",
    ready=False,
):
    return WaitActionPlan(
        preferred_side=preferred_side,
        conditions=(
            []
            if ready
            else [WaitCondition.MOMENTUM]
        ),
        ready=ready,
        reason="Test",
    )


def test_buy_decision_returns_ready():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            decision=MultiTimeframeDecision.BUY,
            preferred_side="BUY",
        ),
        wait_plan=make_wait_plan(
            ready=True,
        ),
        bias_readiness=make_readiness(
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    assert analysis.state == ScenarioState.READY
    assert analysis.target_side == "BUY"
    assert analysis.score == 100


def test_toward_bias_returns_building():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(),
        wait_plan=make_wait_plan(),
        bias_readiness=make_readiness(
            readiness=BiasReadiness.MEDIUM,
            convergence=BiasConvergence.TOWARD,
            score=75,
        ),
    )

    assert analysis.state == ScenarioState.BUILDING
    assert analysis.target_side == "BUY"
    assert analysis.score == 75


def test_away_bias_returns_degrading():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            preferred_side=None,
        ),
        wait_plan=make_wait_plan(
            preferred_side=None,
        ),
        bias_readiness=make_readiness(
            target_side="BUY",
            readiness=BiasReadiness.LOW,
            convergence=BiasConvergence.AWAY,
            score=7,
        ),
    )

    assert analysis.state == ScenarioState.DEGRADING
    assert analysis.target_side == "BUY"
    assert analysis.score == 7


def test_no_directional_scenario_returns_invalid():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            preferred_side=None,
        ),
        wait_plan=make_wait_plan(
            preferred_side=None,
        ),
        bias_readiness=make_readiness(
            target_side=None,
            readiness=BiasReadiness.LOW,
            convergence=BiasConvergence.UNDEFINED,
            score=0,
        ),
    )

    assert analysis.state == ScenarioState.INVALID
    assert analysis.target_side is None
    assert analysis.score == 0


def test_aligned_bias_with_missing_conditions_is_building():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            preferred_side="BUY",
        ),
        wait_plan=make_wait_plan(
            preferred_side="BUY",
            ready=False,
        ),
        bias_readiness=make_readiness(
            target_side="BUY",
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    assert analysis.state == ScenarioState.BUILDING
    assert analysis.target_side == "BUY"
    assert analysis.score == 80
    