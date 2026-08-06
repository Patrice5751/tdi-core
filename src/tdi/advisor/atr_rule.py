from tdi.advisor.rule_result import RuleResult
from tdi.advisor.rule_category import RuleCategory


class ATRRule:
    """Évalue la cohérence du Stop Loss avec l'ATR."""

    @staticmethod
    def evaluate(
        atr_ok: bool,
    ) -> RuleResult:
        if atr_ok:
            return RuleResult(
                category=RuleCategory.RISK,
                rule="ATR",
                score=10,
                max_score=15,   
                passed=True,
                message="Stop Loss cohérent avec la volatilité.",
            )

        return RuleResult(
            category=RuleCategory.RISK,
            rule="ATR",
            score=0,
            max_score=15,
            passed=False,
            message=(
                "Repositionner le Stop Loss en fonction "
                "de la volatilité ATR."
            ),
        )