from datetime import datetime

from tdi.journal.trade_record import TradeRecord
from tdi.reporting.report import Report


def test_create_trade_record():
    record = TradeRecord(
        trade_id="000001",
        created_at=datetime(2026, 8, 1, 10, 0),

        symbol="XAUUSD",
        direction="SELL",

        entry=4050,
        stop_loss=4090,
        take_profit=3970,

        report=Report(["Example"]),

        tdi_version="0.9.0",
    )

    assert record.trade_id == "000001"
    assert record.symbol == "XAUUSD"
    assert record.direction == "SELL"
    assert record.tdi_version == "0.9.0"