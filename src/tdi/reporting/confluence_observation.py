from dataclasses import dataclass

from tdi.reporting.severity import Severity


@dataclass(frozen=True)
class ConfluenceObservation:
    severity: Severity
    title: str
    message: str