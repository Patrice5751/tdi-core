from dataclasses import dataclass

from tdi.analysis.momentum_analysis import MomentumAnalysis
from tdi.analysis.structure_analysis import StructureAnalysis
from tdi.analysis.trend_analysis import TrendAnalysis


@dataclass(frozen=True)
class AnalysisResult:
    trend: TrendAnalysis
    momentum: MomentumAnalysis
    structure: StructureAnalysis