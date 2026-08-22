from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_bias_engine import (
    MarketBiasEngine,
)
from tdi.graphical.multi_timeframe_decision import (
    MultiTimeframeDecision,
)
from tdi.graphical.multi_timeframe_decision_analysis import (
    MultiTimeframeDecisionAnalysis,
)


class MultiTimeframeDecisionEngine:
    def decide(
        self,
        result: MT5MultiTimeframeResult,
        h4_momentum: MomentumAnalysis | None = None,
        h1_momentum: MomentumAnalysis | None = None,
    ) -> MultiTimeframeDecisionAnalysis:
        h4_bias = MarketBiasEngine().analyze(
            result.h4
        )

        h1_bias = MarketBiasEngine().analyze(
            result.h1
        )

        bias_aligned = (
            h4_bias.preferred_side is not None
            and h4_bias.preferred_side
            == h1_bias.preferred_side
        )

        preferred_side = (
            h4_bias.preferred_side
            if bias_aligned
            else None
        )

        confidence = min(
            h4_bias.confidence,
            h1_bias.confidence,
        )

        momentum_available = (
            h4_momentum is not None
            and h1_momentum is not None
        )

        momentum_confirmed = self._momentum_confirmed(
            preferred_side=preferred_side,
            h4_momentum=h4_momentum,
            h1_momentum=h1_momentum,
        )

        timing_favorable = self._timing_favorable(
            result=result,
            preferred_side=preferred_side,
        )

        if not bias_aligned:
            return MultiTimeframeDecisionAnalysis(
                decision=MultiTimeframeDecision.WAIT,
                preferred_side=None,
                bias_aligned=False,
                structure_aligned=result.aligned,
                timing_favorable=False,
                confidence=confidence,
                reason=(
                    "Les biais H4 et H1 ne sont pas "
                    "suffisamment alignés."
                ),
                momentum_confirmed=False,
            )
        if not result.aligned:
            return MultiTimeframeDecisionAnalysis(
                decision=MultiTimeframeDecision.WAIT,
                preferred_side=preferred_side,
                bias_aligned=True,
                structure_aligned=False,
                timing_favorable=timing_favorable,
                confidence=confidence,
                reason=(
                    f"Biais {preferred_side} aligné H4/H1, "
                    "mais structure H4/H1 non confirmée."
                ),
                momentum_confirmed=momentum_confirmed,
            )

        if not timing_favorable:
            return MultiTimeframeDecisionAnalysis(
                decision=MultiTimeframeDecision.WAIT,
                preferred_side=preferred_side,
                bias_aligned=True,
                structure_aligned=result.aligned,
                timing_favorable=False,
                confidence=confidence,
                reason=(
                    f"Biais {preferred_side} aligné H4/H1, "
                    "mais timing d'entrée insuffisant."
                ),
                momentum_confirmed=momentum_confirmed,
            )

        if not momentum_confirmed:
            return MultiTimeframeDecisionAnalysis(
                decision=MultiTimeframeDecision.WAIT,
                preferred_side=preferred_side,
                bias_aligned=True,
                structure_aligned=result.aligned,
                timing_favorable=True,
                confidence=confidence,
                reason=(
                    f"Biais {preferred_side} et timing favorables, "
                    + (
                        "mais momentum H4/H1 non confirmé."
                        if momentum_available
                        else "mais données de momentum H4/H1 absentes."
                    )
                ),
                momentum_confirmed=False,
            )

        if preferred_side == "BUY":
            decision = MultiTimeframeDecision.BUY
        else:
            decision = MultiTimeframeDecision.SELL

        return MultiTimeframeDecisionAnalysis(
            decision=decision,
            preferred_side=preferred_side,
            bias_aligned=True,
            structure_aligned=result.aligned,
            timing_favorable=True,
            confidence=confidence,
            reason=(
                f"Biais {preferred_side} aligné H4/H1, "
                "localisation favorable"
                + (
                    " et momentum confirmé."
                    if momentum_available
                    else "."
                )
            ),
            momentum_confirmed=momentum_confirmed,
        )

    def _momentum_confirmed(
        self,
        preferred_side: str | None,
        h4_momentum: MomentumAnalysis | None,
        h1_momentum: MomentumAnalysis | None,
    ) -> bool:
        if (
            preferred_side is None
            or h4_momentum is None
            or h1_momentum is None
        ):
            return False

        expected = (
            Momentum.BULLISH
            if preferred_side == "BUY"
            else Momentum.BEARISH
        )

        return (
            h4_momentum.momentum == expected
            and h1_momentum.momentum == expected
        )

    def _timing_favorable(
        self,
        result: MT5MultiTimeframeResult,
        preferred_side: str | None,
    ) -> bool:
        if preferred_side is None:
            return False

        if result.h4.location_type in {
            LocationType.EXTENSION,
            LocationType.MIDDLE,
        }:
            return False

        if result.h1.location_type in {
            LocationType.EXTENSION,
            LocationType.MIDDLE,
        }:
            return False

        if (
            preferred_side == "BUY"
            and result.h1.location_type
            == LocationType.RESISTANCE
        ):
            return False

        if (
            preferred_side == "SELL"
            and result.h1.location_type
            == LocationType.SUPPORT
        ):
            return False

        return True
    