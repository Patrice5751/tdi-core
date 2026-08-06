from dataclasses import dataclass


@dataclass(frozen=True)
class AdvisorResult:
    summary: str

    recommendation: str

    improvements: list[str]

    strengths: list[str]

    estimated_score: int