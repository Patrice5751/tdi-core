from enum import Enum


class LocationType(str, Enum):
    UNKNOWN = "Unknown"
    SUPPORT = "Support"
    RESISTANCE = "Resistance"
    PULLBACK = "Pullback"
    BREAKOUT = "Breakout"
    EXTENSION = "Extension"
    MIDDLE = "Middle"