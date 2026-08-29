import json
from dataclasses import asdict
from pathlib import Path

from tdi.graphical.dashboard_state import DashboardState


class JsonDashboardStateWriter:
    @staticmethod
    def write(
        state: DashboardState,
        path: Path,
    ) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = asdict(state)

        temp_path = path.with_suffix(
            path.suffix + ".tmp"
        )

        temp_path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        temp_path.replace(path)