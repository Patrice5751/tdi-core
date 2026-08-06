# TDI Core Architecture

Version: 0.9
Status: Living Document

---

# Purpose

TDI (Trading Decision Intelligence) is a deterministic trading decision engine.

Its objective is not to predict markets, but to evaluate the quality of a trading setup using objective, explainable and testable rules.

The architecture is designed around a strict separation of responsibilities.

---

# Architecture Overview

```
                Applications
        ┌────────────┬─────────────┐
        │            │             │
      CLI          MT5         Future UI
        │            │
        └──────┬─────┘
               │
               ▼
          TDI CORE
               │
    ┌──────────┼──────────┐
    │          │          │
 Models    Analysis    Advisor
               │
               ▼
            Engines
               │
               ▼
           Reporting
               │
               ▼
            Journal
```

---

# Modules

## models

Business objects.

Contains immutable objects representing the trading domain.

Examples:

- Trade
- MarketSnapshot
- PriceStructure

Future:

- TradeSetup
- TradeOutcome

Rules:

- no calculations
- no business logic
- no reporting

---

## analysis

Represents observations produced by the engines.

Examples:

- TrendAnalysis
- MomentumAnalysis
- StructureAnalysis

Results:

- AnalysisResult
- ValidationResult
- RiskResult
- DecisionResult
- AdvisorResult

Rules:

- immutable
- descriptive only

---

## advisor

Business rules.

Contains every scoring rule.

Examples:

- TrendRule
- MomentumRule
- StructureRule
- ATRRule
- RRRule

Also contains:

- RuleEngine
- RuleRegistry
- RuleResult
- ScoreAggregator

Rules:

- deterministic
- explainable
- independently testable

---

## engines

Execution layer.

Responsible for orchestrating the different analyses.

Examples:

- TrendEngine
- MomentumEngine
- StructureEngine
- RiskEngine
- ValidationEngine
- DecisionEngine
- TradeAdvisor

Future:

- TradeAnalysisEngine

Rules:

- orchestrate
- never display
- never store data

---

## reporting

Transforms analysis into reports.

Outputs:

- text
- markdown

Future:

- PDF
- HTML

---

## journal

Persistence layer.

Contains:

- TradeRecord
- TradeJournal
- JsonTradeJournalRepository

Purpose:

Store every analysed trade without modifying the original analysis.

---

## app

User interfaces.

Examples:

- CLI
- MT5
- Desktop
- Web

Applications must never contain business logic.

---

# Architectural Principles

## 1. Single Responsibility

Each class has one responsibility.

---

## 2. Deterministic Decision

The same inputs must always produce the same outputs.

---

## 3. Explainability

Every decision must be explainable.

No black-box behaviour.

---

## 4. Testability

Every rule must be unit tested.

---

## 5. Separation of Concerns

Models

↓

Analysis

↓

Advisor

↓

Engines

↓

Reporting

↓

Journal

---

## 6. No MT5 Dependency

TDI Core never depends on MT5.

MT5 depends on TDI Core.

---

# Vision

TDI is not an automated trading robot.

It is a professional decision support system designed to improve the quality and consistency of discretionary trading decisions.