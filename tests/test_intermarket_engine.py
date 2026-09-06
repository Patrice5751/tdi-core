from tdi.analysis.trend_analysis import Trend, TrendAnalysis
from tdi.engines.intermarket_engine import IntermarketEngine


def make_trend(trend: Trend, confidence: int = 80) -> TrendAnalysis:
    return TrendAnalysis(
        trend=trend,
        confidence=confidence,
        reason="test",
    )


def test_intermarket_confirms_bullish_alignment():
    result = IntermarketEngine().analyze(
        primary=make_trend(Trend.BULLISH),
        confirmation=make_trend(Trend.BULLISH),
    )

    assert result.state.value == "Confirmed"
    assert result.score == 100


def test_intermarket_confirms_bearish_alignment():
    result = IntermarketEngine().analyze(
        primary=make_trend(Trend.BEARISH),
        confirmation=make_trend(Trend.BEARISH),
    )

    assert result.state.value == "Confirmed"
    assert result.score == 100


def test_intermarket_detects_divergence():
    result = IntermarketEngine().analyze(
        primary=make_trend(Trend.BULLISH),
        confirmation=make_trend(Trend.BEARISH),
    )

    assert result.state.value == "Divergent"
    assert result.score == 0


def test_intermarket_is_mixed_when_confirmation_is_neutral():
    result = IntermarketEngine().analyze(
        primary=make_trend(Trend.BULLISH),
        confirmation=make_trend(Trend.NEUTRAL),
    )

    assert result.state.value == "Mixed"
    assert result.score == 50

def test_intermarket_is_mixed_when_primary_is_neutral():
    result = IntermarketEngine().analyze(
        primary=make_trend(Trend.NEUTRAL),
        confirmation=make_trend(Trend.BULLISH),
    )

    assert result.state.value == "Mixed"
    assert result.score == 50


def test_intermarket_is_mixed_when_both_are_neutral():
    result = IntermarketEngine().analyze(
        primary=make_trend(Trend.NEUTRAL),
        confirmation=make_trend(Trend.NEUTRAL),
    )

    assert result.state.value == "Mixed"
    assert result.score == 50


def test_intermarket_detects_reverse_divergence():
    result = IntermarketEngine().analyze(
        primary=make_trend(Trend.BEARISH),
        confirmation=make_trend(Trend.BULLISH),
    )

    assert result.state.value == "Divergent"
    assert result.score == 0