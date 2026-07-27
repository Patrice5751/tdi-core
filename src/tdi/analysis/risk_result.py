from dataclasses import dataclass


@dataclass(frozen=True)
class RiskResult:
    risk_amount: float
    stop_distance: float
    target_distance: float
    rr: float
    position_size: float
    valid: bool
    reasons: list[str]