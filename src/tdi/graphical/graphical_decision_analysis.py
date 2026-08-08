from dataclasses import dataclass

from tdi.graphical.graphical_decision import GraphicalDecision


@dataclass(frozen=True)
class GraphicalDecisionAnalysis:
    decision: GraphicalDecision
    confidence: int
    reason: str
    