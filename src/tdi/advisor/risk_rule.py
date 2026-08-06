from tdi.advisor.rule_result import RuleResult
from tdi.advisor.rule_category import RuleCategory


class RiskRule:
    """Évalue la qualité de la gestion du risque."""

    @staticmethod
    def evaluate(
        risk_ok: bool,
    ) -> RuleResult:
        if risk_ok:
            return RuleResult(
                category=RuleCategory.RISK,
                rule="Risk",
                score=15,
                max_score=15,
                passed=True,
                message="Risque monétaire conforme.",
            )

        return RuleResult(
            category=RuleCategory.RISK,
            rule="Risk",
            score=0,
            max_score=15,
            passed=False,
            message=(
                "Réduire la taille de position afin de respecter "
                "le risque maximal."
            ),
        )