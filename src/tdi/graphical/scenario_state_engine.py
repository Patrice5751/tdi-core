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
            if wait_plan.ready:
                return ScenarioStateAnalysis(
                    target_side=target_side,
                    state=ScenarioState.READY,
                    score=100,
                    reason=(
                        f"Le scénario {target_side} "
                        "est prêt."
                    ),
                )

            return ScenarioStateAnalysis(
                target_side=target_side,
                state=ScenarioState.BUILDING,
                score=max(
                    bias_readiness.score - 20,
                    0,
                ),
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
    