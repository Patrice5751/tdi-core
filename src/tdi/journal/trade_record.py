from dataclasses import dataclass
from datetime import datetime

from tdi.reporting.report import Report


@dataclass(frozen=True)
class TradeRecord:

    trade_id: str

    created_at: datetime

    report: Report

    symbol: str

    direction: str

    entry: float

    stop_loss: float

    take_profit: float

    tdi_version: str