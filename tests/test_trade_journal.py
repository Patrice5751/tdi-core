from datetime import datetime

from tdi.journal.trade_journal import TradeJournal
from tdi.journal.trade_record import TradeRecord
from tdi.reporting.report import Report


def test_add_trade_record():
    journal = TradeJournal()

    record = TradeRecord(
        trade_id="000001",
        created_at=datetime(2026, 8, 1, 10, 0),
        report=Report(["Example"]),
        symbol="XAUUSD",
        direction="SELL",
        entry=4050,
        stop_loss=4090,
        take_profit=3970,
        tdi_version="0.9.0",
    )

    journal.add(record)

    assert len(journal.records) == 1
    assert journal.records[0] == record

def test_count_records():
    journal = TradeJournal()

    assert journal.count() == 0

def test_find_trade_by_id():
    journal = TradeJournal()

    record = TradeRecord(
        trade_id="000001",
        created_at=datetime(2026, 8, 1, 10, 0),
        report=Report(["Example"]),
        symbol="XAUUSD",
        direction="SELL",
        entry=4050,
        stop_loss=4090,
        take_profit=3970,
        tdi_version="0.9.0",
    )

    journal.add(record)

    assert journal.find_by_trade_id("000001") == record
    
        