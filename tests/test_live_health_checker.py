import os
from datetime import datetime, timedelta, timezone

from tdi.services.live_health_checker import LiveHealthChecker


def test_live_health_checker_reports_healthy_for_recent_file(tmp_path):
    state_file = tmp_path / "XAUUSD.json"
    state_file.write_text("{}", encoding="utf-8")

    now = datetime.now(timezone.utc)

    checker = LiveHealthChecker(stale_after_seconds=300)

    assert checker.is_healthy(state_file, now=now) is True


def test_live_health_checker_reports_stale_for_old_file(tmp_path):
    state_file = tmp_path / "XAUUSD.json"
    state_file.write_text("{}", encoding="utf-8")

    now = datetime.now(timezone.utc)
    old_time = now - timedelta(seconds=301)

    os.utime(
        state_file,
        (old_time.timestamp(), old_time.timestamp()),
    )

    checker = LiveHealthChecker(stale_after_seconds=300)

    assert checker.is_healthy(state_file, now=now) is False


def test_live_health_checker_reports_stale_for_missing_file(tmp_path):
    state_file = tmp_path / "XAUUSD.json"

    checker = LiveHealthChecker(stale_after_seconds=300)

    assert checker.is_healthy(state_file) is False

def test_live_health_checker_reports_healthy_at_stale_threshold(tmp_path):
    state_file = tmp_path / "XAUUSD.json"
    state_file.write_text("{}", encoding="utf-8")

    now = datetime.now(timezone.utc)
    threshold_time = now - timedelta(seconds=300)

    os.utime(
        state_file,
        (threshold_time.timestamp(), threshold_time.timestamp()),
    )

    checker = LiveHealthChecker(stale_after_seconds=300)

    assert checker.is_healthy(state_file, now=now) is True

def test_live_health_checker_requires_recovery_when_any_file_is_stale(
    tmp_path,
):
    fresh_file = tmp_path / "XAUUSD.json"
    stale_file = tmp_path / "ETHUSD.json"

    fresh_file.write_text("{}", encoding="utf-8")
    stale_file.write_text("{}", encoding="utf-8")

    now = datetime.now(timezone.utc)
    old_time = now - timedelta(seconds=301)

    os.utime(
        stale_file,
        (old_time.timestamp(), old_time.timestamp()),
    )

    checker = LiveHealthChecker(stale_after_seconds=300)

    assert checker.requires_recovery(
        [fresh_file, stale_file],
        now=now,
    ) is True


def test_live_health_checker_does_not_require_recovery_when_all_files_are_fresh(
    tmp_path,
):
    first_file = tmp_path / "XAUUSD.json"
    second_file = tmp_path / "ETHUSD.json"

    first_file.write_text("{}", encoding="utf-8")
    second_file.write_text("{}", encoding="utf-8")

    now = datetime.now(timezone.utc)

    checker = LiveHealthChecker(stale_after_seconds=300)

    assert checker.requires_recovery(
        [first_file, second_file],
        now=now,
    ) is False
