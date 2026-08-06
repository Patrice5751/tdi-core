from dataclasses import dataclass

from tdi.analysis.momentum_analysis import MomentumAnalysis
from tdi.analysis.structure_analysis import StructureAnalysis
from tdi.analysis.trend_analysis import TrendAnalysis
from tdi.analysis.multi_timeframe_trend import MultiTimeframeTrend


@dataclass(frozen=True)
class AnalysisResult:
    trend: TrendAnalysis
    momentum: MomentumAnalysis
    structure: StructureAnalysis
from dataclasses import dataclass

from tdi.analysis.momentum_analysis import MomentumAnalysis
from tdi.analysis.multi_timeframe_trend import MultiTimeframeTrend
from tdi.analysis.structure_analysis import StructureAnalysis
from tdi.analysis.trend_analysis import TrendAnalysis


@dataclass(frozen=True)
class AnalysisResult:
    trend: TrendAnalysis
    momentum: MomentumAnalysis
    structure: StructureAnalysis
    multi_timeframe: MultiTimeframeTrend | None = None