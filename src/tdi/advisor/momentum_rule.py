from tdi.advisor.rule_result import RuleResult
from tdi.advisor.rule_category import RuleCategory


class MomentumRule:
    """Évalue la qualité du momentum."""

    @staticmethod
    def evaluate(confidence: float) -> RuleResult:
        if confidence >= 90:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Momentum",
                score=20,
                max_score=20,
                passed=True,
                message="Momentum excellent.",
            )

        if confidence >= 80:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Momentum",
                score=16,
                max_score=16,
                passed=True,
                message="Momentum fort.",
            )

        if confidence >= 70:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Momentum",
                score=12,
                max_score=12,
                passed=True,
                message="Momentum correct.",
            )

        if confidence >= 60:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Momentum",
                score=8,
                max_score=8,
                passed=True,
                message="Momentum faible mais exploitable.",
            )

        return RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Momentum",
            score=0,
            max_score=0,
            passed=False,
            message="Attendre une confirmation du momentum.",
        )