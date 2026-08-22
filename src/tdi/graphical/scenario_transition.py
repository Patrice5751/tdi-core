from dataclasses import dataclass
from enum import Enum

from tdi.graphical.scenario_state import ScenarioState


class ScenarioTransition(Enum):
    UNCHANGED = "Unchanged"
    IMPROVING = "Improving"
    DETERIORATING = "Deteriorating"
    TRIGGERED = "Triggered"
    INVALIDATED = "Invalidated"
    REVERSAL = "Reversal"


@dataclass(frozen=True)
class ScenarioTransitionAnalysis:
    previous_state: ScenarioState
    current_state: ScenarioState
    transition: ScenarioTransition
    reason: str

    previous_target_side: str | None = None
    current_target_side: str | None = None
    