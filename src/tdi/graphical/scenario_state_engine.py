from tdi.graphical.bias_readiness import (
    BiasConvergence,
    BiasReadinessAnalysis,
)
from tdi.graphical.multi_timeframe_decision import (
    MultiTimeframeDecision,
)
from tdi.graphical.multi_timeframe_decision_analysis import (
    MultiTimeframeDecisionAnalysis,
)
from tdi.graphical.scenario_state import (
    ScenarioState,
    ScenarioStateAnalysis,
)
from tdi.graphical.wait_action_plan import WaitActionPlan
from tdi.graphical.wait_condition import WaitCondition


class ScenarioStateEngine:
    def analyze(
        self,
        decision: MultiTimeframeDecisionAnalysis,
        wait_plan: WaitActionPlan,
        bias_readiness: BiasReadinessAnalysis,
    ) -> ScenarioStateAnalysis:
        target_side = (
            decision.preferred_side
            or bias_readiness.target_side
        )

        if decision.decision in {
            MultiTimeframeDecision.BUY,
            MultiTimeframeDecision.SELL,
        }:
            return ScenarioStateAnalysis(
                target_side=target_side,
                state=ScenarioState.READY,
                score=100,
                reason=(
                    "Les conditions nécessaires à "
                    "l'entrée sont réunies."
                ),
            )

        if target_side is None:
            return ScenarioStateAnalysis(
                target_side=None,
                state=ScenarioState.INVALID,
                score=0,
                reason=(
                    "Aucun scénario directionnel "
                    "exploitable n'est identifié."
                ),
            )

        if (
            bias_readiness.convergence
            == BiasConvergence.AWAY
        ):
            return ScenarioStateAnalysis(
                target_side=target_side,
                state=ScenarioState.DEGRADING,
                score=bias_readiness.score,
                reason=(
                    f"Le scénario {target_side} existe, "
                    "mais le timeframe H1 évolue "
                    "actuellement à son encontre."
                ),
            )

        if (
            bias_readiness.convergence
            == BiasConvergence.TOWARD
        ):
            return ScenarioStateAnalysis(
                target_side=target_side,
                state=ScenarioState.BUILDING,
                score=bias_readiness.score,
                reason=(
                    f"Le scénario {target_side} se "
                    "construit : H1 converge vers "
                    "le biais H4."
                ),
            )

        if (
            bias_readiness.convergence
            == BiasConvergence.ALIGNED
        ):
            maturity_score = self._maturity_score(
                base_score=bias_readiness.score,
                conditions=wait_plan.conditions,
            )

            return ScenarioStateAnalysis(
                target_side=target_side,
                state=ScenarioState.BUILDING,
                score=maturity_score,
                reason=(
                    f"Le biais {target_side} est aligné, "
                    "mais certaines conditions d'entrée "
                    "restent à confirmer."
                ),
            )

        return ScenarioStateAnalysis(
            target_side=target_side,
            state=ScenarioState.BUILDING,
            score=bias_readiness.score,
            reason=(
                f"Le scénario {target_side} existe, "
                "mais sa convergence n'est pas encore "
                "suffisamment confirmée."
            ),
        )

    def _maturity_score(
        self,
        base_score: int,
        conditions: list,
    ) -> int:
        penalty = 0

        for condition in conditions:
            if condition in {
                WaitCondition.H4_STRUCTURE,
                WaitCondition.H1_STRUCTURE,
                WaitCondition.BIAS_ALIGNMENT,
            }:
                penalty += 15

            elif condition in {
                WaitCondition.H4_PULLBACK,
                WaitCondition.H1_PULLBACK,
                WaitCondition.H4_SUPPORT,
                WaitCondition.H1_SUPPORT,
                WaitCondition.H4_RESISTANCE,
                WaitCondition.H1_RESISTANCE,
                WaitCondition.BREAKOUT,
            }:
                penalty += 10

            elif condition == WaitCondition.MOMENTUM:
                penalty += 10

        return max(
            base_score - penalty,
            0,
        )