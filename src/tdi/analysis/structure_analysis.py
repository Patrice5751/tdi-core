from dataclasses import dataclass
from enum import Enum


class Structure(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


@dataclass(frozen=True)
class StructureAnalysis:
    structure: Structure
    confidence: int
    entry_zone: bool
    reason: list[str]