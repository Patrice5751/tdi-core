from enum import Enum

from tdi.reporting.trade_grade import TradeGrade


class TradeAssessment(Enum):
    EXCELLENT = "EXCELLENT"
    VERY_GOOD = "VERY GOOD"
    GOOD = "GOOD"
    AVERAGE = "AVERAGE"
    POOR = "POOR"

    @staticmethod
    def from_grade(grade: TradeGrade):
        value = grade.value

        if value >= 9.0:
            return TradeAssessment.EXCELLENT

        if value >= 8.0:
            return TradeAssessment.VERY_GOOD

        if value >= 7.0:
            return TradeAssessment.GOOD

        if value >= 6.0:
            return TradeAssessment.AVERAGE

        return TradeAssessment.POOR