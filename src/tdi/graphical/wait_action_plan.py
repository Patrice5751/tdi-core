from dataclasses import dataclass

from tdi.graphical.wait_condition import WaitCondition


@dataclass(frozen=True)
class WaitActionPlan:
    preferred_side: str | None

    conditions: list[WaitCondition]

    ready: bool

    reason: str
    