from dataclasses import dataclass

from tdi.graphical.wait_condition import WaitCondition


@dataclass(frozen=True)
class WaitPriority:
    condition: WaitCondition

    priority: int

    proximity_score: int

    reason: str

    importance_score: int = 0
    