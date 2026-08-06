from enum import Enum


class DecisionZone(str, Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    ACCEPTABLE = "Acceptable"
    POOR = "Poor"
    FORBIDDEN = "Forbidden"