from tdi.graphical.scenario_state import ScenarioState
from tdi.graphical.scenario_transition import ScenarioTransition
from tdi.graphical.scenario_transition_engine import (
    ScenarioTransitionEngine,
)
from tdi.graphical.transition_alert import AlertLevel
from tdi.graphical.transition_alert_engine import (
    TransitionAlertEngine,
)


def test_building_to_ready_buy_triggers_high_alert():
    transition = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.READY,
        previous_target_side="BUY",
        current_target_side="BUY",
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side="BUY",
    )

    assert transition.transition == ScenarioTransition.TRIGGERED
    assert alert.level == AlertLevel.HIGH
    assert alert.active is True
    assert "BUY" in alert.message


def test_building_to_ready_sell_triggers_high_alert():
    transition = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.READY,
        previous_target_side="SELL",
        current_target_side="SELL",
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side="SELL",
    )

    assert transition.transition == ScenarioTransition.TRIGGERED
    assert alert.level == AlertLevel.HIGH
    assert alert.active is True
    assert "SELL" in alert.message


def test_building_to_building_never_triggers_entry_alert():
    transition = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.BUILDING,
        previous_target_side="BUY",
        current_target_side="BUY",
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side="BUY",
    )

    assert transition.transition != ScenarioTransition.TRIGGERED
    assert alert.level != AlertLevel.HIGH
    assert alert.active is False


def test_ready_same_side_does_not_repeat_trigger_alert():
    transition = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.READY,
        current_state=ScenarioState.READY,
        previous_target_side="BUY",
        current_target_side="BUY",
    )

    alert = TransitionAlertEngine().analyze(
        transition=transition,
        target_side="BUY",
    )

    assert transition.transition == ScenarioTransition.UNCHANGED
    assert alert.level == AlertLevel.NONE
    assert alert.active is False