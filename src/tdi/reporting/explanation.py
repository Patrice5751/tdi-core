from dataclasses import dataclass


@dataclass(frozen=True)
class Explanation:
    title: str
    value: int
    message: str
    