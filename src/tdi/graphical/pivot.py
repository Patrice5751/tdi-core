
from dataclasses import dataclass

from tdi.graphical.pivot_type import PivotType


@dataclass(frozen=True)

class Pivot:

    index: int

    price: float

    pivot_type: PivotType

from dataclasses import dataclass

from tdi.graphical.pivot_type import PivotType


