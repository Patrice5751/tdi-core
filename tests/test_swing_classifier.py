from tdi.graphical.pivot import Pivot
from tdi.graphical.pivot_type import PivotType
from tdi.graphical.swing_classifier import SwingClassifier
from tdi.graphical.swing_type import SwingType


def test_empty_pivots_returns_empty():
    result = SwingClassifier().classify([])

    assert result == []


def test_first_high_cannot_be_classified():
    pivots = [
        Pivot(
            index=2,
            price=100,
            pivot_type=PivotType.HIGH,
        )
    ]

    result = SwingClassifier().classify(pivots)

    assert result == []


def test_higher_high_returns_hh():
    pivots = [
        Pivot(2, 100, PivotType.HIGH),
        Pivot(6, 110, PivotType.HIGH),
    ]

    result = SwingClassifier().classify(pivots)

    assert len(result) == 1
    assert result[0].index == 6
    assert result[0].price == 110
    assert result[0].swing_type == SwingType.HH


def test_lower_high_returns_lh():
    pivots = [
        Pivot(2, 110, PivotType.HIGH),
        Pivot(6, 100, PivotType.HIGH),
    ]

    result = SwingClassifier().classify(pivots)

    assert len(result) == 1
    assert result[0].swing_type == SwingType.LH


def test_higher_low_returns_hl():
    pivots = [
        Pivot(3, 90, PivotType.LOW),
        Pivot(7, 95, PivotType.LOW),
    ]

    result = SwingClassifier().classify(pivots)

    assert len(result) == 1
    assert result[0].swing_type == SwingType.HL


def test_lower_low_returns_ll():
    pivots = [
        Pivot(3, 90, PivotType.LOW),
        Pivot(7, 80, PivotType.LOW),
    ]

    result = SwingClassifier().classify(pivots)

    assert len(result) == 1
    assert result[0].swing_type == SwingType.LL


def test_mixed_structure_is_classified_chronologically():
    pivots = [
        Pivot(2, 100, PivotType.HIGH),
        Pivot(3, 90, PivotType.LOW),
        Pivot(6, 110, PivotType.HIGH),
        Pivot(7, 95, PivotType.LOW),
        Pivot(10, 105, PivotType.HIGH),
        Pivot(11, 85, PivotType.LOW),
    ]

    result = SwingClassifier().classify(pivots)

    assert [swing.index for swing in result] == [
        6,
        7,
        10,
        11,
    ]

    assert [swing.swing_type for swing in result] == [
        SwingType.HH,
        SwingType.HL,
        SwingType.LH,
        SwingType.LL,
    ]
    