from tdi.graphical.alert_state import AlertState
from tdi.graphical.json_alert_state_repository import (
    JsonAlertStateRepository,
)


def test_save_and_load_alert(tmp_path):
    path = tmp_path / "alerts.json"

    alert = AlertState(
        level="Info",
        message="Scenario improving",
    )

    JsonAlertStateRepository.save(
        symbol="XAUUSD",
        alert=alert,
        path=path,
    )

    result = JsonAlertStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    assert result == alert


def test_unknown_alert_returns_none(tmp_path):
    path = tmp_path / "alerts.json"

    result = JsonAlertStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    assert result is None


def test_multiple_alert_symbols_are_preserved(tmp_path):
    path = tmp_path / "alerts.json"

    JsonAlertStateRepository.save(
        symbol="XAUUSD",
        alert=AlertState(
            level="Info",
            message="Gold",
        ),
        path=path,
    )

    JsonAlertStateRepository.save(
        symbol="NAS100",
        alert=AlertState(
            level="Warning",
            message="Nasdaq",
        ),
        path=path,
    )

    gold = JsonAlertStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    nasdaq = JsonAlertStateRepository.load(
        symbol="NAS100",
        path=path,
    )

    assert gold.message == "Gold"
    assert nasdaq.message == "Nasdaq"

def test_delete_alert_removes_symbol_only(tmp_path):
    path = tmp_path / "alerts.json"

    JsonAlertStateRepository.save(
        symbol="XAUUSD",
        alert=AlertState(
            level="High",
            message="Gold alert",
        ),
        path=path,
    )

    JsonAlertStateRepository.save(
        symbol="NAS100",
        alert=AlertState(
            level="Warning",
            message="Nasdaq alert",
        ),
        path=path,
    )

    JsonAlertStateRepository.delete(
        symbol="XAUUSD",
        path=path,
    )

    gold = JsonAlertStateRepository.load(
        symbol="XAUUSD",
        path=path,
    )

    nasdaq = JsonAlertStateRepository.load(
        symbol="NAS100",
        path=path,
    )

    assert gold is None
    assert nasdaq is not None
    assert nasdaq.message == "Nasdaq alert"

    
    