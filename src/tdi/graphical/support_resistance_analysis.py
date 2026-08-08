from dataclasses import dataclass


@dataclass(frozen=True)
class SupportResistanceAnalysis:
    support: float | None
    resistance: float | None
    support_touches: int
    resistance_touches: int