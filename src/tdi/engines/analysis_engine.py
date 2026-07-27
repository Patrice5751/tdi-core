from tdi.analysis.analysis_result import AnalysisResult
from tdi.engines.momentum_engine import MomentumEngine
from tdi.engines.structure_engine import StructureEngine
from tdi.engines.trend_engine import TrendEngine
from tdi.models.market_snapshot import MarketSnapshot
from tdi.models.price_structure import PriceStructure
from tdi.models.trade import Side


class AnalysisEngine:
    """Orchestre les différents moteurs d'analyse."""

    def __init__(self) -> None:
        self.trend_engine = TrendEngine()
        self.momentum_engine = MomentumEngine()
        self.structure_engine = StructureEngine()

    def analyze(
        self,
        snapshot: MarketSnapshot,
        price_structure: PriceStructure,
        side: Side,
    ) -> AnalysisResult:
        """
        Lance les analyses de tendance, de momentum et de structure,
        puis retourne un AnalysisResult complet.
        """

        trend = self.trend_engine.analyze(snapshot)
        momentum = self.momentum_engine.analyze(snapshot)
        structure = self.structure_engine.analyze(
            structure=price_structure,
            side=side,
        )

        return AnalysisResult(
            trend=trend,
            momentum=momentum,
            structure=structure,
        )