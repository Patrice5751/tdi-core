from dataclasses import dataclass

from tdi.graphical.swing_type import SwingType


@dataclass(frozen=True)
class SwingPoint:

    index: int

    price: float

    swing_type: SwingType