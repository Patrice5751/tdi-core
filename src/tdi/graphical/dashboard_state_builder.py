from datetime import datetime, timezone

from tdi.graphical.dashboard_state import DashboardState


class DashboardStateBuilder:
    @staticmethod
    def build(
        symbol,
        decision,
        bias_readiness,
        scenario,
        wait_plan,
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
            updated_at=datetime.now(timezone.utc).isoformat(),
        )