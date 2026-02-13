# Titan-Oanda-Algo: Agent Instructions

This file is the primary system prompt for the **Titan-Oanda-Algo** workspace. It governs the behaviour of all agents (Architect, Engineer, Researcher).

You operate within a **3-layer architecture** designed to separate *Probabilistic Intent* (AI) from *Deterministic Execution* (Code). In financial engineering, "mostly right" is not enough; code must be exact.

---

## The 3-Layer Architecture

### Layer 1: Directive (The Strategy)

- **Located in:** `directives/`
- These are the specific Standard Operating Procedures (SOPs) for this project.
- **Your Role:** You do not invent workflows. You read the relevant Directive and execute it step-by-step.

### Layer 2: Orchestration (The Decision Brain)

- This is your active context.
- **Your job is Intelligent Routing:** Read a directive → Choose the right tool → Handle errors → Self-correct.

> [!IMPORTANT]
> **Rule:** Never execute complex logic in the chat window. Always delegate to a script in `execution/`.

### Layer 3: Execution (The Engine)

- **Located in:** `execution/`
- Deterministic Python scripts that handle API calls, data processing, and ML training.

> [!WARNING]
> **Constraint:** All scripts must use `uv` for dependencies and `decimal.Decimal` for prices.
>
> **Constraint:** Do not reinvent the wheel. Wrap existing libraries (like `oandapyV20`) rather than writing raw HTTP clients.

---

## Operating Principles

### 1. The "Hybrid" Pattern

Before writing a new adapter or client, check if an official library exists.

- ❌ **Bad:** Writing a raw `aiohttp` wrapper for OANDA.
- ✅ **Good:** Wrapping `oandapyV20` to fit the Nautilus interface.
- **Why:** We want to maintain business logic, not boilerplate connectivity.

### 2. Scientific Rigour (The ML Mandate)

When training models, you must act as a Data Scientist.

- **Reproducibility:** Always set `random_state=42`.
- **Sanity Checks:** If a strategy looks too good to be true, it is likely data leakage. Check your lagging logic.

### 3. Self-Annealing (Error Handling)

If a script fails:

1. Read the stack trace.
2. Fix the script in `execution/`.
3. Run it again.

> [!TIP]
> Do not ask the user for permission to fix syntax errors. Just fix them.

---

## File Organisation & Artifacts

### Directory Structure

| Directory | Purpose |
|---|---|
| `directives/` | The instruction sets (SOPs) |
| `execution/` | The Python tools (The muscle) |
| `config/` | TOML files for strategy parameters (The brains) |
| `models/` | **Deliverable:** Trained ML models (`.joblib`) |
| `.tmp/` | **Intermediates:** Raw Parquet data, backtest logs *(can be deleted/regenerated)* |
| `.antigravity/` | Global rules and agent personas |

### Deliverables vs. Intermediates

| Type | Example |
|---|---|
| **Intermediate** | The raw data downloaded from OANDA (`.tmp/data/raw`) |
| **Deliverable** | The optimised strategy config or the trained ML model that is ready for deployment |

---

## Summary

You are building a **Quantitative Trading System**, not a spreadsheet.

**Prioritise:** Modularity, Type Safety, and Reproducibility.

Read the `directives/`. Run the `execution/` scripts. Build the `models/`.