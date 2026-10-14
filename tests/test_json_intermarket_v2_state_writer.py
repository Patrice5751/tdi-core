import json
from datetime import datetime

from tdi.analysis.trend_analysis import Trend
from tdi.engines.intermarket_v2_engine import IntermarketV2Engine
from tdi.graphical.json_intermarket_v2_state_writer import (
    JsonIntermarketV2StateWriter,
)


def test_writer_serializes_full_confirmation(tmp_path):
    analysis = IntermarketV2Engine().analyze(
        Trend.BULLISH,
        Trend.BULLISH,
        Trend.BEARISH,
    )
    path = tmp_path / "dashboard" / "intermarket_XAUUSD_v2.json"

    JsonIntermarketV2StateWriter.write(analysis, path)

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["version"] == 2
    assert data["primary_symbol"] == "XAUUSD"
    assert data["state"] == "Confirmed"
    assert data["score"] == 100
    assert data["coverage"] == 100
    assert data["primary_trend"] == Trend.BULLISH.value

    silver = data["confirmations"]["XAGUSD"]
    assert silver["trend"] == Trend.BULLISH.value
    assert silver["score"] == 100
    assert silver["weight"] == 60
    assert silver["relationship"] == "Direct"

    dollar = data["confirmations"]["USDX"]
    assert dollar["trend"] == Trend.BEARISH.value
    assert dollar["score"] == 100
    assert dollar["weight"] == 40
    assert dollar["relationship"] == "Inverse"

    timestamp = datetime.fromisoformat(data["updated_at"])
    assert timestamp.utcoffset().total_seconds() == 0
    assert not path.with_suffix(".json.tmp").exists()


def test_writer_preserves_missing_source_as_null(tmp_path):
    analysis = IntermarketV2Engine().analyze(
        Trend.BULLISH,
        Trend.BULLISH,
        None,
    )
    path = tmp_path / "intermarket_XAUUSD_v2.json"

    JsonIntermarketV2StateWriter.write(analysis, path)

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["score"] == 100
    assert data["coverage"] == 60
    assert data["confirmations"]["USDX"]["trend"] is None
    assert data["confirmations"]["USDX"]["score"] is None


def test_writer_replaces_previous_result_when_unavailable(tmp_path):
    engine = IntermarketV2Engine()
    path = tmp_path / "intermarket_XAUUSD_v2.json"

    JsonIntermarketV2StateWriter.write(
        engine.analyze(Trend.BULLISH, Trend.BULLISH, Trend.BEARISH),
        path,
    )
    JsonIntermarketV2StateWriter.write(
        engine.analyze(Trend.BULLISH, None, None),
        path,
    )

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["state"] == "Unavailable"
    assert data["score"] is None
    assert data["coverage"] == 0
    assert not path.with_suffix(".json.tmp").exists()
    