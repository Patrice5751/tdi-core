import json

from tdi.analysis.intermarket_analysis import (
    IntermarketAnalysis,
    IntermarketState,
)
from tdi.analysis.trend_analysis import Trend
from tdi.graphical.json_intermarket_state_writer import (
    JsonIntermarketStateWriter,
)


def test_json_intermarket_state_writer_writes_analysis(tmp_path):
    analysis = IntermarketAnalysis(
        state=IntermarketState.MIXED,
        score=50,
        primary_trend=Trend.NEUTRAL,
        confirmation_trend=Trend.BULLISH,
        reason="Intermarket confirmation is mixed.",
    )

    path = (
        tmp_path
        / "dashboard"
        / "intermarket_XAUUSD_XAGUSD.json"
    )

    JsonIntermarketStateWriter.write(
        analysis=analysis,
        primary_symbol="XAUUSD",
        confirmation_symbol="XAGUSD",
        path=path,
    )

    assert path.exists()

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert data["primary_symbol"] == "XAUUSD"
    assert data["confirmation_symbol"] == "XAGUSD"
    assert data["state"] == "Mixed"
    assert data["score"] == 50
    assert data["primary_trend"] == "Neutral"
    assert data["confirmation_trend"] == "Bullish"
    assert data["reason"] == (
        "Intermarket confirmation is mixed."
    )
    assert data["updated_at"]
    