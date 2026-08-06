from tdi.reporting.trade_assessment import TradeAssessment
from tdi.reporting.trade_grade import TradeGrade


def test_trade_assessment_from_grade():
    assert (
        TradeAssessment.from_grade(
            TradeGrade(9.5)
        )
        is TradeAssessment.EXCELLENT
    )

    assert (
        TradeAssessment.from_grade(
            TradeGrade(8.4)
        )
        is TradeAssessment.VERY_GOOD
    )

    assert (
        TradeAssessment.from_grade(
            TradeGrade(7.3)
        )
        is TradeAssessment.GOOD
    )

    assert (
        TradeAssessment.from_grade(
            TradeGrade(6.2)
        )
        is TradeAssessment.AVERAGE
    )

    assert (
        TradeAssessment.from_grade(
            TradeGrade(5.4)
        )
        is TradeAssessment.POOR
    )