from tdi.graphical.scenario_state import ScenarioState
from tdi.graphical.scenario_transition import (
    ScenarioTransition,
    ScenarioTransitionAnalysis,
)
from tdi.graphical.transition_alert import AlertLevel
from tdi.graphical.transition_alert_engine import (
    TransitionAlertEngine,
)


def make_transition(
    transition: ScenarioTransition,
    previous_state=ScenarioState.DEGRADING,
    current_state=ScenarioState.BUILDING,
):
    return ScenarioTransitionAnalysis(
        previous_state=previous_state,
        current_state=current_state,
        transition=transition,
        reason="Test",
    )


def test_unchanged_has_no_alert():
    alert = TransitionAlertEngine().analyze(
        transition=make_transition(
            ScenarioTransition.UNCHANGED
        ),
        target_side="BUY",
    )

    assert alert.level == AlertLevel.NONE
    assert alert.active is False


def test_improving_generates_info_alert():
    alert = TransitionAlertEngine().analyze(
        transition=make_transition(
            ScenarioTransition.IMPROVING
        ),
        target_side="BUY",
    )

    assert alert.level == AlertLevel.INFO
    assert alert.active is True
    assert "BUY" in alert.message


def test_deteriorating_generates_warning():
    alert = TransitionAlertEngine().analyze(
        transition=make_transition(
            ScenarioTransition.DETERIORATING
        ),
        target_side="BUY",
    )

    assert alert.level == AlertLevel.WARNING
    assert alert.active is True


def test_invalidated_generates_warning():
    alert = TransitionAlertEngine().analyze(
        transition=make_transition(
            ScenarioTransition.INVALIDATED,
            current_state=ScenarioState.INVALID,
        ),
        target_side=None,
    )

    assert alert.level == AlertLevel.WARNING
    assert alert.active is True


def test_triggered_generates_high_alert():
    alert = TransitionAlertEngine().analyze(
        transition=make_transition(
            ScenarioTransition.TRIGGERED,
            previous_state=ScenarioState.BUILDING,
            current_state=ScenarioState.READY,
        ),
        target_side="BUY",
    )

    assert alert.level == AlertLevel.HIGH
    assert alert.active is True
    assert "Ready" in alert.message
    assert "BUY" in alert.message


def test_missing_target_side_is_supported():
    alert = TransitionAlertEngine().analyze(
        transition=make_transition(
            ScenarioTransition.IMPROVING
        ),
        target_side=None,
    )

    assert alert.level == AlertLevel.INFO
    assert alert.active is True

def test_ready_same_side_has_no_repeated_alert():
    transition = ScenarioTransitionAnalysis(
        previous_state=ScenarioState.READY,
        current_state=ScenarioState.READY,
        transition=ScenarioTransition.UNCHANGED,
        reason="Le scénario reste Ready.",
        previous_target_side="BUY",
        current_target_side="BUY",
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side="BUY",
    )

    assert alert.level == AlertLevel.NONE
    assert alert.active is False


def test_sell_triggered_alert_contains_sell_side():
    transition = ScenarioTransitionAnalysis(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.READY,
        transition=ScenarioTransition.TRIGGERED,
        reason="Le scénario devient Ready.",
        previous_target_side="SELL",
        current_target_side="SELL",
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side="SELL",
    )

    assert alert.level == AlertLevel.HIGH
    assert alert.active is True
    assert "SELL" in alert.message


def test_reversal_generates_high_alert():
    transition = ScenarioTransitionAnalysis(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.BUILDING,
        transition=ScenarioTransition.REVERSAL,
        reason="Le scénario passe de BUY à SELL.",
        previous_target_side="BUY",
        current_target_side="SELL",
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side="SELL",
    )

    assert alert.level == AlertLevel.HIGH
    assert alert.active is True
    assert "SELL" in alert.message
    