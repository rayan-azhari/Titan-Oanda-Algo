# Directive: Alpha Research Loop (VectorBT Pro)

## Goal

Identify and optimise a viable trading strategy for **EUR/USD**, **GBP/USD**, and **AUD/USD** using vectorised backtesting.

## Inputs

- Instrument list
- Parameter ranges (e.g., RSI 10–20)

## Execution Steps

### 1. Data Ingestion

Run `execution/download_oanda_data.py` to pull **1 year of M5 OHLC data**.
Store in `.tmp/data/raw` as Parquet.

### 2. Strategy Optimisation

- **Researcher Agent** runs `execution/run_vbt_optimisation.py`.
- Use `vbt.parameterized` and `@vbt.chunked` for memory management.

### 3. Candidate Selection

- Generate **Sharpe Ratio Heatmap**.
- **Architect Agent** identifies the "Plateau of Stability".

### 4. Parity Transfer

- Convert optimal parameters into `config/strategy_config.toml`.

## Outputs

- Optimised strategy configuration
- Performance heatmap *(Artifact)*