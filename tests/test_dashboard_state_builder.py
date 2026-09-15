from types import SimpleNamespace

from tdi.graphical.dashboard_state_builder import (
    DashboardStateBuilder,
)
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection


def value(name):
    return SimpleNamespace(value=name)


def test_dashboard_state_builder_builds_initial_state():
    decision = SimpleNamespace(
        decision=value("Wait"),
        preferred_side=None,
        bias_aligned=False,
        structure_aligned=False,
        timing_favorable=False,
        momentum_confirmed=False,
    )

    bias_readiness = SimpleNamespace(
        convergence=value("Toward"),
        readiness=value("Medium"),
        score=85,
    )

    scenario = SimpleNamespace(
        target_side="BUY",
        state=value("Building"),
        score=85,
    )

    wait_plan = SimpleNamespace(
        conditions=[
            value("H4/H1 Bias Alignment"),
        ]
    )

    state = DashboardStateBuilder.build(
        symbol="XAUUSD",
        decision=decision,
        bias_readiness=bias_readiness,
        scenario=scenario,
        wait_plan=wait_plan,
    )

    assert state.symbol == "XAUUSD"
    assert state.decision == "Wait"
    assert state.preferred_side is None
    assert state.target_side == "BUY"

    assert state.bias_convergence == "Toward"
    assert state.bias_readiness == "Medium"
    assert state.bias_score == 85

    assert state.bias_aligned is False
    assert state.structure_aligned is False
    assert state.timing_favorable is False
    assert state.momentum_confirmed is False

    assert state.scenario == "Building"
    assert state.scenario_score == 85
    assert state.waiting_for == (
        "H4/H1 Bias Alignment",
    )

    assert state.transition == "Initial"
    assert state.alert_level is None
    assert state.alert_active is False

def test_dashboard_state_builder_builds_alert_state():
    decision = SimpleNamespace(
        decision=value("Wait"),
        preferred_side="SELL",
        bias_aligned=True,
        structure_aligned=True,
        timing_favorable=False,
        momentum_confirmed=False,
    )

    bias_readiness = SimpleNamespace(
        convergence=value("Toward"),
        readiness=value("High"),
        score=90,
    )

    scenario = SimpleNamespace(
        target_side="SELL",
        state=value("Ready"),
        score=90,
    )

    wait_plan = SimpleNamespace(
        conditions=[
            value("Momentum Confirmation"),
        ]
    )

    transition = SimpleNamespace(
        transition=value("Improving"),
    )

    alert = SimpleNamespace(
        level=value("INFO"),
        active=True,
    )

    state = DashboardStateBuilder.build(
        symbol="XAUUSD",
        decision=decision,
        bias_readiness=bias_readiness,
        scenario=scenario,
        wait_plan=wait_plan,
        transition=transition,
        alert=alert,
    )

    assert state.transition == "Improving"
    assert state.alert_level == "INFO"
    assert state.alert_active is True


def test_dashboard_state_builder_marks_sell_watch_opportunity():
    decision = SimpleNamespace(
        decision=value("Wait"),
        preferred_side="SELL",
        bias_aligned=True,
        structure_aligned=False,
        timing_favorable=True,
        momentum_confirmed=False,
    )
    bias_readiness = SimpleNamespace(
        convergence=value("Aligned"),
        readiness=value("High"),
        score=100,
    )
    scenario = SimpleNamespace(
        target_side="SELL",
        state=value("Building"),
        score=60,
    )
    wait_plan = SimpleNamespace(conditions=[])
    h4_momentum = SimpleNamespace(
        momentum=value("Bearish"),
        confidence=100,
    )
    h1_momentum = SimpleNamespace(
        momentum=value("Neutral"),
        confidence=40,
    )

    state = DashboardStateBuilder.build(
        symbol="XAUUSD",
        decision=decision,
        bias_readiness=bias_readiness,
        scenario=scenario,
        wait_plan=wait_plan,
        h4_momentum=h4_momentum,
        h1_momentum=h1_momentum,
    )

    assert state.decision == "Wait"
    assert state.opportunity == "SELL WATCH"
    assert state.decisive_condition == (
        "H1 Bearish Momentum Confirmation"
    )
    assert state.h4_momentum == "Bearish"
    assert state.h4_momentum_confidence == 100
    assert state.h1_momentum == "Neutral"
    assert state.h1_momentum_confidence == 40


def test_dashboard_state_builder_marks_early_continuation():
    decision = SimpleNamespace(
        decision=value("Sell"),
        preferred_side="SELL",
        bias_aligned=True,
        structure_aligned=False,
        timing_favorable=True,
        momentum_confirmed=True,
    )
    bias_readiness = SimpleNamespace(
        convergence=value("Aligned"),
        readiness=value("High"),
        score=100,
    )
    scenario = SimpleNamespace(
        target_side="SELL",
        state=value("Ready"),
        score=100,
    )

    state = DashboardStateBuilder.build(
        symbol="GBPUSD",
        decision=decision,
        bias_readiness=bias_readiness,
        scenario=scenario,
        wait_plan=SimpleNamespace(conditions=[]),
    )

    assert state.scenario == "Ready"
    assert state.scenario_display == "Early continuation"
    assert state.decision_trigger == "Strong continuation confirmed"


def test_dashboard_state_builder_identifies_opposed_h1_structure():
    decision = SimpleNamespace(
        decision=value("Wait"),
        preferred_side="SELL",
        bias_aligned=True,
        structure_aligned=False,
        timing_favorable=True,
        momentum_confirmed=True,
    )
    result = SimpleNamespace(
        h4=SimpleNamespace(
            direction=MarketDirection.BEARISH,
            location_type=LocationType.PULLBACK,
        ),
        h1=SimpleNamespace(
            direction=MarketDirection.BULLISH,
            location_type=LocationType.RESISTANCE,
        ),
    )

    state = DashboardStateBuilder.build(
        symbol="GBPUSD",
        decision=decision,
        bias_readiness=SimpleNamespace(
            convergence=value("Aligned"),
            readiness=value("High"),
            score=100,
        ),
        scenario=SimpleNamespace(
            target_side="SELL",
            state=value("Building"),
            score=85,
        ),
        wait_plan=SimpleNamespace(conditions=[]),
        result=result,
    )

    assert state.decision_trigger == "H1 structure opposes SELL"
    assert state.scenario_display == "Building"


def test_dashboard_state_builder_accepts_result_test_double():
    decision = SimpleNamespace(
        decision=value("Wait"),
        preferred_side="SELL",
        bias_aligned=True,
        structure_aligned=False,
        timing_favorable=True,
        momentum_confirmed=True,
    )

    state = DashboardStateBuilder.build(
        symbol="GBPUSD",
        decision=decision,
        bias_readiness=SimpleNamespace(
            convergence=value("Aligned"),
            readiness=value("High"),
            score=100,
        ),
        scenario=SimpleNamespace(
            target_side="SELL",
            state=value("Building"),
            score=85,
        ),
        wait_plan=SimpleNamespace(conditions=[]),
        result=object(),
    )

    assert state.decision_trigger == "H4/H1 structure not confirmed"
