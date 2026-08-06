from tdi.scoring.grade import Grade
from tdi.scoring.score_breakdown import ScoreBreakdown
from tdi.scoring.score_result import ScoreResult


class ScoreEngine:
    def compute(
        self,
        breakdown: ScoreBreakdown,
    ) -> ScoreResult:
        total_score = breakdown.total
        grade = self._grade_from_score(total_score)

        return ScoreResult(
            total_score=total_score,
            grade=grade,
            confidence=total_score,
            breakdown=breakdown,
        )

    @staticmethod
    def _grade_from_score(score: int) -> Grade:
        if score >= 90:
            return Grade.A

        if score >= 80:
            return Grade.B

        if score >= 70:
            return Grade.C

        if score >= 60:
            return Grade.D

        return Grade.E