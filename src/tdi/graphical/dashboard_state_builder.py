from datetime import datetime, timezone

from tdi.analysis.momentum_analysis import Momentum
from tdi.graphical.dashboard_state import DashboardState
from tdi.graphical.location_type import LocationType
from tdi.graphical.market_direction import MarketDirection


class DashboardStateBuilder:
    @staticmethod
    def build(
        symbol,
        decision,
        bias_readiness,
        scenario,
        wait_plan,
        result=None,
        h4_momentum=None,
        h1_momentum=None,
        global_score=None,
        transition=None,
        alert=None,
    ) -> DashboardState:
        waiting_for = tuple(
            condition.value
            for condition in wait_plan.conditions
        )

        transition_value = (
            "Initial"
            if transition is None
            else transition.transition.value
        )

        alert_level = (
            None
            if alert is None
            else alert.level.value
        )

        alert_active = (
            False
            if alert is None
            else alert.active
        )
        global_score_value = (
            0 if global_score is None else global_score.score
        )

        global_grade_value = (
            "E" if global_score is None else global_score.grade
        )

        global_bias_score = (
            0 if global_score is None else global_score.bias_score
        )

        global_structure_score = (
            0 if global_score is None else global_score.structure_score
        )

        global_momentum_score = (
            0 if global_score is None else global_score.momentum_score
        )

        global_location_score = (
            0 if global_score is None else global_score.location_score
        )

        h4_momentum_value = DashboardStateBuilder._momentum_value(
            h4_momentum
        )
        h1_momentum_value = DashboardStateBuilder._momentum_value(
            h1_momentum
        )
        h4_momentum_confidence = getattr(
            h4_momentum,
            "confidence",
            0,
        )
        h1_momentum_confidence = getattr(
            h1_momentum,
            "confidence",
            0,
        )

        opportunity, decisive_condition = (
            DashboardStateBuilder._opportunity(
                decision=decision,
                bias_readiness=bias_readiness,
                h4_momentum=h4_momentum_value,
                h1_momentum=h1_momentum_value,
            )
        )

        decision_trigger = DashboardStateBuilder._decision_trigger(
            decision=decision,
            result=result,
            h4_momentum=h4_momentum,
            h1_momentum=h1_momentum,
        )

        scenario_display = scenario.state.value
        if (
            decision.decision.value in {"Buy", "Sell"}
            and not decision.structure_aligned
        ):
            scenario_display = "Early continuation"

        return DashboardState(
            symbol=symbol,
            decision=decision.decision.value,
            preferred_side=decision.preferred_side,
            target_side=scenario.target_side,
            bias_convergence=bias_readiness.convergence.value,
            bias_readiness=bias_readiness.readiness.value,
            bias_score=bias_readiness.score,
            bias_aligned=decision.bias_aligned,
            structure_aligned=decision.structure_aligned,
            timing_favorable=decision.timing_favorable,
            momentum_confirmed=decision.momentum_confirmed,
            scenario=scenario.state.value,
            scenario_score=scenario.score,
            waiting_for=waiting_for,
            transition=transition_value,
            alert_level=alert_level,
            alert_active=alert_active,
            opportunity=opportunity,
            decisive_condition=decisive_condition,
            decision_trigger=decision_trigger,
            scenario_display=scenario_display,
            h4_momentum=h4_momentum_value,
            h4_momentum_confidence=h4_momentum_confidence,
            h1_momentum=h1_momentum_value,
            h1_momentum_confidence=h1_momentum_confidence,
            global_score=global_score_value,
            global_grade=global_grade_value,
            global_bias_score=global_bias_score,
            global_structure_score=global_structure_score,
            global_momentum_score=global_momentum_score,
            global_location_score=global_location_score,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

    @staticmethod
    def _momentum_value(momentum) -> str:
        value = getattr(momentum, "momentum", None)
        return getattr(value, "value", "Unavailable")

    @staticmethod
    def _opportunity(
        decision,
        bias_readiness,
        h4_momentum: str,
        h1_momentum: str,
    ) -> tuple[str, str | None]:
        side = decision.preferred_side

        if (
            decision.decision.value != "Wait"
            or side not in {"BUY", "SELL"}
            or bias_readiness.readiness.value != "High"
            or not decision.timing_favorable
        ):
            return "None", None

        expected = "Bullish" if side == "BUY" else "Bearish"

        if h4_momentum != expected or h1_momentum != "Neutral":
            return "None", None

        return (
            f"{side} WATCH",
            f"H1 {expected} Momentum Confirmation",
        )

    @staticmethod
    def _decision_trigger(
        decision,
        result,
        h4_momentum,
        h1_momentum,
    ) -> str | None:
        if decision.decision.value in {"Buy", "Sell"}:
            if not decision.structure_aligned:
                return "Strong continuation confirmed"
            return "All entry conditions confirmed"

        if not decision.bias_aligned:
            return "H4/H1 bias alignment lost"

        side = decision.preferred_side
        if (
            hasattr(result, "h4")
            and hasattr(result, "h1")
            and side in {"BUY", "SELL"}
        ):
            opposite = (
                MarketDirection.BEARISH
                if side == "BUY"
                else MarketDirection.BULLISH
            )
            opposed = [
                timeframe
                for timeframe, context in (
                    ("H4", result.h4),
                    ("H1", result.h1),
                )
                if context.direction == opposite
            ]
            if opposed:
                return f"{'/'.join(opposed)} structure opposes {side}"

        if not decision.timing_favorable:
            timing_trigger = DashboardStateBuilder._timing_trigger(
                result=result,
                side=side,
            )
            return timing_trigger or "Entry timing lost"

        if not decision.momentum_confirmed:
            expected = (
                Momentum.BULLISH
                if side == "BUY"
                else Momentum.BEARISH
            )
            mismatched = [
                timeframe
                for timeframe, momentum in (
                    ("H4", h4_momentum),
                    ("H1", h1_momentum),
                )
                if getattr(momentum, "momentum", None) != expected
            ]
            if mismatched:
                return f"Momentum lost on {'/'.join(mismatched)}"
            return "Momentum confirmation lost"

        if (
            not decision.structure_aligned
            and getattr(decision, "confidence", 100) < 85
        ):
            return "Bias confidence below 85"

        if not decision.structure_aligned:
            return "H4/H1 structure not confirmed"

        return getattr(decision, "reason", None)

    @staticmethod
    def _timing_trigger(result, side: str | None) -> str | None:
        if not (
            hasattr(result, "h4")
            and hasattr(result, "h1")
        ):
            return None

        for timeframe, context in (
            ("H4", result.h4),
            ("H1", result.h1),
        ):
            location = context.location_type
            blocked = location in {
                LocationType.EXTENSION,
                LocationType.MIDDLE,
            }
            blocked = blocked or (
                side == "BUY" and location == LocationType.RESISTANCE
            )
            blocked = blocked or (
                side == "SELL" and location == LocationType.SUPPORT
            )
            if blocked:
                return f"{timeframe} timing: {location.value}"

        return None
