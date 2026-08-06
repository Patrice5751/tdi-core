from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Candle:

    index: int

    timestamp: datetime

    open: float

    high: float

    low: float

    close: float

    from dataclasses import dataclass
from datetime import datetime


