from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalTDIScore:
    score: int
    grade: str

    bias_score: int
    structure_score: int
    momentum_score: int
    location_score: int
    