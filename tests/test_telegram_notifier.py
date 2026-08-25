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
    