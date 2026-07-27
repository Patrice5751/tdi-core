from dataclasses import dataclass


@dataclass(frozen=True)
class MarketSnapshot:
    price: float
    ema20: float
    ema50: float
    ema200: float
    rsi: float
    macd: float
    macd_signal: float
    macd_histogram: float