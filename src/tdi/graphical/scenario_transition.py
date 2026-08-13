from dataclasses import dataclass
from enum import Enum

from tdi.graphical.scenario_state import ScenarioState


class ScenarioTransition(Enum):
    UNCHANGED = "Unchanged"
    IMPROVING = "Improving"
    DETERIORATING = "Deteriorating"
    TRIGGERED = "Triggered"
    INVALIDATED = "Invalidated"


@dataclass(frozen=True)
class ScenarioTransitionAnalysis:
    previous_state: ScenarioState
    current_state: ScenarioState
    transition: ScenarioTransition
    reason: str
    