from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.bias_readiness import (
    BiasConvergence,
    BiasReadiness,
    BiasReadinessAnalysis,
)
from tdi.graphical.market_bias_engine import (
    MarketBiasEngine,
)


class BiasReadinessEngine:
    def analyze(
        self,
        result: MT5MultiTimeframeResult,
        h1_momentum: MomentumAnalysis | None = None,
    ) -> BiasReadinessAnalysis:
        h4_bias = MarketBiasEngine().analyze(
            result.h4
        )

        h1_bias = MarketBiasEngine().analyze(
            result.h1
        )

        target_side = h4_bias.preferred_side

        if target_side is None:
            return BiasReadinessAnalysis(
                target_side=None,
                readiness=BiasReadiness.LOW,
                convergence=BiasConvergence.UNDEFINED,
                score=0,
                reason=(
                    "Aucun biais H4 exploitable pour "
                    "définir une direction cible."
                ),
            )

        if h1_bias.preferred_side == target_side:
            return BiasReadinessAnalysis(
                target_side=target_side,
                readiness=BiasReadiness.HIGH,
                convergence=BiasConvergence.ALIGNED,
                score=100,
                reason=(
                    f"Le biais H1 est déjà aligné "
                    f"avec le biais H4 {target_side}."
                ),
            )

        if (
            h1_bias.preferred_side is not None
            and h1_bias.preferred_side != target_side
        ):
            return BiasReadinessAnalysis(
                target_side=target_side,
                readiness=BiasReadiness.LOW,
                convergence=BiasConvergence.AWAY,
                score=0,
                reason=(
                    "Le biais H1 est opposé "
                    "au biais directionnel H4."
                ),
            )

        return self._analyze_neutral_h1(
            target_side=target_side,
            h1_momentum=h1_momentum,
        )

    def _analyze_neutral_h1(
        self,
        target_side: str,
        h1_momentum: MomentumAnalysis | None,
    ) -> BiasReadinessAnalysis:
        if h1_momentum is None:
            return BiasReadinessAnalysis(
                target_side=target_side,
                readiness=BiasReadiness.LOW,
                convergence=BiasConvergence.UNDEFINED,
                score=20,
                reason=(
                    "Le biais H1 est neutre et le momentum "
                    "H1 n'est pas disponible."
                ),
            )

        expected = (
            Momentum.BULLISH
            if target_side == "BUY"
            else Momentum.BEARISH
        )

        opposite = (
            Momentum.BEARISH
            if target_side == "BUY"
            else Momentum.BULLISH
        )

        if h1_momentum.momentum == expected:
            score = min(
                50 + (h1_momentum.confidence // 2),
                90,
            )

            return BiasReadinessAnalysis(
                target_side=target_side,
                readiness=BiasReadiness.MEDIUM,
                convergence=BiasConvergence.TOWARD,
                score=score,
                reason=(
                    f"Le biais H1 est encore neutre, "
                    f"mais son momentum converge vers "
                    f"le biais H4 {target_side}."
                ),
            )

        if h1_momentum.momentum == opposite:
            return BiasReadinessAnalysis(
                target_side=target_side,
                readiness=BiasReadiness.LOW,
                convergence=BiasConvergence.AWAY,
                score=max(
                    30 - (h1_momentum.confidence // 3),
                    0,
                ),
                reason=(
                    f"Le biais H1 est neutre et son "
                    f"momentum évolue à l'opposé du "
                    f"biais H4 {target_side}."
                ),
            )

        return BiasReadinessAnalysis(
            target_side=target_side,
            readiness=BiasReadiness.LOW,
            convergence=BiasConvergence.UNDEFINED,
            score=30,
            reason=(
                "Le biais H1 et son momentum restent "
                "neutres : convergence non confirmée."
            ),
        )
    