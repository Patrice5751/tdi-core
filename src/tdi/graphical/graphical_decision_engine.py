from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.graphical_decision import GraphicalDecision
from tdi.graphical.graphical_decision_analysis import (
    GraphicalDecisionAnalysis,
)
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection
from tdi.models.trade import Side


class GraphicalDecisionEngine:
    def decide(
        self,
        context: GraphicalContext,
        side: Side,
    ) -> GraphicalDecisionAnalysis:
        expected_direction = (
            MarketDirection.BULLISH
            if side == Side.BUY
            else MarketDirection.BEARISH
        )

        if context.direction in {
            MarketDirection.TRANSITION,
            MarketDirection.RANGE,
        }:
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.WAIT,
                confidence=context.direction_confidence,
                reason=(
                    "La structure du marché n'est pas "
                    "suffisamment directionnelle."
                ),
            )

        if context.direction != expected_direction:
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.NO_GO,
                confidence=100 - context.direction_confidence,
                reason=(
                    "La direction du marché n'est pas alignée "
                    "avec le trade."
                ),
            )

        if context.location_type == LocationType.EXTENSION:
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.WAIT,
                confidence=context.direction_confidence,
                reason=(
                    "La direction est favorable, "
                    "mais le prix est en extension."
                ),
            )

        if context.location_type == LocationType.MIDDLE:
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.WAIT,
                confidence=context.direction_confidence,
                reason=(
                    "La direction est favorable, "
                    "mais la localisation du prix est moyenne."
                ),
            )

        if context.location_type == LocationType.PULLBACK:
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.GO,
                confidence=context.direction_confidence,
                reason=(
                    "Direction alignée et pullback favorable."
                ),
            )

        if context.location_type == LocationType.BREAKOUT:
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.GO,
                confidence=context.direction_confidence,
                reason=(
                    "Direction alignée et breakout favorable."
                ),
            )

        if (
            side == Side.BUY
            and context.location_type == LocationType.SUPPORT
        ):
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.GO,
                confidence=context.direction_confidence,
                reason=(
                    "Direction haussière et prix situé "
                    "sur une zone de support."
                ),
            )

        if (
            side == Side.SELL
            and context.location_type == LocationType.RESISTANCE
        ):
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.GO,
                confidence=context.direction_confidence,
                reason=(
                    "Direction baissière et prix situé "
                    "sur une zone de résistance."
                ),
            )

        if (
            side == Side.BUY
            and context.location_type == LocationType.RESISTANCE
        ):
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.WAIT,
                confidence=context.direction_confidence,
                reason=(
                    "Direction haussière, mais le prix est "
                    "au contact d'une résistance."
                ),
            )

        if (
            side == Side.SELL
            and context.location_type == LocationType.SUPPORT
        ):
            return GraphicalDecisionAnalysis(
                decision=GraphicalDecision.WAIT,
                confidence=context.direction_confidence,
                reason=(
                    "Direction baissière, mais le prix est "
                    "au contact d'un support."
                ),
            )

        return GraphicalDecisionAnalysis(
            decision=GraphicalDecision.WAIT,
            confidence=context.direction_confidence,
            reason="Contexte graphique insuffisamment clair.",
        )
    