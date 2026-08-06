from tdi.graphical.pivot import Pivot
from tdi.graphical.pivot_type import PivotType


def test_create_high_pivot():

    pivot = Pivot(
        index=10,
        price=4275,
        pivot_type=PivotType.HIGH,
    )

    assert pivot.index == 10

    assert pivot.price == 4275

    assert pivot.pivot_type == PivotType.HIGH


def test_create_low_pivot():

    pivot = Pivot(
        index=22,
        price=4198,
        pivot_type=PivotType.LOW,
    )

    assert pivot.pivot_type == PivotType.LOW