from types import SimpleNamespace

from tdi.analysis.recommendation import Recommendation
from tdi.engines.trade_decision_pipeline import TradeDecisionPipeline
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection
from tdi.models.trade import Side


def make_analysis(
    trend_confidence: int = 90,
):
    return SimpleNamespace(
        trend=SimpleNamespace(
            confidence=trend_confidence,
        )
    )


def make_validation(
    score: int = 90,
    valid: bool = True,
):
    return SimpleNamespace(
        score=score,
        valid=valid,
        trend_ok=True,
        momentum_ok=True,
        structure_ok=True,
        rr_ok=True,
    )


def make_risk(
    rr: float = 2.0,
):
    return SimpleNamespace(
        rr=rr,
    )


def make_context(
    direction: MarketDirection,
    location_type: LocationType,
    confidence: int = 90,
):
    return GraphicalContext(
        direction=direction,
        direction_confidence=confidence,
        location_type=location_type,
        support=100.0,
        resistance=120.0,
        support_touches=3,
        resistance_touches=2,
    )


def test_pipeline_buy_go():
    result = TradeDecisionPipeline().decide(
        analysis=make_analysis(),
        validation=make_validation(),
        risk=make_risk(),
        graphical_context=make_context(
            direction=MarketDirection.BULLISH,
            location_type=LocationType.PULLBACK,
        ),
        side=Side.BUY,
    )

    assert result.accepted is True
    assert result.recommendation != Recommendation.WAIT
    assert result.recommendation != Recommendation.REJECT


def test_pipeline_wait_on_extension():
    result = TradeDecisionPipeline().decide(
        analysis=make_analysis(),
        validation=make_validation(
            score=95,
            valid=True,
        ),
        risk=make_risk(rr=3.0),
        graphical_context=make_context(
            direction=MarketDirection.BULLISH,
            location_type=LocationType.EXTENSION,
        ),
        side=Side.BUY,
    )

    assert result.accepted is False
    assert result.recommendation == Recommendation.WAIT


def test_pipeline_rejects_wrong_direction():
    result = TradeDecisionPipeline().decide(
        analysis=make_analysis(),
        validation=make_validation(
            score=95,
            valid=True,
        ),
        risk=make_risk(rr=3.0),
        graphical_context=make_context(
            direction=MarketDirection.BEARISH,
            location_type=LocationType.PULLBACK,
        ),
        side=Side.BUY,
    )

    assert result.accepted is False
    assert result.recommendation == Recommendation.REJECT


def test_pipeline_sell_go_on_resistance():
    result = TradeDecisionPipeline().decide(
        analysis=make_analysis(),
        validation=make_validation(),
        risk=make_risk(),
        graphical_context=make_context(
            direction=MarketDirection.BEARISH,
            location_type=LocationType.RESISTANCE,
        ),
        side=Side.SELL,
    )

    assert result.accepted is True
    