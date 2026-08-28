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

        path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        