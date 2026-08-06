from tdi.advisor.score_aggregator import ScoreAggregator
from tdi.analysis.advisor_result import AdvisorResult
from tdi.analysis.analysis_result import AnalysisResult
from tdi.analysis.decision_result import DecisionResult
from tdi.analysis.risk_result import RiskResult
from tdi.analysis.validation_result import ValidationResult
from tdi.models.trade import Trade
from tdi.advisor.rule_engine import RuleEngine

class TradeAdvisor:
    """Produit des conseils d'amélioration à partir des résultats TDI.

    Le TradeAdvisor orchestre les règles de conseil sans modifier
    la décision produite par le DecisionEngine.
    """

    def advise(
        self,
        trade: Trade,
        analysis: AnalysisResult,
        validation: ValidationResult,
        decision: DecisionResult,
        risk: RiskResult,
    ) -> AdvisorResult:
        rule_results = RuleEngine.evaluate(
            trade=trade,
            analysis=analysis,
            validation=validation,
            risk=risk,
        )

        strengths = ScoreAggregator.strengths(rule_results)
        improvements = ScoreAggregator.weaknesses(rule_results)

        self._append_rr_optimization(
            improvements=improvements,
            validation=validation,
            risk=risk,
        )

        return AdvisorResult(
            summary=self._summary(decision),
            recommendation=self._recommendation(
                validation=validation,
                decision=decision,
                improvements=improvements,
            ),
            improvements=improvements,
            strengths=strengths,
            estimated_score=self._estimated_score(
                current_score=decision.score,
                improvements=improvements,
            ),
        )

    @staticmethod
    def _summary(decision: DecisionResult) -> str:
        if decision.accepted:
            return "Le trade est valide selon les règles TDI."

        return "Le trade présente plusieurs faiblesses."

    @staticmethod
    def _recommendation(
        validation: ValidationResult,
        decision: DecisionResult,
        improvements: list[str],
    ) -> str:
        if decision.accepted and not improvements:
            return (
                "Le setup est propre. "
                "Aucune amélioration majeure détectée."
            )

        if not validation.structure_ok:
            return "Attendre une meilleure zone d'entrée."

        if not validation.momentum_ok:
            return "Attendre une confirmation du momentum."

        if not validation.rr_ok:
            return (
                "Améliorer le ratio rendement/risque avant d'entrer."
            )

        if decision.accepted:
            return (
                "Le trade est acceptable, "
                "mais il peut encore être optimisé."
            )

        return "Ne pas prendre le trade dans sa configuration actuelle."

    @staticmethod
    def _append_rr_optimization(
        improvements: list[str],
        validation: ValidationResult,
        risk: RiskResult,
    ) -> None:
        """Conserve le conseil d'optimisation pour un RR valide sous 3."""

        if validation.rr_ok and risk.rr < 3:
            improvements.append(
                f"Le ratio rendement/risque de {risk.rr:.2f} "
                "est valide, mais une meilleure entrée pourrait "
                "le rapprocher de 3,00."
            )

    @staticmethod
    def _estimated_score(
        current_score: int,
        improvements: list[str],
    ) -> int:
        potential_gain = len(improvements) * 3

        return min(current_score + potential_gain, 100)