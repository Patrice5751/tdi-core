# TDI Dashboard — UI Specification

## Status

Official visual reference for the MT5 TDI Dashboard.

The dashboard is a presentation layer for data produced by tdi-core.
It must not implement or duplicate TDI decision logic.

## Visual Reference

Target design: left-side TDI LIVE dashboard with prominent semi-circular gauges.

The reference design includes two major gauges:

- Bias Score
- Scenario Score

These gauges are a visual representation of scores calculated by tdi-core.
MT5 must not recalculate these scores.

## General Layout

- Position: left side of the MT5 chart
- Dark / black background
- Compact vertical panel
- Chart remains visible to the right
- Clear visual hierarchy
- Horizontal separators between major sections
- Functional colors only
- No additional oscillator or technical indicator inside the dashboard

## Information Hierarchy

1. TDI LIVE / Symbol / Status
2. Decision
3. Bias
4. Bias Score gauge
5. Confirmation
6. Scenario
7. Scenario Score gauge
8. Waiting For
9. Transition
10. Alert

## Functional Colors

- Green: favorable / confirmed / BUY
- Red or bright red-orange: SELL / warning / stale
- Orange: intermediate state
- White: primary neutral information
- Silver: secondary neutral information
- Dark gray: separators and borders

## Gauges

### Bias Score

Semi-circular gauge.

Range:
0–100

Displayed value comes directly from tdi-core.

### Scenario Score

Semi-circular gauge.

Range:
0–100

Displayed value comes directly from tdi-core.

## Current MT5 Baseline

The existing TDI_Dashboard.mq5 remains the functional base.

Already validated:

- 300 px panel width
- left-side positioning
- black background
- section hierarchy
- six horizontal separators
- WAITING FOR / TRANSITION spacing
- emphasized main title
- functional status colors

Future visual changes must evolve incrementally from this implementation.

## Architecture Rule

tdi-core = analysis and decision engine

MT5 TDI_Dashboard = visualization layer

The MT5 dashboard must never become a second independent TDI calculation engine.
