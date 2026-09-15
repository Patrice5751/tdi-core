import json

from tdi.graphical.dashboard_state import DashboardState
from tdi.graphical.json_dashboard_state_writer import (
    JsonDashboardStateWriter,
)


def test_json_dashboard_state_writer_writes_state(tmp_path):
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

    path = tmp_path / "dashboard" / "XAUUSD.json"

    JsonDashboardStateWriter.write(
        state=state,
        path=path,
    )

    assert path.exists()

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert data["symbol"] == "XAUUSD"
    assert data["decision"] == "Wait"
    assert data["target_side"] == "BUY"
    assert data["bias_score"] == 85
    assert data["scenario"] == "Building"
    assert data["scenario_score"] == 85
    assert data["waiting_for"] == [
        "H4/H1 Bias Alignment"
    ]
    assert data["transition"] == "Improving"
    assert data["alert_level"] == "INFO"
    assert data["alert_active"] is True
    assert data["opportunity"] == "None"
    assert data["decision_trigger"] is None
    assert data["scenario_display"] == ""
    assert data["h4_momentum"] == "Unavailable"
    assert data["h1_momentum"] == "Unavailable"
