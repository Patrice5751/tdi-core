from tdi.graphical.decision_zone import DecisionZone
from tdi.graphical.location_type import LocationType
from tdi.graphical.price_location_analysis import (
    PriceLocationAnalysis,
)
from tdi.graphical.price_location_input import (
    PriceLocationInput,
)


class PriceLocationEngine:

    def analyze(
        self,
        data: PriceLocationInput,
    ) -> PriceLocationAnalysis:

        distance_ma20 = abs(data.current_price - data.ma20) / data.atr

        distance_support = (
            abs(data.current_price - data.nearest_support)
            / data.atr
        )

        distance_resistance = (
            abs(data.current_price - data.nearest_resistance)
            / data.atr
        )

        extension = distance_ma20

        score = 100

        score -= self._ma_penalty(distance_ma20)

        score -= self._extension_penalty(extension)

        score = max(score, 0)

        location = self._location_type(
            data=data,
            support=distance_support,
            resistance=distance_resistance,
            ma20=distance_ma20,
        )
    

        if location == LocationType.BREAKOUT:
            zone = DecisionZone.GOOD
        else:
            zone = self._decision_zone(
                score=score,
                extension=extension,
            )

        return PriceLocationAnalysis(
            location_type=location,
            decision_zone=zone,
            quality_score=score,
            extension_atr=extension,
            distance_ma20=distance_ma20,
            distance_support=distance_support,
            distance_resistance=distance_resistance,
            reason="Initial Price Location evaluation.",
        )

    def _ma_penalty(self, distance: float) -> int:

        if distance < 0.5:
            return 0

        if distance < 1:
            return 10

        if distance < 2:
            return 20

        return 30

    def _extension_penalty(self, extension: float) -> int:

        if extension < 1:
            return 0

        if extension < 2:
            return 5

        if extension < 3:
            return 10

        return 20

    def _location_type(
        self,
        data: PriceLocationInput,
        support: float,
        resistance: float,
        ma20: float,
    ) -> LocationType:
        if data.breakout_level is not None:
            breakout_distance = (
                abs(data.current_price - data.breakout_level)
                / data.atr
            )

            if breakout_distance <= 0.5:
                return LocationType.BREAKOUT

        if ma20 < 0.5:
            return LocationType.PULLBACK

        if support < 0.5:
            return LocationType.SUPPORT

        if resistance < 0.5:
            return LocationType.RESISTANCE

        if ma20 > 2:
            return LocationType.EXTENSION

        return LocationType.MIDDLE

    def _decision_zone(
        self,
        score: int,
        extension: float,
    ) -> DecisionZone:
        if extension >= 3:
            return DecisionZone.FORBIDDEN

        if extension >= 2:
            return DecisionZone.POOR

        if score >= 90:
            return DecisionZone.EXCELLENT

        if score >= 75:
            return DecisionZone.GOOD

        if score >= 60:
            return DecisionZone.ACCEPTABLE

        if score >= 40:
            return DecisionZone.POOR

        return DecisionZone.FORBIDDEN

        return DecisionZone.FORBIDDEN
            
    