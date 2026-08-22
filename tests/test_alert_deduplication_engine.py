from tdi.graphical.alert_deduplication_engine import (
    AlertDeduplicationEngine,
)
from tdi.graphical.alert_state import AlertState
from tdi.graphical.transition_alert import (
    AlertLevel,
    TransitionAlert,
)


def make_alert(
    level=AlertLevel.INFO,
    active=True,
    message="Le scénario BUY s'améliore.",
):
    return TransitionAlert(
        level=level,
        active=active,
        message=message,
        action="Surveiller.",
    )


def test_first_active_alert_is_new():
    result = AlertDeduplicationEngine().analyze(
        current_alert=make_alert(),
        previous_alert=None,
    )

    assert result.is_new is True


def test_identical_alert_is_not_new():
    current = make_alert()

    previous = AlertState(
        level=current.level.value,
        message=current.message,
    )

    result = AlertDeduplicationEngine().analyze(
        current_alert=current,
        previous_alert=previous,
    )

    assert result.is_new is False


def test_different_level_is_new():
    current = make_alert(
        level=AlertLevel.WARNING,
    )

    previous = AlertState(
        level=AlertLevel.INFO.value,
        message=current.message,
    )

    result = AlertDeduplicationEngine().analyze(
        current_alert=current,
        previous_alert=previous,
    )

    assert result.is_new is True


def test_different_message_is_new():
    current = make_alert(
        message="Le scénario BUY se détériore.",
    )

    previous = AlertState(
        level=current.level.value,
        message="Le scénario BUY s'améliore.",
    )

    result = AlertDeduplicationEngine().analyze(
        current_alert=current,
        previous_alert=previous,
    )

    assert result.is_new is True


def test_inactive_alert_is_never_new():
    result = AlertDeduplicationEngine().analyze(
        current_alert=make_alert(
            level=AlertLevel.NONE,
            active=False,
            message="Aucun changement.",
        ),
        previous_alert=None,
    )

    assert result.is_new is False

def test_identical_high_trigger_alert_is_not_new():
    current = make_alert(
        level=AlertLevel.HIGH,
        active=True,
        message="Le scénario BUY atteint l'état Ready.",
    )

    previous = AlertState(
        level=AlertLevel.HIGH.value,
        message=current.message,
    )

    result = AlertDeduplicationEngine().analyze(
        current_alert=current,
        previous_alert=previous,
    )

    assert result.is_new is False