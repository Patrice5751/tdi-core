# Technical Debt

Version: 0.9
Status: Living Document

## Purpose

This document records technical improvements that are known, intentional,
and postponed.

Items listed here are not forgotten defects. They are controlled refactoring
tasks planned for future versions.

---

## Pending Improvements

### TradeSetup location

Current location:

`src/tdi/advisor/trade_setup.py`

Target location:

`src/tdi/models/trade_setup.py`

Reason:

`TradeSetup` is a business data object. It does not evaluate rules or compute
scores.

Priority:

Medium

Target version:

1.0.0

---

### Residual validation module

Current file:

`src/tdi/analysis/validation_engine.py`

Issue:

The file contains only configuration imports and no engine implementation.

Target:

Remove it after confirming that no source file or test imports it.

Priority:

High

Target version:

0.9.0

---

### Residual RiskResult module

Current file:

`src/tdi/engines/risk_result.py`

Issue:

The active model is:

`src/tdi/analysis/risk_result.py`

Target:

Remove the residual file after confirming that it is unused.

Priority:

High

Target version:

0.9.0

---

### ATR validation

Current behaviour:

`ValidationEngine` sets:

`atr_ok = False`

Issue:

ATR is represented in the validation result but is not yet evaluated by the
validation engine.

Target:

Define and test an objective ATR validation rule.

Priority:

High

Target version:

1.0.0

---

### Multi-timeframe alignment

Missing capability:

TDI does not yet formally score trend alignment between H4 and H1.

Target:

Add a deterministic multi-timeframe alignment rule with explicit scoring.

Priority:

High

Target version:

1.0.0

---

### TradeAnalysisEngine

Current file:

`src/tdi/engines/trade_analysis_engine.py`

Current status:

Empty.

Target:

Use it as the single orchestration entry point for a complete trade analysis.

Priority:

High

Target version:

0.9.0

---

### CLI configuration persistence

Current behaviour:

Capital and risk defaults are stored directly in the CLI code.

Target:

Create persistent user settings using JSON.

Priority:

Medium

Target version:

0.9.0

---

### Statistics expansion

Current metrics:

- Trades
- Winners
- Losers
- Win Rate
- Expectancy
- Average Winner
- Average Loser
- Profit Factor

Missing metrics:

- Maximum Drawdown
- Performance by score range
- Performance by instrument
- Performance by setup
- Performance by TDI version

Priority:

High

Target version:

1.0.0