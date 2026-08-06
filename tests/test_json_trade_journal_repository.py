import json
from datetime import datetime

from tdi.journal.json_trade_journal_repository import (
    JsonTradeJournalRepository,
)
from tdi.journal.trade_journal import TradeJournal
from tdi.journal.trade_record import TradeRecord
from tdi.reporting.report import Report


def test_save_trade_journal_to_json(tmp_path):
    journal = TradeJournal()

    record = TradeRecord(
        trade_id="000001",
        created_at=datetime(2026, 8, 1, 10, 0),
        report=Report(["Example report"]),
        symbol="XAUUSD",
        direction="SELL",
        entry=4050.0,
        stop_loss=4090.0,
        take_profit=3970.0,
        tdi_version="0.9.0",
    )

    journal.add(record)

    destination = tmp_path / "journal.json"

    JsonTradeJournalRepository.save(
        journal,
        destination,
    )

    saved_data = json.loads(
        destination.read_text(encoding="utf-8")
    )

    assert len(saved_data) == 1
    assert saved_data[0]["trade_id"] == "000001"
    assert saved_data[0]["symbol"] == "XAUUSD"
    assert saved_data[0]["report"] == ["Example report"]
    assert saved_data[0]["tdi_version"] == "0.9.0"