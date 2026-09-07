import json
from datetime import datetime, timezone
from pathlib import Path

from tdi.analysis.intermarket_analysis import (
    IntermarketAnalysis,
)


class JsonIntermarketStateWriter:
    @staticmethod
    def write(
        analysis: IntermarketAnalysis,
        primary_symbol: str,
        confirmation_symbol: str,
        path: Path,
    ) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = {
            "primary_symbol": primary_symbol,
            "confirmation_symbol": confirmation_symbol,
            "state": analysis.state.value,
            "score": analysis.score,
            "primary_trend": analysis.primary_trend.value,
            "confirmation_trend": (
                analysis.confirmation_trend.value
            ),
            "reason": analysis.reason,
            "updated_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

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
