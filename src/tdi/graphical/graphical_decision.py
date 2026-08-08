from enum import Enum


class GraphicalDecision(str, Enum):
    GO = "Go"
    WAIT = "Wait"
    NO_GO = "NoGo"
    