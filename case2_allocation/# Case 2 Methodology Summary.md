# Case 2 Methodology Summary

## Overview
This document outlines the detailed step-by-step methodology for solving Case 2 of the Superman Plus Material A allocation challenge, based on the final refined script.

---

## 🎯 Objective
The goal of this model is to **optimize weekly supply allocation** across three product lines—**Superman, Superman Plus, and Superman Mini**—over a 4-week planning window, while satisfying demand, supply, and inventory constraints.

---

## 🧩 Key Components

### 1. **Supply Allocation**
- **Total supply** is fixed at **1200 units**, distributed across 4 weeks.
- Weekly allocation for each product is determined through integer programming to fully utilize supply without exceeding the limit.

### 2. **Cumulative Actual Build**
- Calculated by adding a **fixed base buffer** to each product’s weekly allocation:
  - Superman / Superman Plus: `Allocation + 70`
  - Superman Mini: `Allocation + 60`

### 3. **Demand Constraints**
- **Cumulative demand forecasts** are provided for each product-week.
- **Superman** and **Superman Mini** allocations must meet or exceed forecast.
- **Superman Plus** demand is a soft constraint (penalized slack allowed).

### 4. **Week of Supply (WoS) Constraints**
- WoS is computed using: WoS = (Cumulative Actual Build - Cumulative Demand) / Avg Future Incremental Demand
- For each product in weeks 2 to 5:
- **WoS must be ≥ 4, ≤ 2**, strictly enforced.
- Week 5 uses the same future demand rate as week 4.

### 5. **Channel Allocation (Superman Plus)**
- Allocated across three channels:
- **Online > Retail > Reseller** (priority order enforced).
- Deviations from channel-level cumulative demand are minimized.

### 6. **Regional Reseller Allocation**
- Reseller channel allocation is further distributed across:
- **AMR, Europe, PAC**
- Soft constraints are applied to minimize deviation from regional asks.

---

## 🧮 Optimization Engine

- Built using **Gurobi Optimizer (v12.0.1)** with Python.
- All allocation decisions are **integers**, ensuring operational feasibility.
- Multi-stage optimization:
1. Product-level allocation
2. Channel-level allocation (Superman Plus)
3. Regional reseller distribution

---

## ✅ Outcome

- Full utilization of available supply.
- Demand coverage with minimal slack.
- WoS targets maintained to ensure inventory health.
- Channel and regional priorities respected.



