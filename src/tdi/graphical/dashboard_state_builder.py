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
        )

def test_dashboard_state_builder_builds_alert_state():
    decision = SimpleNamespace(
        decision=value("Wait"),
        preferred_side="SELL",
        bias_aligned=True,
        structure_aligned=True,
        timing_favorable=False,
        momentum_confirmed=False,
    )

    bias_readiness = SimpleNamespace(
        convergence=value("Toward"),
        readiness=value("High"),
        score=90,
    )

    scenario = SimpleNamespace(
        target_side="SELL",
        state=value("Ready"),
        score=90,
    )

    wait_plan = SimpleNamespace(
        conditions=[
            value("Momentum Confirmation"),
        ]
    )

    transition = SimpleNamespace(
        transition=value("Improving"),
    )

    alert = SimpleNamespace(
        level=value("INFO"),
        active=True,
    )

    state = DashboardStateBuilder.build(
        symbol="XAUUSD",
        decision=decision,
        bias_readiness=bias_readiness,
        scenario=scenario,
        wait_plan=wait_plan,
        transition=transition,
        alert=alert,
    )

    assert state.transition == "Improving"
    assert state.alert_level == "INFO"
    assert state.alert_active is True