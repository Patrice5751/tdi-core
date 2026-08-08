from dataclasses import dataclass


@dataclass(frozen=True)
class MAConfirmationAnalysis:
    score: int
    bullish: bool
    bearish: bool
    reason: str
    