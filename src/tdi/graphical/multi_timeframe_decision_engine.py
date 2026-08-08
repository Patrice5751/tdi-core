from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
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

        timing_favorable = self._timing_favorable(
            result=result,
            preferred_side=preferred_side,
        )

        confidence = min(
            h4_bias.confidence,
            h1_bias.confidence,
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
                f"Biais {preferred_side} aligné H4/H1 "
                "avec localisation favorable."
            ),
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
    