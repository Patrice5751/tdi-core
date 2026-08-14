import json
from pathlib import Path

from tdi.graphical.alert_state import AlertState


class JsonAlertStateRepository:
    """Sauvegarde la dernière alerte active par symbole."""

    @staticmethod
    def save(
        symbol: str,
        alert: AlertState,
        path: str | Path,
    ) -> None:
        destination = Path(path)

        data = JsonAlertStateRepository._load_data(
            destination
        )

        data[symbol] = {
            "level": alert.level,
            "message": alert.message,
        }

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def load(
        symbol: str,
        path: str | Path,
    ) -> AlertState | None:
        source = Path(path)

        data = JsonAlertStateRepository._load_data(
            source
        )

        record = data.get(symbol)

        if record is None:
            return None

        return AlertState(
            level=record["level"],
            message=record["message"],
        )

    @staticmethod
    def _load_data(
        path: Path,
    ) -> dict:
        if not path.exists():
            return {}

        content = path.read_text(
            encoding="utf-8",
        ).strip()

        if not content:
            return {}

        return json.loads(content)
    