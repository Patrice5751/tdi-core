import json
from pathlib import Path

from tdi.journal.trade_journal import TradeJournal


class JsonTradeJournalRepository:
    """Sauvegarde un TradeJournal dans un fichier JSON."""

    @staticmethod
    def save(journal: TradeJournal, path: str | Path) -> None:
        destination = Path(path)

        data = []

        for record in journal.records:
            data.append(
                {
                    "trade_id": record.trade_id,
                    "created_at": record.created_at.isoformat(),
                    "symbol": record.symbol,
                    "direction": record.direction,
                    "entry": record.entry,
                    "stop_loss": record.stop_loss,
                    "take_profit": record.take_profit,
                    "report": record.report.lines,
                    "tdi_version": record.tdi_version,
                }
            )

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