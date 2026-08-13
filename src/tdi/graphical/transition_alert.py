from dataclasses import dataclass
from enum import Enum


class AlertLevel(Enum):
    NONE = "None"
    INFO = "Info"
    WARNING = "Warning"
    HIGH = "High"


@dataclass(frozen=True)
class TransitionAlert:
    level: AlertLevel
    active: bool
    message: str
    action: str
    