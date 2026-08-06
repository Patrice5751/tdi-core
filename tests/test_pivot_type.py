from tdi.graphical.pivot_type import PivotType


def test_high_enum():

    assert PivotType.HIGH.value == "High"


def test_low_enum():

    assert PivotType.LOW.value == "Low"
    