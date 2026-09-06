from tdi.analysis.trend_analysis import Trend
from tdi.graphical.market_direction import MarketDirection


class IntermarketDirectionAdapter:

    @staticmethod
    def to_trend(direction: MarketDirection) -> Trend:
        if direction == MarketDirection.BULLISH:
            return Trend.BULLISH

        if direction == MarketDirection.BEARISH:
            return Trend.BEARISH

        return Trend.NEUTRAL