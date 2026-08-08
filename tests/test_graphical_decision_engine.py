from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.graphical_decision import GraphicalDecision
from tdi.graphical.graphical_decision_engine import GraphicalDecisionEngine
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection
from tdi.models.trade import Side


def make_context(
    direction=MarketDirection.BULLISH,
    location_type=LocationType.PULLBACK,
    confidence=90,
):
    return GraphicalContext(
        direction=direction,
        direction_confidence=confidence,
        location_type=location_type,
        support=100.0,
        resistance=120.0,
        support_touches=3,
        resistance_touches=2,
    )


def test_buy_bullish_pullback_returns_go():
    result = GraphicalDecisionEngine().decide(
        context=make_context(),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.GO


def test_sell_bearish_resistance_returns_go():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.BEARISH,
            location_type=LocationType.RESISTANCE,
        ),
        side=Side.SELL,
    )

    assert result.decision == GraphicalDecision.GO


def test_buy_against_bearish_direction_returns_no_go():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.BEARISH,
        ),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.NO_GO


def test_extension_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            location_type=LocationType.EXTENSION,
        ),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.WAIT


def test_middle_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            location_type=LocationType.MIDDLE,
        ),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.WAIT

def test_buy_on_support_returns_go():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.BULLISH,
            location_type=LocationType.SUPPORT,
        ),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.GO


def test_buy_on_resistance_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.BULLISH,
            location_type=LocationType.RESISTANCE,
        ),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.WAIT


def test_sell_on_resistance_returns_go():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.BEARISH,
            location_type=LocationType.RESISTANCE,
        ),
        side=Side.SELL,
    )

    assert result.decision == GraphicalDecision.GO


def test_sell_on_support_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.BEARISH,
            location_type=LocationType.SUPPORT,
        ),
        side=Side.SELL,
    )

    assert result.decision == GraphicalDecision.WAIT

def test_transition_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.TRANSITION,
            location_type=LocationType.MIDDLE,
        ),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.WAIT


def test_range_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.RANGE,
            location_type=LocationType.MIDDLE,
        ),
        side=Side.SELL,
    )

    assert result.decision == GraphicalDecision.WAIT

def test_transition_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.TRANSITION,
            location_type=LocationType.MIDDLE,
        ),
        side=Side.BUY,
    )

    assert result.decision == GraphicalDecision.WAIT


def test_range_returns_wait():
    result = GraphicalDecisionEngine().decide(
        context=make_context(
            direction=MarketDirection.RANGE,
            location_type=LocationType.MIDDLE,
        ),
        side=Side.SELL,
    )

    assert result.decision == GraphicalDecision.WAIT
    

