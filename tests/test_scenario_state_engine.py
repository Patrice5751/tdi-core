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
    assert analysis.score == 90

def test_multiple_missing_conditions_reduce_maturity():
    wait_plan = WaitActionPlan(
        preferred_side="BUY",
        conditions=[
            WaitCondition.H4_STRUCTURE,
            WaitCondition.H1_STRUCTURE,
            WaitCondition.H1_SUPPORT,
            WaitCondition.MOMENTUM,
        ],
        ready=False,
        reason="Test",
    )

    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            preferred_side="BUY",
        ),
        wait_plan=wait_plan,
        bias_readiness=make_readiness(
            target_side="BUY",
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    assert analysis.state == ScenarioState.BUILDING
    assert analysis.score == 50


def test_structure_penalizes_maturity_more_than_momentum():
    structure_plan = WaitActionPlan(
        preferred_side="BUY",
        conditions=[
            WaitCondition.H4_STRUCTURE,
        ],
        ready=False,
        reason="Test",
    )

    momentum_plan = WaitActionPlan(
        preferred_side="BUY",
        conditions=[
            WaitCondition.MOMENTUM,
        ],
        ready=False,
        reason="Test",
    )

    engine = ScenarioStateEngine()

    structure = engine.analyze(
        decision=make_decision(),
        wait_plan=structure_plan,
        bias_readiness=make_readiness(
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    momentum = engine.analyze(
        decision=make_decision(),
        wait_plan=momentum_plan,
        bias_readiness=make_readiness(
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    assert structure.score == 85
    assert momentum.score == 90
    assert structure.score < momentum.score


def test_wait_decision_can_never_return_ready():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            decision=MultiTimeframeDecision.WAIT,
            preferred_side="BUY",
        ),
        wait_plan=make_wait_plan(
            preferred_side="BUY",
            ready=True,
        ),
        bias_readiness=make_readiness(
            target_side="BUY",
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    assert analysis.state != ScenarioState.READY


def test_buy_decision_always_returns_ready():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            decision=MultiTimeframeDecision.BUY,
            preferred_side="BUY",
        ),
        wait_plan=make_wait_plan(
            preferred_side="BUY",
            ready=True,
        ),
        bias_readiness=make_readiness(
            target_side="BUY",
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    assert analysis.state == ScenarioState.READY
    assert analysis.target_side == "BUY"


def test_sell_decision_always_returns_ready():
    analysis = ScenarioStateEngine().analyze(
        decision=make_decision(
            decision=MultiTimeframeDecision.SELL,
            preferred_side="SELL",
        ),
        wait_plan=make_wait_plan(
            preferred_side="SELL",
            ready=True,
        ),
        bias_readiness=make_readiness(
            target_side="SELL",
            readiness=BiasReadiness.HIGH,
            convergence=BiasConvergence.ALIGNED,
            score=100,
        ),
    )

    assert analysis.state == ScenarioState.READY
    assert analysis.target_side == "SELL"