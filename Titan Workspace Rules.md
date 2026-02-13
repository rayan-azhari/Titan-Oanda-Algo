# Titan-Oanda-Algo: Rules of Engagement

All agents must adhere to these constraints to ensure system integrity, financial accuracy, and scientific rigour.

---

## Technical Constraints

| Rule | Detail |
|---|---|
| **Dependency Management** | All Python code must use `uv` for dependency management. No bare `pip` installs. |
| **Financial Precision** | All financial data types must use `decimal.Decimal` or Nautilus native types. Standard floats are **strictly prohibited** for price or volume logic. |
| **Coding Standard** | All code must follow the [Google Style Guide](https://google.github.io/styleguide/pyguide.html). |
| **Documentation** | All public methods must include docstrings. |

---

## ML & Data Science Standards

| Rule | Detail |
|---|---|
| **Determinism** | Set explicit random seeds (`random_state=42`) for all ML training to ensure reproducibility. |
| **Data Leakage** | Features must be lagged. Targets must be future-derived. The Researcher must explicitly check for look-ahead bias before training. |
| **Storage** | Trained models are "Artifacts" and must be stored in `models/`, **not** `.tmp/`. |

---

## Agent Personas

| Agent | Runtime | Responsibilities |
|---|---|---|
| **Architect** | Gemini 3 Pro | File structure, `config/` management, and high-level design |
| **Engineer** | Gemini 3 Pro / Claude Sonnet | Writing Rust/Python code and API adapters |
| **Researcher** | Gemini 3 Pro | VectorBT scripts, data modelling, ML feature engineering, and Jupyter notebooks |