from dataclasses import dataclass

from tdi.analysis.analysis_result import AnalysisResult
from tdi.analysis.decision_result import DecisionResult
from tdi.analysis.risk_result import RiskResult
from tdi.analysis.validation_result import ValidationResult
from tdi.engines.decision_engine import DecisionEngine
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.graphical_decision_engine import (
    GraphicalDecisionEngine,
)
from tdi.models.trade import Side


@dataclass(frozen=True)
class TradeDecisionPipeline:
    def decide(
        self,
        analysis: AnalysisResult,
        validation: ValidationResult,
        risk: RiskResult,
        graphical_context: GraphicalContext,
        side: Side,
    ) -> DecisionResult:
        graphical_decision = GraphicalDecisionEngine().decide(
            context=graphical_context,
            side=side,
        )

        return DecisionEngine().decide(
            analysis=analysis,
            validation=validation,
            risk=risk,
            graphical_decision=graphical_decision,
        )
    