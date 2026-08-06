from dataclasses import dataclass


@dataclass(frozen=True)
class TradeSetup:
    symbol: str
    direction: str

    entry: float
    stop_loss: float
    take_profit: float

    atr_h4: float

    capital: float
    risk_percent: float

    