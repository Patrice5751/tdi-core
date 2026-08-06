from tdi.analysis.analysis_result import AnalysisResult
from tdi.analysis.momentum_analysis import Momentum, MomentumAnalysis
from tdi.analysis.risk_result import RiskResult
from tdi.analysis.structure_analysis import Structure, StructureAnalysis
from tdi.analysis.trend_analysis import Trend, TrendAnalysis
from tdi.engines.validation_engine import ValidationEngine
from tdi.models.trade import Side
from tdi.analysis.validation_result import ValidationResult



def make_analysis(
    trend: Trend = Trend.BEARISH,
    momentum: Momentum = Momentum.BEARISH,
    structure: Structure = Structure.BEARISH,
    entry_zone: bool = True,
) -> AnalysisResult:
    return AnalysisResult(
        trend=TrendAnalysis(
            trend=trend,
            confidence=100,
            reason="Test trend",
        ),
        momentum=MomentumAnalysis(
            momentum=momentum,
            confidence=100,
            reason=["Test momentum"],
        ),
        structure=StructureAnalysis(
            structure=structure,
            confidence=100,
            entry_zone=entry_zone,
            reason=["Test structure"],
        ),
    )


def make_risk(
    rr: float = 2.0,
    valid: bool = True,
) -> RiskResult:
    return RiskResult(
        risk_amount=50.0,
        stop_distance=40.0,
        target_distance=80.0,
        rr=rr,
        position_size=0.0,
        valid=valid,
        reasons=[],
    )


def test_validation_accepts_complete_sell_setup() -> None:
    engine = ValidationEngine()

    result = engine.validate(
        analysis=make_analysis(),
        risk=make_risk(),
        side=Side.SELL,
    )

    assert result.score == 100
    assert result.trend_ok is True
    assert result.momentum_ok is True
    assert result.structure_ok is True
    assert result.rr_ok is True
    assert result.risk_ok is True
    assert result.valid is True


def test_validation_rejects_low_rr() -> None:
    engine = ValidationEngine()

    result = engine.validate(
        analysis=make_analysis(),
        risk=make_risk(rr=1.0, valid=False),
        side=Side.SELL,
    )

    assert result.score == 100
    assert result.rr_ok is False
    assert result.risk_ok is False
    assert result.valid is False


def test_validation_rejects_bad_structure() -> None:
    engine = ValidationEngine()

    analysis = make_analysis(
        structure=Structure.BULLISH,
        entry_zone=False,
    )

    result = engine.validate(
        analysis=analysis,
        risk=make_risk(),
        side=Side.SELL,
    )

    assert result.score == 60
    assert result.structure_ok is False
    assert result.valid is False


def test_validation_rejects_wrong_side_alignment() -> None:
    engine = ValidationEngine()

    analysis = make_analysis(
        trend=Trend.BULLISH,
        momentum=Momentum.BULLISH,
        structure=Structure.BULLISH,
        entry_zone=True,
    )

    result = engine.validate(
        analysis=analysis,
        risk=make_risk(),
        side=Side.SELL,
    )

    assert result.score == 0
    assert result.valid is False

def test_validation_contains_alignment():
    validation = ValidationResult(
        score=90,
        trend_ok=True,
        momentum_ok=True,
        structure_ok=True,
        alignment_ok=True,
        rr_ok=True,
        risk_ok=True,
        atr_ok=False,
        valid=True,
        reasons=[],
    )

    assert validation.alignment_ok is True
