from tdi.graphical.pivot import Pivot
from tdi.graphical.pivot_type import PivotType
from tdi.graphical.support_resistance_engine import (
    SupportResistanceEngine,
)


def test_empty_pivots_returns_no_levels():
    result = SupportResistanceEngine().analyze(
        pivots=[],
        current_price=100,
    )

    assert result.support is None
    assert result.resistance is None
    assert result.support_touches == 0
    assert result.resistance_touches == 0


def test_nearest_low_below_price_is_support():
    pivots = [
        Pivot(2, 80, PivotType.LOW),
        Pivot(5, 90, PivotType.LOW),
        Pivot(8, 95, PivotType.LOW),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.support == 95


def test_nearest_high_above_price_is_resistance():
    pivots = [
        Pivot(2, 130, PivotType.HIGH),
        Pivot(5, 110, PivotType.HIGH),
        Pivot(8, 120, PivotType.HIGH),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.resistance == 110


def test_low_above_current_price_is_not_support():
    pivots = [
        Pivot(2, 105, PivotType.LOW),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.support is None


def test_high_below_current_price_is_not_resistance():
    pivots = [
        Pivot(2, 95, PivotType.HIGH),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.resistance is None


def test_equal_support_levels_count_touches():
    pivots = [
        Pivot(2, 90, PivotType.LOW),
        Pivot(6, 90, PivotType.LOW),
        Pivot(10, 80, PivotType.LOW),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.support == 90
    assert result.support_touches == 2


def test_equal_resistance_levels_count_touches():
    pivots = [
        Pivot(2, 110, PivotType.HIGH),
        Pivot(6, 110, PivotType.HIGH),
        Pivot(10, 120, PivotType.HIGH),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.resistance == 110
    assert result.resistance_touches == 2


def test_support_and_resistance_are_found_together():
    pivots = [
        Pivot(2, 90, PivotType.LOW),
        Pivot(4, 115, PivotType.HIGH),
        Pivot(6, 95, PivotType.LOW),
        Pivot(8, 110, PivotType.HIGH),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.support == 95
    assert result.resistance == 110

def test_supports_inside_atr_tolerance_count_as_touches():
    pivots = [
        Pivot(2, 90.0, PivotType.LOW),
        Pivot(6, 91.0, PivotType.LOW),
        Pivot(10, 90.5, PivotType.LOW),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
        atr=4.0,
    )

    assert result.support == 91.0
    assert result.support_touches == 3


def test_support_outside_atr_tolerance_is_not_touch():
    pivots = [
        Pivot(2, 90.0, PivotType.LOW),
        Pivot(6, 91.0, PivotType.LOW),
        Pivot(10, 89.9, PivotType.LOW),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
        atr=4.0,
    )

    assert result.support == 91.0
    assert result.support_touches == 2


def test_resistances_inside_atr_tolerance_count_as_touches():
    pivots = [
        Pivot(2, 110.0, PivotType.HIGH),
        Pivot(6, 109.5, PivotType.HIGH),
        Pivot(10, 109.0, PivotType.HIGH),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
        atr=4.0,
    )

    assert result.resistance == 109.0
    assert result.resistance_touches == 3


def test_without_atr_keeps_exact_level_behaviour():
    pivots = [
        Pivot(2, 90.0, PivotType.LOW),
        Pivot(6, 90.1, PivotType.LOW),
        Pivot(10, 90.1, PivotType.LOW),
    ]

    result = SupportResistanceEngine().analyze(
        pivots=pivots,
        current_price=100,
    )

    assert result.support == 90.1
    assert result.support_touches == 2
