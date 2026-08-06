# MARKET DIRECTION SPECIFICATION

Version : 0.11 Draft

---

# Purpose

The Market Direction Engine determines the dominant market direction before any technical indicator is analysed.

It is the first stage of the Graphical Intelligence Engine.

Its objective is to answer one question:

"In which direction is the market really moving?"

---

# Guiding Principle

Market structure determines direction.

Indicators only confirm direction.

A moving average never creates a trend.

It only confirms an existing market structure.

---

# Analysis Sequence

The engine analyses the market in the following order.

1. Swing detection
2. Market structure
3. Moving averages
4. Multi-timeframe coherence
5. Final confidence

---

# Step 1 — Swing Detection

The engine detects significant swing highs and swing lows.

A swing high is valid if:

- higher than the previous two candles
- higher than the next two candles
- amplitude ≥ 0.5 ATR

A swing low is defined symmetrically.

Minimum requirement:

- 3 significant highs
- 3 significant lows

Recommended analysis window:

50–100 candles.

---

# Step 2 — Market Structure

The dominant structure is determined from the sequence of swings.

Bullish:

HH + HL

Bearish:

LH + LL

Mixed:

Transition

No clear progression:

Range

This structural analysis is the primary source of direction.

---

# Step 3 — Moving Average Confirmation

Moving averages confirm the structure.

Reference averages:

MA20
MA50
MA200

Three confirmation criteria are analysed.

## Price position

Bullish:

Price > MA20 > MA50 > MA200

Bearish:

Price < MA20 < MA50 < MA200

---

## Average ordering

Perfect ordering increases confidence.

Mixed ordering reduces confidence.

---

## Average slopes

The engine evaluates:

- positive slope
- negative slope
- flattening
- recent crossover
- old crossover

Crossovers never determine direction alone.

---

# Step 4 — Multi-Timeframe Coherence

Reference timeframes:

H4
H1

The engine measures coherence.

Examples.

Bullish / Bullish

Very High

Bullish / Pullback

High

Bullish / Bearish

Low

Range / Bullish

Low

---

# Step 5 — Final Classification

Possible outputs:

Bullish

Bearish

Transition

Range

---

# Confidence

Confidence combines:

Market Structure

Moving Average Confirmation

Multi-Timeframe Coherence

Output:

0–100

---

# Explainability

Every conclusion must include:

Detected structure

Swing count

Moving average confirmation

Multi-timeframe analysis

Reasons

No unexplained decision is allowed.

---

# Future Extensions

Future releases may include:

Channel detection

Bias lines

Support quality

Resistance quality

Pullback quality

Breakout quality

Market Geometry Score