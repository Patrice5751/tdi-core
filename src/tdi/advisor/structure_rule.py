from tdi.advisor.rule_result import RuleResult
from tdi.models.trade import Side
from tdi.advisor.rule_category import RuleCategory


class StructureRule:
    """Évalue la qualité de l'emplacement de l'entrée."""

    @staticmethod
    def evaluate(
        *,
        side: Side,
        entry: float,
        support: float | None,
        resistance: float | None,
        atr: float,
    ) -> RuleResult:

        if atr <= 0:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Structure",
                score=0,
                max_score=15,
                passed=False,
                message="ATR invalide.",
            )

        if side == Side.BUY:
            distance = abs(entry - support)
            level = "support"
        else:
            distance = abs(resistance - entry)
            level = "résistance"

        distance_atr = distance / atr

        if distance_atr <= 0.30:
            return RuleResult(
                category=RuleCategory.STRUCTURE,
                rule="Structure",
                score=10,
                max_score=15,   
                passed=True,
                message=(
                    f"Entrée située à {distance_atr:.2f} ATR du {level}. "
                    "Excellente localisation."
                ),
            )

        if distance_atr <= 0.50:
            return RuleResult(
                category=RuleCategory.STRUCTURE,    
                rule="Structure",
                score=5,
                max_score=15,
                passed=True,
                message=(
                    f"Entrée située à {distance_atr:.2f} ATR du {level}. "
                    "Bonne localisation."
                ),
            )

        if distance_atr <= 1.00:
            return RuleResult(                  
                category=RuleCategory.STRUCTURE,
                rule="Structure",
                score=0,
                max_score=15,
                passed=True,
                message=(
                    f"Entrée située à {distance_atr:.2f} ATR du {level}. "
                    "Entrée correcte mais améliorable."
                ),
            )

        if side == Side.BUY and support is None:
            return RuleResult(
            category=RuleCategory.STRUCTURE,                    
            rule="Structure",
            score=0,    
            passed=False,
            message="Aucun niveau de support disponible pour évaluer l'entrée.",
            )

        if side == Side.SELL and resistance is None:
            return RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Structure",
            score=0,
            max_score=15,
            passed=False,
            message="Aucun niveau de résistance disponible pour évaluer l'entrée.",
            )

        return RuleResult(
            category=RuleCategory.STRUCTURE,
            rule="Structure",
            score=-5,
            max_score=15,
            passed=False,
            message=(
                f"Entrée située à {distance_atr:.2f} ATR du {level}. "
                "Attendre un pullback."
            ),
        )