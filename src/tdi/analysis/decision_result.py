from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionResult:
    score: int
    confidence: float

    accepted: bool

    recommendation: str

    strengths: list[str]
    weaknesses: list[str]