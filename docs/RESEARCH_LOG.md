# TDI Research Log

This document records experimental hypotheses, version changes and formal reviews.

---

## 2026-08-02 — Baseline experiment opened

### Version

TDI 0.9.0

### Objective

Measure the performance and decision quality of the current TDI baseline.

### Experimental status

Active

### Target sample

30 analysed opportunities

### Main KPI

Expectancy in R per executed trade

### Secondary KPIs

- Win Rate
- Profit Factor
- Average Winner
- Average Loser
- Maximum Drawdown

### H4/H1 alignment

Recorded as an observation.

Not included in the score or decision.

### Trading execution

Manual execution on MT5.

TDI analyses and proposes.

The trader decides.

### Rule policy

Decision rules are frozen during the 30-observation baseline.

Only non-decision improvements and verified bug fixes are permitted.

---

## Pending hypothesis — H4/H1 alignment

### Hypothesis

Trades aligned on H4 and H1 produce higher Expectancy and lower drawdown than non-aligned trades.

### Candidate version

TDI 0.10.0

### Current status

Engine implemented.

Not yet integrated into the experimental baseline score.

### Validation plan

Compare aligned and non-aligned opportunities recorded during the baseline.

Do not draw a formal conclusion before a sufficient sample exists.