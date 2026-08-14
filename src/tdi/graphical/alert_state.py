from dataclasses import dataclass


@dataclass(frozen=True)
class AlertState:
    level: str
    message: str
    