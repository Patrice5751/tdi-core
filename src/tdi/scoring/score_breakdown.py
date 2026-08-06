from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreBreakdown:
    trend: int
    structure: int
    momentum: int
    alignment: int
    rr: int
    atr: int
    risk: int

    @property
    def total(self) -> int:
        return (
            self.trend
            + self.structure
            + self.momentum
            + self.alignment
            + self.rr
            + self.atr
            + self.risk
        )