from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    score: int

    trend_ok: bool
    momentum_ok: bool
    structure_ok: bool

    rr_ok: bool
    risk_ok: bool
    atr_ok: bool

    valid: bool

    reasons: list[str]