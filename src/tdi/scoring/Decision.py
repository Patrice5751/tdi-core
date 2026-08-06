from enum import Enum


class Decision(Enum):
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    BUY_WITH_CAUTION = "Buy with Caution"
    WAIT = "Wait"
    REJECT = "Reject"