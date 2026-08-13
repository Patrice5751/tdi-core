from tdi.graphical.scenario_state import ScenarioState
from tdi.graphical.scenario_transition import (
    ScenarioTransition,
)
from tdi.graphical.scenario_transition_engine import (
    ScenarioTransitionEngine,
)


def test_degrading_to_building_is_improving():
    analysis = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.DEGRADING,
        current_state=ScenarioState.BUILDING,
    )

    assert (
        analysis.transition
        == ScenarioTransition.IMPROVING
    )


def test_building_to_ready_is_triggered():
    analysis = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.READY,
    )

    assert (
        analysis.transition
        == ScenarioTransition.TRIGGERED
    )


def test_ready_to_building_is_deteriorating():
    analysis = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.READY,
        current_state=ScenarioState.BUILDING,
    )

    assert (
        analysis.transition
        == ScenarioTransition.DETERIORATING
    )


def test_building_to_degrading_is_deteriorating():
    analysis = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.DEGRADING,
    )

    assert (
        analysis.transition
        == ScenarioTransition.DETERIORATING
    )


def test_degrading_to_invalid_is_invalidated():
    analysis = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.DEGRADING,
        current_state=ScenarioState.INVALID,
    )

    assert (
        analysis.transition
        == ScenarioTransition.INVALIDATED
    )


def test_same_state_is_unchanged():
    analysis = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.BUILDING,
        current_state=ScenarioState.BUILDING,
    )

    assert (
        analysis.transition
        == ScenarioTransition.UNCHANGED
    )


def test_invalid_to_building_is_improving():
    analysis = ScenarioTransitionEngine().analyze(
        previous_state=ScenarioState.INVALID,
        current_state=ScenarioState.BUILDING,
    )

    assert (
        analysis.transition
        == ScenarioTransition.IMPROVING
    )
    