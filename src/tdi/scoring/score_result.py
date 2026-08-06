from dataclasses import dataclass

from tdi.scoring.grade import Grade
from tdi.scoring.score_breakdown import ScoreBreakdown


@dataclass(frozen=True)
class ScoreResult:
    total_score: int
    grade: Grade
    confidence: int
    breakdown: ScoreBreakdown