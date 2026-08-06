from enum import Enum


class MarketDirection(Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    TRANSITION = "Transition"
    RANGE = "Range"