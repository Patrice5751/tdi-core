from dataclasses import dataclass


@dataclass(frozen=True)
class IndicatorResult:
    ma20: float | None
    ma50: float | None
    ma200: float | None
    atr: float | None

    rsi: float | None = None
    macd: float | None = None
    macd_signal: float | None = None
    macd_histogram: float | None = None
    