import pytest
from tdi.notifications.telegram_notifier import TelegramNotifier


def test_telegram_notifier_builds_expected_request(
    monkeypatch,
):
    requests = []

    def fake_post(url, data, timeout):
        requests.append(
            {
                "url": url,
                "data": data,
                "timeout": timeout,
            }
        )

    notifier = TelegramNotifier(
        bot_token="test-token",
        chat_id="123456",
        post=fake_post,
    )

    notifier.send(
        symbol="XAUUSD",
        message="Scenario BUY improving",
        action="Monitor confirmation",
    )

    assert requests == [
        {
            "url": (
                "https://api.telegram.org/"
                "bottest-token/sendMessage"
            ),
            "data": {
                "chat_id": "123456",
                "text": (
                    "TDI ALERT — XAUUSD\n"
                    "Scenario BUY improving\n"
                    "Action: Monitor confirmation"
                ),
            },
            "timeout": 10,
        }
    ]

def test_telegram_notifier_from_environment(
    monkeypatch,
):
    monkeypatch.setenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        "environment-token",
    )
    monkeypatch.setenv(
        "TDI_TELEGRAM_CHAT_ID",
        "987654",
    )

    def fake_post(url, data, timeout):
        pass

    notifier = TelegramNotifier.from_environment(
        post=fake_post,
    )

    assert notifier.bot_token == "environment-token"
    assert notifier.chat_id == "987654"

def test_telegram_notifier_requires_bot_token(
    monkeypatch,
):
    monkeypatch.delenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        raising=False,
    )
    monkeypatch.setenv(
        "TDI_TELEGRAM_CHAT_ID",
        "987654",
    )

    def fake_post(url, data, timeout):
        pass

    with pytest.raises(
        RuntimeError,
        match="TDI_TELEGRAM_BOT_TOKEN",
    ):
        TelegramNotifier.from_environment(
            post=fake_post,
        )

def test_telegram_notifier_requires_chat_id(
    monkeypatch,
):
    monkeypatch.setenv(
        "TDI_TELEGRAM_BOT_TOKEN",
        "test-token",
    )
    monkeypatch.delenv(
        "TDI_TELEGRAM_CHAT_ID",
        raising=False,
    )

    def fake_post(url, data, timeout):
        pass

    with pytest.raises(
        RuntimeError,
        match="TDI_TELEGRAM_CHAT_ID",
    ):
        TelegramNotifier.from_environment(
            post=fake_post,
        )

def test_telegram_notifier_includes_alert_level(
    monkeypatch,
):
    requests = []

    def fake_post(url, data, timeout):
        requests.append(data)

    notifier = TelegramNotifier(
        bot_token="test-token",
        chat_id="123456",
        post=fake_post,
    )

    notifier.send(
        symbol="XAUUSD",
        level="High",
        message="Scenario BUY ready",
        action="Review setup",
    )

    assert requests[0]["text"] == (
        "TDI ALERT — XAUUSD\n"
        "Priority: READY\n"
        "Level: HIGH\n"
        "Scenario BUY ready\n"
        "Action: Review setup"
    )

def test_high_alert_is_presented_as_ready():
    requests = []

    def fake_post(url, data, timeout):
        requests.append(data)

    notifier = TelegramNotifier(
        bot_token="test-token",
        chat_id="123456",
        post=fake_post,
    )

    notifier.send(
        symbol="XAUUSD",
        level="High",
        message="Scenario BUY ready",
        action="Review setup",
    )

    assert requests[0]["text"] == (
        "TDI ALERT — XAUUSD\n"
        "Priority: READY\n"
        "Level: HIGH\n"
        "Scenario BUY ready\n"
        "Action: Review setup"
    )

@pytest.mark.parametrize(
    ("level", "expected_priority"),
    [
        ("Info", "WATCH"),
        ("Warning", "CAUTION"),
        ("High", "READY"),
    ],
)
def test_alert_levels_map_to_operational_priorities(
    level,
    expected_priority,
):
    requests = []

    def fake_post(url, data, timeout):
        requests.append(data)

    notifier = TelegramNotifier(
        bot_token="test-token",
        chat_id="123456",
        post=fake_post,
    )

    notifier.send(
        symbol="XAUUSD",
        level=level,
        message="Test scenario",
        action="Test action",
    )

    text = requests[0]["text"]

    assert (
        f"Priority: {expected_priority}\n"
        in text
    )
    assert f"Level: {level.upper()}\n" in text