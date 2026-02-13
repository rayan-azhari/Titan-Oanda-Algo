# Titan-Oanda-Algo

> A quantitative trading system for OANDA — ML-driven strategy discovery, VectorBT Pro optimisation, NautilusTrader execution, and GCE deployment.

---

## Architecture

This project follows a **3-layer architecture** that separates *Probabilistic Intent* (AI) from *Deterministic Execution* (Code).

| Layer | Location | Purpose |
|---|---|---|
| **Directive** | `directives/` | Standard Operating Procedures — step-by-step instructions |
| **Orchestration** | Agent context | Intelligent routing — read directives, choose tools, handle errors |
| **Execution** | `execution/` | Deterministic Python scripts — API calls, data processing, ML training |

## Directory Structure

```
├── AGENTS.MD                      ← Agent system prompt
├── Titan Workspace Rules.md       ← Technical & ML constraints
├── directives/                    ← SOPs
│   ├── Alpha Research Loop (VectorBT Pro).md
│   ├── Machine Learning Strategy Discovery.md
│   ├── Nautilus-Oanda Adapter Construction.md
│   ├── Strategy Validation (Backtesting.py).md
│   ├── Live Deployment and Monitoring.md
│   └── Workspace Initialisation.md
├── execution/                     ← Python scripts
│   ├── setup_env.py               ← Interactive .env setup
│   ├── verify_connection.py       ← OANDA connection test
│   ├── download_oanda_data.py     ← Historical M5 OHLC data
│   ├── run_vbt_optimisation.py    ← VectorBT Pro parameter sweep
│   ├── build_ml_features.py       ← Feature matrix (X) + target (y)
│   ├── train_ml_model.py          ← Walk-forward ML training
│   ├── run_backtesting_validation.py ← Backtesting.py visual audit
│   ├── parse_oanda_instruments.py ← Nautilus instrument provider
│   ├── run_live.py                ← Live/paper trading engine
│   ├── kill_switch.py             ← Emergency: flatten all positions
│   ├── build_docker_image.py      ← Docker container for GCE
│   └── send_notification.py       ← Slack alert integration
├── config/                        ← TOML configuration
│   ├── instruments.toml           ← Currency pairs & granularities
│   ├── features.toml              ← Technical indicator definitions
│   ├── strategy_config.toml       ← Optimised strategy parameters
│   ├── training.toml              ← ML model & hyperparameters
│   └── risk.toml                  ← Position & risk limits
├── models/                        ← Deliverable: trained .joblib models
├── tests/                         ← Unit tests
├── .tmp/                          ← Intermediate: raw data, reports, logs
├── pyproject.toml                 ← Dependencies (managed by uv)
└── .env.example                   ← Credential template
```

## Quick Start

### 1. Install dependencies
```bash
uv sync
```

### 2. Configure credentials
```bash
uv run python execution/setup_env.py
```
Or manually: `cp .env.example .env` and edit.

### 3. Verify connection
```bash
uv run python execution/verify_connection.py
```

### 4. Alpha Research Loop
```bash
uv run python execution/download_oanda_data.py
uv run python execution/run_vbt_optimisation.py
```

### 5. ML Strategy Discovery
```bash
uv run python execution/build_ml_features.py
uv run python execution/train_ml_model.py
```

### 6. Validate & Deploy
```bash
uv run python execution/run_backtesting_validation.py
uv run python execution/run_live.py --mode practice
```

## Agent Personas

| Agent | Responsibilities |
|---|---|
| **Architect** | File structure, `config/` management, high-level design |
| **Engineer** | Python/Rust code, API adapters, Nautilus integration |
| **Researcher** | VectorBT scripts, ML features, model training, notebooks |

## Rules of Engagement

See [Titan Workspace Rules.md](Titan%20Workspace%20Rules.md) for the full constraints. Key rules:

- **`uv` only** — no bare `pip` installs
- **`decimal.Decimal`** for all financial types
- **`random_state=42`** — always
- **No look-ahead bias** — features lagged, targets future-derived
- **Google Style Guide** for all code
