import os
from collections.abc import Callable



class TelegramNotifier:
    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        post: Callable,
    ):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.post = post


    @classmethod
    def from_environment(
        cls,
        post: Callable,
    ):
        bot_token = os.environ.get(
            "TDI_TELEGRAM_BOT_TOKEN"
        )

        if not bot_token:
            raise RuntimeError(
                "Missing environment variable: "
                "TDI_TELEGRAM_BOT_TOKEN"
            )

        chat_id = os.environ.get(
            "TDI_TELEGRAM_CHAT_ID"
        )

        if not chat_id:
            raise RuntimeError(
                "Missing environment variable: "
                "TDI_TELEGRAM_CHAT_ID"
            )

        return cls(
            bot_token=bot_token,
            chat_id=chat_id,
            post=post,
        )

    def send(
        self,
        symbol: str,
        message: str,
        action: str,
        level: str | None = None,
    ) -> None:
        url = (
            "https://api.telegram.org/"
            f"bot{self.bot_token}/sendMessage"
        )

        if level is None:
            text = (
                f"TDI ALERT — {symbol}\n"
                f"{message}\n"
                f"Action: {action}"
            )
        else:
            priority_by_level = {
                "INFO": "WATCH",
                "WARNING": "CAUTION",
                "HIGH": "READY",
            }

            normalized_level = level.upper()
            priority = priority_by_level.get(
                normalized_level,
                "WATCH",
            )

            text = (
                f"TDI ALERT — {symbol}\n"
                f"Priority: {priority}\n"
                f"Level: {normalized_level}\n"
                f"{message}\n"
                f"Action: {action}"
            )

        self.post(
            url,
            data={
                "chat_id": self.chat_id,
                "text": text,
            },
            timeout=10,
        )


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