from tdi.graphical.global_tdi_score import GlobalTDIScore


class GlobalTDIScoreEngine:
    @staticmethod
    def _grade_from_score(score: int) -> str:
        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "E"

    def compute(
        self,
        bias_score: int,
        structure_score: int,
        momentum_score: int,
        location_score: int,
        bias_available: bool,
        structure_aligned: bool,
        timing_favorable: bool,
        momentum_confirmed: bool,
    ) -> GlobalTDIScore:
        raw_score = round(
            bias_score * 0.25
            + structure_score * 0.30
            + momentum_score * 0.20
            + location_score * 0.25
        )

        score = raw_score

        if not bias_available:
            score = min(score, 25)

        elif not structure_aligned:
            score = min(score, 69)

        elif not timing_favorable:
            score = min(score, 79)

        elif not momentum_confirmed:
            score = min(score, 89)

        return GlobalTDIScore(
            score=score,
            grade=self._grade_from_score(score),
            bias_score=bias_score,
            structure_score=structure_score,
            momentum_score=momentum_score,
            location_score=location_score,
        )
    