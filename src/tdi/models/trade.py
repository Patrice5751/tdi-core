from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True)
class Trade:
    instrument: str
    side: Side
    entry: float
    stop_loss: float
    take_profit: float
    capital: float
    risk_percent: float
    timeframe: str
    atr: float
    created_at: datetime