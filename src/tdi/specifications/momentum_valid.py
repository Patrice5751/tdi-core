from tdi.analysis.momentum_analysis import Momentum
from tdi.models.trade import Side


class MomentumValidSpecification:
    """Checks whether momentum matches the trade direction."""

    def is_satisfied_by(
        self,
        momentum: Momentum,
        side: Side,
    ) -> bool:
        expected_momentum = (
            Momentum.BULLISH
            if side == Side.BUY
            else Momentum.BEARISH
        )

        return momentum == expected_momentum