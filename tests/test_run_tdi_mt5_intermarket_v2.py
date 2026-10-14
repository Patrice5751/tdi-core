import json
from types import SimpleNamespace
from unittest.mock import Mock

from scripts.run_tdi_mt5 import write_intermarket_v2
from tdi.graphical.market_direction import MarketDirection


def result(direction):
    return SimpleNamespace(
        h4=SimpleNamespace(direction=direction)
    )


def read_state(tmp_path):
    path = tmp_path / "intermarket_XAUUSD_v2.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_full_confirmation_uses_usdx_h4(tmp_path):
    pipeline = Mock()
    pipeline.analyze.return_value = SimpleNamespace(
        direction=MarketDirection.BEARISH
    )

    write_intermarket_v2(
        {
            "XAUUSD": result(MarketDirection.BULLISH),
            "XAGUSD": result(MarketDirection.BULLISH),
        },
        pipeline,
        tmp_path,
    )

    pipeline.analyze.assert_called_once_with(
        symbol="USDX", timeframe="H4", count=250
    )
    data = read_state(tmp_path)
    assert data["state"] == "Confirmed"
    assert data["score"] == 100
    assert data["coverage"] == 100


def test_usdx_failure_keeps_silver_confirmation(tmp_path):
    pipeline = Mock()
    pipeline.analyze.side_effect = RuntimeError("USDX unavailable")

    write_intermarket_v2(
        {
            "XAUUSD": result(MarketDirection.BULLISH),
            "XAGUSD": result(MarketDirection.BULLISH),
        },
        pipeline,
        tmp_path,
    )

    data = read_state(tmp_path)
    assert data["score"] == 100
    assert data["coverage"] == 60
    assert data["confirmations"]["USDX"]["trend"] is None


def test_missing_silver_keeps_dollar_confirmation(tmp_path):
    pipeline = Mock()
    pipeline.analyze.return_value = SimpleNamespace(
        direction=MarketDirection.BEARISH
    )

    write_intermarket_v2(
        {"XAUUSD": result(MarketDirection.BULLISH)},
        pipeline,
        tmp_path,
    )

    data = read_state(tmp_path)
    assert data["score"] == 100
    assert data["coverage"] == 40
    assert data["confirmations"]["XAGUSD"]["trend"] is None


def test_both_confirmations_missing(tmp_path):
    pipeline = Mock()
    pipeline.analyze.side_effect = RuntimeError("USDX unavailable")

    write_intermarket_v2(
        {"XAUUSD": result(MarketDirection.BULLISH)},
        pipeline,
        tmp_path,
    )

    data = read_state(tmp_path)
    assert data["state"] == "Unavailable"
    assert data["score"] is None
    assert data["coverage"] == 0


def test_missing_primary_replaces_previous_confirmation(tmp_path):
    pipeline = Mock()
    pipeline.analyze.return_value = SimpleNamespace(
        direction=MarketDirection.BEARISH
    )

    write_intermarket_v2(
        {
            "XAUUSD": result(MarketDirection.BULLISH),
            "XAGUSD": result(MarketDirection.BULLISH),
        },
        pipeline,
        tmp_path,
    )
    assert read_state(tmp_path)["score"] == 100

    pipeline.reset_mock()
    write_intermarket_v2({}, pipeline, tmp_path)

    data = read_state(tmp_path)
    assert data["state"] == "Unavailable"
    assert data["score"] is None
    assert data["coverage"] == 0
    pipeline.analyze.assert_not_called()
    