# Case 1 Methodology Summary

## Overview
This document explains the step-by-step methodology for forecasting Superman Plus initial 15-week demand, leveraging historical data and analytical adjustments.

---

## 🚀 Step 1: Define Baseline
- Used **Princess Plus** 15-week sales data as baseline reference.
- Time-shifted to align with Superman Plus' Sep Wk3 launch.

---

## 🚀 Step 2: Seasonality Adjustment
- Applied **seasonality uplift**:
  - +25% for Sep Wk3–Sep Wk4
  - +15% for Oct Wk1–Oct Wk2
- Reflects pre-holiday demand surges observed historically.

---

## 🚀 Step 3: Price Elasticity Analysis
- Calculated real Price Elasticity (PE) by region:
  - Compared total 15-week sales of **Dwarf Plus** and **Princess Plus**.
  - PE Formula:  
    \[
    PE = \\frac{\\text{Demand \\% Change}}{\\text{Price \\% Change}}
    \]
- Resulted in different sensitivity per region:
  - **AMR:** -0.45
  - **Europe:** -0.24
  - **PAC:** +0.01

---

## 🚀 Step 4: Price Adjustment
- Superman Plus price: $205
- +2.5% price increase from Princess Plus.
- Applied region-specific adjustment multipliers based on PE.

---

## 🚀 Step 5: Forecast Generation
- Computed final regional forecast:
  - Base sales × Seasonality uplift × PE multiplier
- Applied light smoothing to maintain realistic forecast curves.

---

## 📈 Final Outputs
- 15-week forecast by region (AMR, Europe, PAC)
- Line charts visualizing weekly trends
- Data exported to `case1_forecast.csv`

---

## 🛡️ Engineering Excellence
- Full traceability: raw inputs to final forecast
- Python OOP Script
- Visualized inputs/outputs
- GitHub-structured delivery for transparency

---

## ✨ Non-Technical Insights
- PAC shows resilience to price increases — growth focus area.
- AMR is price-sensitive — requires closer post-launch monitoring.
- Early seasonality-driven demand surge must be captured in supply planning.

---

## 📋 Conclusion
- Comprehensive, data-driven forecast model.
- Ready for execution with built-in flexibility for real-world variations.

