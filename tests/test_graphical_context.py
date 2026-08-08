from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection


def test_create_graphical_context():
    context = GraphicalContext(
        direction=MarketDirection.BULLISH,
        direction_confidence=85,
        location_type=LocationType.PULLBACK,
        support=4160.0,
        resistance=4250.0,
        support_touches=3,
        resistance_touches=2,
    )

    assert context.direction == MarketDirection.BULLISH
    assert context.direction_confidence == 85
    assert context.location_type == LocationType.PULLBACK

    assert context.support == 4160.0
    assert context.resistance == 4250.0

    assert context.support_touches == 3
    assert context.resistance_touches == 2


def test_graphical_context_accepts_missing_levels():
    context = GraphicalContext(
        direction=MarketDirection.RANGE,
        direction_confidence=40,
        location_type=LocationType.MIDDLE,
        support=None,
        resistance=None,
        support_touches=0,
        resistance_touches=0,
    )

    assert context.support is None
    assert context.resistance is None


def test_graphical_context_is_immutable():
    context = GraphicalContext(
        direction=MarketDirection.BULLISH,
        direction_confidence=90,
        location_type=LocationType.SUPPORT,
        support=100.0,
        resistance=120.0,
        support_touches=3,
        resistance_touches=1,
    )

    try:
        context.direction_confidence = 10
        mutable = True
    except AttributeError:
        mutable = False

    assert mutable is False