# Directive: Strategy Validation (Backtesting.py)

## Goal

Provide a **secondary validation layer** using a bar-by-bar processing engine to ensure logic consistency.

## Inputs

- Parquet data from `.tmp/data/raw`
- Optimised parameters from `config/strategy_config.toml`

## Execution Steps

### 1. Wrapper Construction

**Engineer Agent** creates a data-loading wrapper to convert Parquet to the `backtesting.py` Pandas format.

### 2. Logic Check

Implement the strategy class (RSI or ML-based logic).

### 3. Visual Audit

Generate HTML plots.

### 4. Validation

Manually inspect trade entries to ensure they align with the expected logic (e.g., buying at dips).

## Success Criteria

- Visual alignment between VBT entry signals and `Backtesting.py` visualisations.