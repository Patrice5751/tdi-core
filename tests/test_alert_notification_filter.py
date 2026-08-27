from tdi.graphical.alert_notification_filter import (
    AlertNotificationFilter,
)


def test_repeated_warning_after_info_is_suppressed():
    filter_ = AlertNotificationFilter()

    assert filter_.should_notify(
        symbol="NAS100",
        level="Warning",
        message="Scenario invalidated",
    ) is True

    assert filter_.should_notify(
        symbol="NAS100",
        level="Info",
        message="Scenario SELL improving",
    ) is True

    assert filter_.should_notify(
        symbol="NAS100",
        level="Warning",
        message="Scenario invalidated",
    ) is False


def test_high_alert_is_never_suppressed():
    filter_ = AlertNotificationFilter()

    assert filter_.should_notify(
        symbol="NAS100",
        level="Warning",
        message="Scenario invalidated",
    ) is True

    assert filter_.should_notify(
        symbol="NAS100",
        level="High",
        message="Scenario SELL ready",
    ) is True

def test_repeated_info_is_suppressed():
    filter_ = AlertNotificationFilter()

    assert filter_.should_notify(
        symbol="XAUUSD",
        level="Info",
        message="Scenario BUY improving",
    ) is True

    assert filter_.should_notify(
        symbol="XAUUSD",
        level="Info",
        message="Scenario BUY improving",
    ) is False

def test_warning_info_oscillation_is_suppressed():
    filter_ = AlertNotificationFilter()

    assert filter_.should_notify(
        symbol="XAUUSD",
        level="Warning",
        message="Scenario deteriorating",
    ) is True

    assert filter_.should_notify(
        symbol="XAUUSD",
        level="Info",
        message="Scenario BUY improving",
    ) is True

    assert filter_.should_notify(
        symbol="XAUUSD",
        level="Warning",
        message="Scenario deteriorating",
    ) is False

    assert filter_.should_notify(
        symbol="XAUUSD",
        level="Info",
        message="Scenario BUY improving",
    ) is False