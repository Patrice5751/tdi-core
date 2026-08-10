from enum import Enum


class WaitCondition(str, Enum):
    H4_PULLBACK = "H4 Pullback"
    H1_PULLBACK = "H1 Pullback"

    H4_SUPPORT = "H4 Support"
    H1_SUPPORT = "H1 Support"

    H4_RESISTANCE = "H4 Resistance"
    H1_RESISTANCE = "H1 Resistance"

    H4_STRUCTURE = "H4 Structure Confirmation"
    H1_STRUCTURE = "H1 Structure Confirmation"

    MOMENTUM = "Momentum Confirmation"

    BREAKOUT = "Breakout Confirmation"