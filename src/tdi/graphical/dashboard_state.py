from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardState:
    symbol: str
    decision: str
    preferred_side: str | None
    target_side: str | None

    bias_convergence: str
    bias_readiness: str
    bias_score: int

    bias_aligned: bool
    structure_aligned: bool
    timing_favorable: bool
    momentum_confirmed: bool

    scenario: str
    scenario_score: int

    waiting_for: tuple[str, ...]

    transition: str
    alert_level: str | None
    alert_active: bool

    updated_at: str = ""
