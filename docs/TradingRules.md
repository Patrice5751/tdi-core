# TDI Trading Rules v1.0

## Objectif

TDI mesure la qualité d'un setup selon des règles objectives.

Il ne cherche pas à prédire avec certitude l'évolution future du marché.

## Piliers d'analyse

### 1. Trend

Le Trend Engine étudie notamment :

- la position du prix ;
- l'alignement EMA20, EMA50 et EMA200 ;
- la direction générale du marché.

### 2. Momentum

Le Momentum Engine étudie notamment :

- le RSI ;
- le MACD ;
- le signal MACD ;
- l'histogramme MACD.

### 3. Structure

Le Structure Engine doit étudier :

- les supports ;
- les résistances ;
- les swing highs ;
- les swing lows ;
- la position dans le range ;
- les cassures et les pullbacks.

### 4. Risk

Le Risk Engine devra vérifier :

- la distance du Stop Loss ;
- la distance du Take Profit ;
- le ratio rendement/risque ;
- la cohérence avec l'ATR ;
- le pourcentage de capital risqué.

### 5. Confluence

Le Confluence Engine agrégera les résultats des différents moteurs.

### 6. Validation

Le Validation Engine vérifiera que le plan de trading est respecté.

Exemples :

- tendance cohérente ;
- momentum cohérent ;
- structure valide ;
- ratio suffisant ;
- risque respecté ;
- absence d'événement économique bloquant.

### 7. Décision

Le Decision Engine produira une décision finale explicable :

- BUY ;
- SELL ;
- NO TRADE.

Chaque décision devra être accompagnée d'un score, d'un statut et de raisons détaillées.
