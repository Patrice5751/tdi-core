from dataclasses import dataclass

from tdi.graphical.transition_alert import TransitionAlert


@dataclass(frozen=True)
class AlertDeduplicationResult:
    alert: TransitionAlert
    is_new: bool
    reason: str
    