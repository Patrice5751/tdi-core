from tdi.adapters.mt5_multi_timeframe_result import (
    MT5MultiTimeframeResult,
)
from tdi.analysis.momentum_analysis import (
    Momentum,
    MomentumAnalysis,
)
from tdi.graphical.bias_readiness import (
    BiasConvergence,
    BiasReadiness,
)
from tdi.graphical.bias_readiness_engine import (
    BiasReadinessEngine,
)
from tdi.graphical.graphical_context import GraphicalContext
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection


def make_context(
    ma_bullish=False,
    ma_bearish=False,
):
    return GraphicalContext(
        direction=MarketDirection.TRANSITION,
        direction_confidence=50,
        location_type=LocationType.MIDDLE,
        support=None,
        resistance=None,
        support_touches=0,
        resistance_touches=0,
        ma_confirmation_score=100,
        ma_bullish=ma_bullish,
        ma_bearish=ma_bearish,
    )


def make_momentum(
    momentum,
    confidence=100,
):
    return MomentumAnalysis(
        momentum=momentum,
        confidence=confidence,
        reason=[],
    )


def test_neutral_h1_bullish_momentum_converges_toward_buy():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            ma_bullish=True,
        ),
        h1=make_context(),
        aligned=False,
    )

    analysis = BiasReadinessEngine().analyze(
        result=result,
        h1_momentum=make_momentum(
            Momentum.BULLISH
        ),
    )

    assert analysis.target_side == "BUY"
    assert analysis.readiness == BiasReadiness.MEDIUM
    assert analysis.convergence == BiasConvergence.TOWARD
    assert analysis.score > 50


def test_neutral_h1_bearish_momentum_moves_away_from_buy():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            ma_bullish=True,
        ),
        h1=make_context(),
        aligned=False,
    )

    analysis = BiasReadinessEngine().analyze(
        result=result,
        h1_momentum=make_momentum(
            Momentum.BEARISH
        ),
    )

    assert analysis.target_side == "BUY"
    assert analysis.readiness == BiasReadiness.LOW
    assert analysis.convergence == BiasConvergence.AWAY


def test_aligned_buy_bias_is_high_readiness():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            ma_bullish=True,
        ),
        h1=make_context(
            ma_bullish=True,
        ),
        aligned=False,
    )

    analysis = BiasReadinessEngine().analyze(
        result=result,
        h1_momentum=make_momentum(
            Momentum.BULLISH
        ),
    )

    assert analysis.target_side == "BUY"
    assert analysis.readiness == BiasReadiness.HIGH
    assert analysis.convergence == BiasConvergence.ALIGNED
    assert analysis.score == 100


def test_opposite_h1_bias_moves_away():
    result = MT5MultiTimeframeResult(
        h4=make_context(
            ma_bullish=True,
        ),
        h1=make_context(
            ma_bearish=True,
        ),
        aligned=False,
    )

    analysis = BiasReadinessEngine().analyze(
        result=result,
        h1_momentum=make_momentum(
            Momentum.BEARISH
        ),
    )

    assert analysis.readiness == BiasReadiness.LOW
    assert analysis.convergence == BiasConvergence.AWAY
    assert analysis.score == 0
    