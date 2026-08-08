from dataclasses import dataclass

from tdi.graphical.graphical_context import GraphicalContext


@dataclass(frozen=True)
class MT5MultiTimeframeResult:
    h4: GraphicalContext
    h1: GraphicalContext
    aligned: bool
    