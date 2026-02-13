# Directive: Multi-Timeframe Confluence

## Goal

Only trade when **all three timeframes** (H1, H4, D) agree on direction. This dramatically reduces false signals by requiring top-down confirmation before entry.

## Concept

| Timeframe | Role | Weight |
|---|---|---|
| **D** | Sets the directional bias — are we in a trend? | 40% |
| **H4** | Confirms the swing — is this a valid pullback? | 40% |
| **H1** | Times the entry — is the short-term turning? | 20% |

```
    D  ──── TREND BIAS ────→  Bullish ✓
    H4 ──── SWING CONFIRM ──→ Bullish ✓
    H1 ──── ENTRY TIMING ───→ Bullish ✓
                                ↓
                        📈 FULL CONFLUENCE
                        ↓
                    Execute BUY signal
```

## Signal Components

Each timeframe produces 3 sub-signals:

1. **Trend** — Dual-MA crossover (fast > slow = bullish)
2. **Momentum** — RSI position (>60 = bullish, <40 = bearish)
3. **Structure** — Higher highs/lows vs lower highs/lows

These are averaged into a **bias** per timeframe, then weighted into a **confluence score**.

## Execution Steps

### 1. Download Multi-Timeframe Data

```bash
uv run python execution/download_oanda_data.py
```
Ensure H1, H4, and D data are all present in `.tmp/data/raw/`.

### 2. Generate Confluence Signals

```bash
uv run python execution/mtf_confluence.py
```
Outputs per-pair confluence features to `.tmp/data/features/{PAIR}_mtf_confluence.parquet`.

### 3. Integrate with ML Features

Run `build_ml_features.py` to combine base indicators with MTF confluence features. The ML model can then learn which confluence setups are most predictive.

### 4. Backtest with Confluence Filter

Use `run_vbt_optimisation.py` on the H4 timeframe, but only allow trades where `confluence_signal ≠ 0`.

## Configuration

See `config/mtf.toml` for:
- Timeframe weights
- Confirmation threshold
- Per-timeframe indicator parameters

> [!IMPORTANT]
> Higher timeframe data is **forward-filled** onto the H1 timeline. This is safe because we only carry forward the *last known* value — no future data leaks.

## Outputs

- `{PAIR}_mtf_confluence.parquet` — per-bar confluence features
- Confluence signal breakdown (% bullish, bearish, neutral)
