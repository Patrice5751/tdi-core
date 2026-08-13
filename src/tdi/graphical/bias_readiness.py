from dataclasses import dataclass
from enum import Enum


class BiasReadiness(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class BiasConvergence(Enum):
    TOWARD = "Toward"
    AWAY = "Away"
    ALIGNED = "Aligned"
    UNDEFINED = "Undefined"


@dataclass(frozen=True)
class BiasReadinessAnalysis:
    target_side: str | None
    readiness: BiasReadiness
    convergence: BiasConvergence
    score: int
    reason: str
    