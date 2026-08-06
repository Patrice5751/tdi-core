from dataclasses import dataclass


@dataclass(frozen=True)
class UserSettings:
    capital: float
    risk_percent: float