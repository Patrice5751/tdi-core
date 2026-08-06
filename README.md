@'
# TDI — Trading Decision Intelligence

> **Better decisions before better profits.**

## Project Status

Current version: **0.9 (Work in Progress)**

Current capabilities:

- Objective trade analysis
- Rule-based scoring
- Decision engine
- Confidence evaluation
- Setup Quality
- Trade Grade
- Assessment
- Recommendation engine
- Confluence engine
- Explainability engine
- Professional reporting

Test suite:

**80 automated tests**

## Présentation

TDI est un assistant d'analyse et de validation de décisions de trading.

Il ne passe aucun ordre automatiquement et ne remplace pas la décision du trader.

Son objectif est d'évaluer un setup selon des règles déterministes, objectives et explicables.

## Philosophie

TDI répond à trois questions principales :

1. Le contexte de marché est-il favorable ?
2. Le setup respecte-t-il le plan de trading ?
3. Le risque est-il acceptable ?

Les modèles d'intelligence artificielle peuvent être utilisés pour expliquer les résultats, mais ils ne doivent pas produire directement la décision de trading.

The trader always makes the final decision.

TDI evaluates.

The trader decides.

## Core Engines

- Rule Engine
- Recommendation Engine
- Confluence Engine
- Explainability Engine
- Verdict Engine
- Report Engine

## Architecture

```text
tdi-core/
├── config/
├── docs/
├── src/
│   └── tdi/
│       ├── analysis/
│       ├── engines/
│       ├── indicators/
│       ├── models/
│       ├── reports/
│       ├── rules/
│       ├── services/
│       └── utils/
├── tests/
├── CHANGELOG.md
├── LICENSE
└── README.md

## Roadmap

See ROADMAP.md

The current objective is Version 1.0.

The project is now entering its real-world validation phase using MT5 and live trading analyses.