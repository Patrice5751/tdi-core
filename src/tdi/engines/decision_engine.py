from tdi.analysis.analysis_result import AnalysisResult
from tdi.analysis.decision_result import DecisionResult
from tdi.analysis.recommendation import Recommendation
from tdi.analysis.risk_result import RiskResult
from tdi.analysis.validation_result import ValidationResult
from tdi.graphical.graphical_decision import GraphicalDecision
from tdi.graphical.graphical_decision_analysis import (
    GraphicalDecisionAnalysis,
)

from config.trading_rules import (
    DECISION_ACCEPTABLE,
    DECISION_EXCELLENT,
    DECISION_GOOD,
    DECISION_RR_BONUS,
    DECISION_TREND_BONUS,
    DECISION_WAIT,
)


class DecisionEngine:
    def decide(
        self,
        analysis: AnalysisResult,
        validation: ValidationResult,
        risk: RiskResult,
        graphical_decision: GraphicalDecisionAnalysis | None = None,
    ) -> DecisionResult:
        score = self._compute_score(
            analysis,
            validation,
            risk,
        )

        confidence = score / 10

        recommendation = self._recommendation(score)
        accepted = validation.valid

        strengths = self._strengths(validation, risk)
        weaknesses = self._weaknesses(validation)

        if graphical_decision is not None:
            (
                recommendation,
                accepted,
                strengths,
                weaknesses,
            ) = self._apply_graphical_decision(
                graphical_decision=graphical_decision,
                recommendation=recommendation,
                accepted=accepted,
                strengths=strengths,
                weaknesses=weaknesses,
            )

        return DecisionResult(
            score=score,
            confidence=confidence,
            accepted=accepted,
            recommendation=recommendation,
            strengths=strengths,
            weaknesses=weaknesses,
        )

    def _compute_score(
        self,
        analysis: AnalysisResult,
        validation: ValidationResult,
        risk: RiskResult,
    ) -> int:
        score = validation.score

        if risk.rr >= 3:
            score += DECISION_RR_BONUS

        if analysis.trend.confidence >= 90:
            score += DECISION_TREND_BONUS

        return min(score, 100)

    def _recommendation(
        self,
        score: int,
    ) -> Recommendation:
        if score >= DECISION_EXCELLENT:
            return Recommendation.EXCELLENT

        if score >= DECISION_GOOD:
            return Recommendation.TAKE

        if score >= DECISION_ACCEPTABLE:
            return Recommendation.ACCEPTABLE

        if score >= DECISION_WAIT:
            return Recommendation.WAIT

        return Recommendation.REJECT

    def _apply_graphical_decision(
        self,
        graphical_decision: GraphicalDecisionAnalysis,
        recommendation: Recommendation,
        accepted: bool,
        strengths: list[str],
        weaknesses: list[str],
    ) -> tuple[
        Recommendation,
        bool,
        list[str],
        list[str],
    ]:
        if graphical_decision.decision == GraphicalDecision.GO:
            strengths.append(
                f"Contexte graphique favorable : "
                f"{graphical_decision.reason}"
            )

            return (
                recommendation,
                accepted,
                strengths,
                weaknesses,
            )

        if graphical_decision.decision == GraphicalDecision.WAIT:
            weaknesses.append(
                f"Attente graphique : "
                f"{graphical_decision.reason}"
            )

            return (
                Recommendation.WAIT,
                False,
                strengths,
                weaknesses,
            )

        weaknesses.append(
            f"Blocage graphique : "
            f"{graphical_decision.reason}"
        )

        return (
            Recommendation.REJECT,
            False,
            strengths,
            weaknesses,
        )

    def _strengths(
        self,
        validation: ValidationResult,
        risk: RiskResult,
    ) -> list[str]:
        strengths = []

        if validation.trend_ok:
            strengths.append("Tendance alignée")

        if validation.momentum_ok:
            strengths.append("Momentum confirmé")

        if validation.structure_ok:
            strengths.append("Structure favorable")

        if validation.rr_ok:
            strengths.append(
                f"Risk/Reward = {risk.rr:.2f}"
            )

        return strengths

    def _weaknesses(
        self,
        validation: ValidationResult,
    ) -> list[str]:
        weaknesses = []

        if not validation.trend_ok:
            weaknesses.append("Tendance non alignée")

        if not validation.momentum_ok:
            weaknesses.append("Momentum insuffisant")

        if not validation.structure_ok:
            weaknesses.append("Structure défavorable")

        if not validation.rr_ok:
            weaknesses.append("Risk/Reward insuffisant")

        if not weaknesses:
            weaknesses.append("Aucune faiblesse majeure")

        return weaknesses
    