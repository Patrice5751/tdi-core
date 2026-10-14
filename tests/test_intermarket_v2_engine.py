import pytest

from tdi.analysis.trend_analysis import Trend
from tdi.engines.intermarket_v2_engine import IntermarketV2Engine


BULL = Trend.BULLISH
BEAR = Trend.BEARISH
NEUTRAL = Trend.NEUTRAL


@pytest.mark.parametrize(
    "primary,silver,dollar,score,state,coverage",
    [
        (BULL, BULL, BEAR, 100, "Confirmed", 100),
        (BEAR, BEAR, BULL, 100, "Confirmed", 100),
        (BULL, BEAR, BULL, 0, "Divergent", 100),
        (BEAR, BULL, BEAR, 0, "Divergent", 100),
        (BULL, BULL, BULL, 60, "Mixed", 100),
        (BULL, BEAR, BEAR, 40, "Mixed", 100),
        (BULL, NEUTRAL, BEAR, 70, "Mixed", 100),
        (BULL, BULL, NEUTRAL, 80, "Mixed", 100),
        (BULL, NEUTRAL, NEUTRAL, 50, "Mixed", 100),
        (BULL, BULL, None, 100, "Confirmed", 60),
        (BULL, None, BEAR, 100, "Confirmed", 40),
        (BULL, BEAR, None, 0, "Divergent", 60),
        (BULL, None, BULL, 0, "Divergent", 40),
        (BULL, NEUTRAL, None, 50, "Mixed", 60),
        (BULL, None, None, None, "Unavailable", 0),
        (NEUTRAL, BULL, BEAR, None, "Unavailable", 100),
    ],
)
def test_intermarket_v2(
    primary, silver, dollar, score, state, coverage
):
    result = IntermarketV2Engine().analyze(
        primary=primary,
        silver=silver,
        dollar=dollar,
    )

    assert result.score == score
    assert result.state.value == state
    assert result.coverage == coverage
    assert result.primary_trend == primary
    assert result.silver_trend == silver
    assert result.dollar_trend == dollar


def test_missing_dollar_is_distinct_from_neutral_dollar():
    engine = IntermarketV2Engine()

    missing = engine.analyze(BULL, BULL, None)
    neutral = engine.analyze(BULL, BULL, NEUTRAL)

    assert missing.dollar_score is None
    assert missing.coverage == 60
    assert neutral.dollar_score == 50
    assert neutral.coverage == 100


def test_neutral_primary_has_no_component_scores():
    result = IntermarketV2Engine().analyze(
        NEUTRAL, BULL, BEAR
    )

    assert result.silver_score is None
    assert result.dollar_score is None
    assert result.score is None