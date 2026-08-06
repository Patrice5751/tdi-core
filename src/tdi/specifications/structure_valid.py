from tdi.analysis.structure_analysis import Structure
from tdi.models.trade import Side


class StructureValidSpecification:
    """Checks whether structure and entry zone match the trade direction."""

    def is_satisfied_by(
        self,
        structure: Structure,
        side: Side,
        entry_zone: bool,
    ) -> bool:
        expected_structure = (
            Structure.BULLISH
            if side == Side.BUY
            else Structure.BEARISH
        )

        return structure == expected_structure and entry_zone