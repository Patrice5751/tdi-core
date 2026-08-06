from enum import Enum


class SetupQuality(Enum):
    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    @staticmethod
    def from_score(score: int):
        if score >= 90:
            return SetupQuality.A_PLUS

        if score >= 80:
            return SetupQuality.A

        if score >= 70:
            return SetupQuality.B

        if score >= 60:
            return SetupQuality.C

        return SetupQuality.D