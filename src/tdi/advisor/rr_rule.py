
from tdi.advisor.rule_result import RuleResult
from tdi.advisor.rule_category import RuleCategory


class RRRule:
    """Évalue la qualité du ratio rendement/risque."""

    @staticmethod
    def evaluate(
        rr: float,
        minimum_rr: float = 1.5,
    ) -> RuleResult:
        if rr < minimum_rr:
            return RuleResult(
                category=RuleCategory.RISK,
                rule="RiskReward",  
                score=0,
                max_score=15,
                passed=False,
                message=(
                    f"Ratio rendement/risque insuffisant : {rr:.2f}. "
                    f"Minimum requis : {minimum_rr:.2f}."
                ),
            )

        if rr < 2.0:
            return RuleResult(
                category=RuleCategory.RISK, 
                rule="RiskReward",
                score=5, 
                max_score=15,
                passed=True,
                message=f"Ratio rendement/risque acceptable : {rr:.2f}.",
            )

        if rr < 2.5:
            return RuleResult(
                category=RuleCategory.RISK,
                rule="RiskReward",
                score=10,
                max_score=15,
                passed=True,
                message=f"Bon ratio rendement/risque : {rr:.2f}.",
            )

        if rr < 3.0:
            return RuleResult(
                category=RuleCategory.RISK,
                rule="RiskReward",
                score=13,
                max_score=15,
                passed=True,
                message=f"Très bon ratio rendement/risque : {rr:.2f}.",
            )

        return RuleResult(
            category=RuleCategory.RISK,
            rule="RiskReward",
            score=15,
            max_score=15,
            passed=True,
            message=f"Excellent ratio rendement/risque : {rr:.2f}.",
        )