from tdi.graphical.ma_confirmation_engine import (
    MAConfirmationEngine,
)


def test_bullish_ma_structure():
    result = MAConfirmationEngine().analyze(
        current_price=120,
        ma20=115,
        ma50=110,
        ma200=100,
    )

    assert result.bullish is True
    assert result.bearish is False
    assert result.score == 100


def test_bearish_ma_structure():
    result = MAConfirmationEngine().analyze(
        current_price=80,
        ma20=85,
        ma50=90,
        ma200=100,
    )

    assert result.bearish is True
    assert result.bullish is False
    assert result.score == 100


def test_mixed_ma_structure_is_neutral():
    result = MAConfirmationEngine().analyze(
        current_price=105,
        ma20=100,
        ma50=110,
        ma200=90,
    )

    assert result.bullish is False
    assert result.bearish is False


def test_missing_ma_returns_zero_score():
    result = MAConfirmationEngine().analyze(
        current_price=100,
        ma20=95,
        ma50=None,
        ma200=90,
    )

    assert result.score == 0
    assert result.bullish is False
    assert result.bearish is False


def test_partial_bullish_structure_scores_below_full_confirmation():
    result = MAConfirmationEngine().analyze(
        current_price=120,
        ma20=115,
        ma50=105,
        ma200=110,
    )

    assert result.score < 100
    