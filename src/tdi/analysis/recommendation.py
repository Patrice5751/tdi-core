from enum import Enum


class Recommendation(Enum):
    EXCELLENT = "TRADE EXCELLENT"
    TAKE = "PRENDRE LE TRADE"
    ACCEPTABLE = "TRADE ACCEPTABLE"
    WAIT = "ATTENDRE"
    REJECT = "REFUSER"