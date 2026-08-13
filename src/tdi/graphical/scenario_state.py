from dataclasses import dataclass
from enum import Enum


class ScenarioState(Enum):
    READY = "Ready"
    BUILDING = "Building"
    DEGRADING = "Degrading"
    INVALID = "Invalid"


@dataclass(frozen=True)
class ScenarioStateAnalysis:
    target_side: str | None
    state: ScenarioState
    score: int
    reason: str
    