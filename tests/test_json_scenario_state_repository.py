from tdi.graphical.json_scenario_state_repository import (
    JsonScenarioStateRepository,
)
from tdi.graphical.scenario_state import ScenarioState


def test_save_and_load_state(tmp_path):
    path = tmp_path / "scenario_states.json"

    JsonScenarioStateRepository.save(
        symbol="XAUUSD",
        state=ScenarioState.DEGRADING,
        target_side="BUY",
        path=path,
    )

    result = JsonScenarioStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    assert result == (
        ScenarioState.DEGRADING,
        "BUY",
    )


def test_unknown_symbol_returns_none(tmp_path):
    path = tmp_path / "scenario_states.json"

    result = JsonScenarioStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    assert result is None


def test_multiple_symbols_are_preserved(tmp_path):
    path = tmp_path / "scenario_states.json"

    JsonScenarioStateRepository.save(
        symbol="XAUUSD",
        state=ScenarioState.DEGRADING,
        target_side="BUY",
        path=path,
    )

    JsonScenarioStateRepository.save(
        symbol="NAS100",
        state=ScenarioState.BUILDING,
        target_side="SELL",
        path=path,
    )

    gold = JsonScenarioStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    nasdaq = JsonScenarioStateRepository.load(
        symbol="NAS100",
        path=path,
    )

    assert gold == (
        ScenarioState.DEGRADING,
        "BUY",
    )

    assert nasdaq == (
        ScenarioState.BUILDING,
        "SELL",
    )


def test_existing_symbol_is_updated(tmp_path):
    path = tmp_path / "scenario_states.json"

    JsonScenarioStateRepository.save(
        symbol="XAUUSD",
        state=ScenarioState.DEGRADING,
        target_side="BUY",
        path=path,
    )

    JsonScenarioStateRepository.save(
        symbol="XAUUSD",
        state=ScenarioState.BUILDING,
        target_side="BUY",
        path=path,
    )

    result = JsonScenarioStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    assert result == (
        ScenarioState.BUILDING,
        "BUY",
    )


def test_repository_creates_parent_directory(tmp_path):
    path = (
        tmp_path
        / "data"
        / "scenario_states.json"
    )

    JsonScenarioStateRepository.save(
        symbol="XAUUSD",
        state=ScenarioState.DEGRADING,
        target_side="BUY",
        path=path,
    )

    assert path.exists()
    