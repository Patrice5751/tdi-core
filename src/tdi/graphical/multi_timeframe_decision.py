from enum import Enum


class MultiTimeframeDecision(str, Enum):
    BUY = "Buy"
    SELL = "Sell"
    WAIT = "Wait"
    NO_GO = "NoGo"
    