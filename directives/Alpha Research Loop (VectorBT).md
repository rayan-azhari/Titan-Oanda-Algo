# Directive: Alpha Research Loop (VectorBT)

## Goal

Identify and optimise a viable **daily swing trading** strategy for **EUR/USD**, **GBP/USD**, and **AUD/USD** using vectorised backtesting on higher timeframes.

## Timeframes

| Granularity | Use Case |
|---|---|
| **H1** | Lowest timeframe — entry/exit timing |
| **H4** | Primary analysis frame |
| **D** | Trend confirmation |
| **W** | Regime filter (trending vs ranging) |

## Inputs

- Instrument list from `config/instruments.toml`
- Parameter ranges (e.g., RSI 10–25, MA 20–100)

## Execution Steps

### 1. Data Ingestion

Run `execution/download_oanda_data.py` to pull **2+ years of H1/H4/D/W OHLC data**.
Store in `.tmp/data/raw` as Parquet.

### 2. Data Validation

Run `execution/validate_data.py` to check for gaps, duplicates, and outlier spikes.

### 3. Strategy Optimisation (In-Sample)

- **Researcher Agent** runs `execution/run_vbt_optimisation.py`.
- Uses open-source `vectorbt` (free) — no Pro license needed.
- Data is split **70% in-sample / 30% out-of-sample**.
- Optimisation runs on IS data only.

### 4. Out-of-Sample Validation

- Best candidates from IS are tested on the held-out OOS data.
- **Reject** any candidate whose OOS Sharpe drops below 50% of IS Sharpe (overfitting signal).

### 5. Candidate Selection

- Generate **Sharpe Ratio Heatmap** (plotly).
- **Architect Agent** identifies the "Plateau of Stability".

### 6. Parity Transfer

- Convert optimal parameters into `config/strategy_config.toml`.

> [!NOTE]
> **Upgrade path:** If parameter space grows too large for the free VectorBT, upgrade to VectorBT Pro for `@vbt.chunked` memory management. The API is compatible.

## Outputs

- Optimised strategy configuration
- Performance heatmap *(Artifact)*
- OOS validation report