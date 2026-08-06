from tdi.reporting.trade_grade import TradeGrade


def test_trade_grade_from_score():
    assert TradeGrade.from_score(95).value == 9.5
    assert TradeGrade.from_score(88).value == 8.8
    assert TradeGrade.from_score(76).value == 7.6
    assert TradeGrade.from_score(61).value == 6.1
    assert TradeGrade.from_score(43).value == 4.3