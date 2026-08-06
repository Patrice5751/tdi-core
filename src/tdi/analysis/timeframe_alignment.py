from dataclasses import dataclass


@dataclass(frozen=True)
class TimeframeAlignment:
    aligned: bool
    score: int