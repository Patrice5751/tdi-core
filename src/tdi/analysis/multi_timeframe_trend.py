from dataclasses import dataclass

from tdi.analysis.trend_analysis import Trend


@dataclass(frozen=True)
class MultiTimeframeTrend:
    h4_trend: Trend
    h1_trend: Trend
    