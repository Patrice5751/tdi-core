import json
from pathlib import Path

from tdi.graphical.scenario_state import ScenarioState


class JsonScenarioStateRepository:
    """Sauvegarde le dernier ScenarioState par symbole."""

    @staticmethod
    def save(
        symbol: str,
        state: ScenarioState,
        target_side: str | None,
        path: str | Path,
    ) -> None:
        destination = Path(path)

        data = JsonScenarioStateRepository._load_data(
            destination
        )

        data[symbol] = {
            "state": state.value,
            "target_side": target_side,
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
    ) -> tuple[ScenarioState, str | None] | None:
        source = Path(path)

        data = JsonScenarioStateRepository._load_data(
            source
        )

        record = data.get(symbol)

        if record is None:
            return None

        return (
            ScenarioState(record["state"]),
            record.get("target_side"),
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
    