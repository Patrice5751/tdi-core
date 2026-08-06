from tdi.advisor.atr_rule import ATRRule


def test_valid_atr():
    result = ATRRule.evaluate(True)

    assert result.passed
    assert result.score == 10
    assert "volatilité" in result.message.lower()


def test_invalid_atr():
    result = ATRRule.evaluate(False)

    assert not result.passed
    assert result.score == 0
    assert "repositionner" in result.message.lower()