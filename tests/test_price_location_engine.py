from tdi.graphical.decision_zone import DecisionZone
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection
from tdi.graphical.price_location_engine import PriceLocationEngine
from tdi.graphical.price_location_input import PriceLocationInput


def make_input(
    *,
    current_price: float = 100.0,
    market_direction: MarketDirection = MarketDirection.BULLISH,
    ma20: float = 100.0,
    atr: float = 10.0,
    nearest_support: float = 95.0,
    nearest_resistance: float = 110.0,
    breakout_level: float | None = None,
) -> PriceLocationInput:
    return PriceLocationInput(
        current_price=current_price,
        market_direction=market_direction,
        ma20=ma20,
        atr=atr,
        nearest_support=nearest_support,
        nearest_resistance=nearest_resistance,
        breakout_level=breakout_level,
    )


def test_pullback_bullish_returns_excellent():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=100.0,
            ma20=98.0,
            atr=10.0,
        )
    )

    assert result.location_type == LocationType.PULLBACK
    assert result.decision_zone == DecisionZone.EXCELLENT


def test_pullback_bearish_returns_excellent():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=100.0,
            market_direction=MarketDirection.BEARISH,
            ma20=102.0,
            atr=10.0,
        )
    )

    assert result.location_type == LocationType.PULLBACK
    assert result.decision_zone == DecisionZone.EXCELLENT


def test_price_near_support_returns_support():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=100.0,
            ma20=110.0,
            atr=10.0,
            nearest_support=98.0,
            nearest_resistance=120.0,
        )
    )

    assert result.location_type == LocationType.SUPPORT


def test_price_near_resistance_returns_resistance():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=100.0,
            ma20=110.0,
            atr=10.0,
            nearest_support=80.0,
            nearest_resistance=102.0,
        )
    )

    assert result.location_type == LocationType.RESISTANCE


def test_price_in_middle_returns_middle():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=100.0,
            ma20=90.0,
            atr=10.0,
            nearest_support=80.0,
            nearest_resistance=120.0,
        )
    )

    assert result.location_type == LocationType.MIDDLE


def test_extension_above_two_atr_returns_extension_and_poor():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=125.0,
            ma20=100.0,
            atr=10.0,
            nearest_support=90.0,
            nearest_resistance=140.0,
        )
    )

    assert result.location_type == LocationType.EXTENSION
    assert result.decision_zone == DecisionZone.POOR


def test_extension_above_three_atr_returns_forbidden():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=135.0,
            ma20=100.0,
            atr=10.0,
            nearest_support=90.0,
            nearest_resistance=150.0,
        )
    )

    assert result.decision_zone == DecisionZone.FORBIDDEN


def test_recent_breakout_returns_good():
    result = PriceLocationEngine().analyze(
        make_input(
            current_price=102.0,
            ma20=95.0,
            atr=10.0,
            nearest_support=90.0,
            nearest_resistance=120.0,
            breakout_level=100.0,
        )
    )

    assert result.decision_zone == DecisionZone.GOOD
    assert result.location_type == LocationType.BREAKOUT
    

def test_quality_score_is_between_zero_and_one_hundred():
    result = PriceLocationEngine().analyze(make_input())

    assert 0 <= result.quality_score <= 100


def test_location_type_is_valid_enum():
    result = PriceLocationEngine().analyze(make_input())

    assert isinstance(result.location_type, LocationType)