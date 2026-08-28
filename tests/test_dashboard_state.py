from tdi.graphical.dashboard_state import DashboardState


def test_dashboard_state_stores_display_values():
    state = DashboardState(
        symbol="XAUUSD",
        decision="Wait",
        preferred_side=None,
        target_side="BUY",
        bias_convergence="Toward",
        bias_readiness="Medium",
        bias_score=85,
        bias_aligned=False,
        structure_aligned=False,
        timing_favorable=False,
        momentum_confirmed=False,
        scenario="Building",
        scenario_score=85,
        waiting_for=("H4/H1 Bias Alignment",),
        transition="Improving",
        alert_level="INFO",
        alert_active=True,
    )

    assert state.symbol == "XAUUSD"
    assert state.decision == "Wait"
    assert state.target_side == "BUY"
    assert state.bias_score == 85
    assert state.scenario == "Building"
    assert state.scenario_score == 85
    assert state.waiting_for == ("H4/H1 Bias Alignment",)
    assert state.transition == "Improving"
    assert state.alert_level == "INFO"
    assert state.alert_active is True

