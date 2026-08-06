from dataclasses import dataclass


@dataclass(frozen=True)
class TradeOutcome:
    executed: bool

    result_r: float

    profit: float

    winner: bool

    notes: str = ""