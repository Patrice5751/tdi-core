import json
from datetime import datetime, timezone
from pathlib import Path

from tdi.analysis.intermarket_v2_analysis import (
    IntermarketV2Analysis,
)


class JsonIntermarketV2StateWriter:
    @staticmethod
    def write(
        analysis: IntermarketV2Analysis,
        path: Path,
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": 2,
            "primary_symbol": "XAUUSD",
            "state": analysis.state.value,
            "score": analysis.score,
            "coverage": analysis.coverage,
            "primary_trend": analysis.primary_trend.value,
            "confirmations": {
                "XAGUSD": {
                    "trend": (
                        analysis.silver_trend.value
                        if analysis.silver_trend is not None
                        else None
                    ),
                    "score": analysis.silver_score,
                    "weight": 60,
                    "relationship": "Direct",
                },
                "USDX": {
                    "trend": (
                        analysis.dollar_trend.value
                        if analysis.dollar_trend is not None
                        else None
                    ),
                    "score": analysis.dollar_score,
                    "weight": 40,
                    "relationship": "Inverse",
                },
            },
            "reason": analysis.reason,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        temp_path = path.with_suffix(path.suffix + ".tmp")
        temp_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temp_path.replace(path)
        