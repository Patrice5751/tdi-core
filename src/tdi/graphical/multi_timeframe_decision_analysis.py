from dataclasses import dataclass

from tdi.graphical.multi_timeframe_decision import (
    MultiTimeframeDecision,
)


@dataclass(frozen=True)
class MultiTimeframeDecisionAnalysis:
    decision: MultiTimeframeDecision
    preferred_side: str | None

    bias_aligned: bool
    structure_aligned: bool
    timing_favorable: bool

    confidence: int

    reason: str
    