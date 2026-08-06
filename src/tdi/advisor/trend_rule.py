from tdi.advisor.rule_result import RuleResult
from tdi.advisor.rule_category import RuleCategory


class TrendRule:
    """Évalue la qualité de la tendance."""

    @staticmethod
    def evaluate(confidence: float) -> RuleResult:
        if confidence >= 90:
            return RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Trend",
        score=20,
        max_score=20,
        passed=True,
        message="Tendance excellente.",
        )

        if confidence >= 80:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Trend",
        score=16,
        max_score=16,
        passed=True,
        message="Tendance solide.",
            )

        if confidence >= 70:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Trend",
            score=12,
            max_score=12,
            passed=True,
            message="Tendance correcte.",
        )

        if confidence >= 60:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Trend",
            score=8,
            max_score=8,
            passed=True,
            message="Tendance faible mais exploitable.",
            )

        return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Trend",
            score=0,
            max_score=0,
            passed=False,
            message="Tendance insuffisante.",
        )