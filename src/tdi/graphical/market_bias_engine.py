from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.market_bias import MarketBias
from tdi.graphical.market_bias_analysis import (
    MarketBiasAnalysis,
)
from tdi.graphical.market_direction import MarketDirection


class MarketBiasEngine:
    def analyze(
        self,
        context: GraphicalContext,
    ) -> MarketBiasAnalysis:
        if context.ma_bullish:
            if context.direction == MarketDirection.BULLISH:
                return MarketBiasAnalysis(
                    bias=MarketBias.STRONG_BULLISH,
                    confidence=100,
                    preferred_side="BUY",
                    reason=(
                        "Structure haussière confirmée "
                        "par les moyennes mobiles."
                    ),
                )

            return MarketBiasAnalysis(
                bias=MarketBias.BULLISH,
                confidence=context.ma_confirmation_score,
                preferred_side="BUY",
                reason=(
                    "Biais haussier des moyennes mobiles, "
                    "structure non confirmée."
                ),
            )

        if context.ma_bearish:
            if context.direction == MarketDirection.BEARISH:
                return MarketBiasAnalysis(
                    bias=MarketBias.STRONG_BEARISH,
                    confidence=100,
                    preferred_side="SELL",
                    reason=(
                        "Structure baissière confirmée "
                        "par les moyennes mobiles."
                    ),
                )

            return MarketBiasAnalysis(
                bias=MarketBias.BEARISH,
                confidence=context.ma_confirmation_score,
                preferred_side="SELL",
                reason=(
                    "Biais baissier des moyennes mobiles, "
                    "structure non confirmée."
                ),
            )

        return MarketBiasAnalysis(
            bias=MarketBias.NEUTRAL,
            confidence=0,
            preferred_side=None,
            reason=(
                "Aucun biais directionnel suffisamment "
                "confirmé."
            ),
        )
    