from dataclasses import dataclass

from tdi.adapters.mt5_analysis_pipeline import (
    MT5AnalysisPipeline,
)
from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)


@dataclass(frozen=True)
class MT5MultiTimeframePipeline:
    pipeline: MT5AnalysisPipeline

    def analyze(
        self,
        symbol: str,
        count: int = 250,
    ) -> MT5MultiTimeframeResult:
        h4 = self.pipeline.analyze(
            symbol=symbol,
            timeframe="H4",
            count=count,
        )

        h1 = self.pipeline.analyze(
            symbol=symbol,
            timeframe="H1",
            count=count,
        )

        aligned = (
            h4.direction == h1.direction
        )

        return MT5MultiTimeframeResult(
            h4=h4,
            h1=h1,
            aligned=aligned,
        )
    