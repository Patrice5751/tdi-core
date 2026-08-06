from tdi.analysis.structure_analysis import Structure
from tdi.models.trade import Side
from tdi.specifications.structure_valid import (
    StructureValidSpecification,
)


def test_buy_with_bullish_structure_and_valid_entry_zone():
    specification = StructureValidSpecification()

    assert specification.is_satisfied_by(
        structure=Structure.BULLISH,
        side=Side.BUY,
        entry_zone=True,
    )


def test_sell_with_bearish_structure_and_valid_entry_zone():
    specification = StructureValidSpecification()

    assert specification.is_satisfied_by(
        structure=Structure.BEARISH,
        side=Side.SELL,
        entry_zone=True,
    )


def test_wrong_structure_is_rejected():
    specification = StructureValidSpecification()

    assert not specification.is_satisfied_by(
        structure=Structure.BEARISH,
        side=Side.BUY,
        entry_zone=True,
    )


def test_invalid_entry_zone_is_rejected():
    specification = StructureValidSpecification()

    assert not specification.is_satisfied_by(
        structure=Structure.BULLISH,
        side=Side.BUY,
        entry_zone=False,
    )