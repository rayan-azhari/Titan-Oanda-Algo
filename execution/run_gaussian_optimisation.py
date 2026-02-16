"""Gaussian Channel VectorBT Optimisation Script.

Loads EUR/USD H1 data, sweeps period/poles/sigma combinations using the
GaussianChannel indicator, calculates Sharpe ratios, and saves the best
parameters to config/gaussian_channel_config.toml.

Usage:
    uv run python execution/run_gaussian_optimisation.py
"""

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project bootstrap — ensure repo root is on sys.path
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import vectorbt as vbt

from execution.indicators.gaussian_filter import GaussianChannel

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_PATH = ROOT / "data" / "EUR_USD_H1.parquet"
CONFIG_PATH = ROOT / "config" / "gaussian_channel_config.toml"
REPORT_DIR = ROOT / ".tmp" / "reports"

# Parameter ranges (from the directive)
PERIODS = list(range(50, 301, 10))  # 50 to 300, step 10
POLES = [1, 2, 3, 4]
SIGMAS = [1.5, 2.0, 2.5, 3.0]

# Backtest settings
INIT_CASH = 10_000
FEES = 0.0002  # 2 pips approx spread cost


def load_data() -> pd.DataFrame:
    """Load EUR/USD H1 OHLC data from parquet."""
    if not DATA_PATH.exists():
        print(f"ERROR: Data file not found at {DATA_PATH}")
        print("Run:  uv run python execution/fetch_eur_usd.py  first.")
        sys.exit(1)

    df = pd.read_parquet(DATA_PATH)
    print(f"Loaded {len(df)} bars from {DATA_PATH.name}")
    return df


def run_optimisation(df: pd.DataFrame) -> pd.DataFrame:
    """Run GaussianChannel over all parameter combos, return Sharpe results."""
    high = df["mid_h"].values if "mid_h" in df.columns else df["high"].values
    low = df["mid_l"].values if "mid_l" in df.columns else df["low"].values
    close = df["mid_c"].values if "mid_c" in df.columns else df["close"].values

    results = []
    total = len(PERIODS) * len(POLES) * len(SIGMAS)
    done = 0

    for sigma in SIGMAS:
        for poles in POLES:
            # Run the indicator across all periods at once
            gc = GaussianChannel.run(
                high,
                low,
                close,
                period=PERIODS,
                poles=poles,
                sigma=sigma,
            )

            for i, period in enumerate(PERIODS):
                mid_col = gc.middle.iloc[:, i].values
                upper_col = gc.upper.iloc[:, i].values
                lower_col = gc.lower.iloc[:, i].values
                close_arr = close

                # Signal logic (from directive):
                #   Long: price crosses above upper band (momentum breakout)
                #         OR price bounces off middle line (trend following)
                #   Short: price crosses below lower band
                entries_long = (
                    (close_arr[1:] > upper_col[1:]) & (close_arr[:-1] <= upper_col[:-1])
                ) | ((close_arr[1:] > mid_col[1:]) & (close_arr[:-1] <= mid_col[:-1]))
                entries_short = (close_arr[1:] < lower_col[1:]) & (close_arr[:-1] >= lower_col[:-1])

                # Pad first bar
                entries_long = np.concatenate(([False], entries_long))
                entries_short = np.concatenate(([False], entries_short))

                # VBT portfolio — long entries exit on short entries and vice versa
                pf = vbt.Portfolio.from_signals(
                    close=close_arr,
                    entries=entries_long,
                    exits=entries_short,
                    init_cash=INIT_CASH,
                    fees=FEES,
                    freq="1h",
                )

                sharpe = pf.sharpe_ratio()
                total_return = pf.total_return()
                n_trades = pf.trades.count()

                results.append(
                    {
                        "period": period,
                        "poles": poles,
                        "sigma": sigma,
                        "sharpe": sharpe,
                        "total_return": total_return,
                        "n_trades": n_trades,
                    }
                )

                done += 1
                if done % 50 == 0:
                    print(f"  [{done}/{total}] combos tested...")

    return pd.DataFrame(results)


def save_best_config(results_df: pd.DataFrame) -> dict:
    """Find the best combo by Sharpe and save to TOML."""
    best = results_df.loc[results_df["sharpe"].idxmax()]
    print("\n=== Best Parameters ===")
    print(f"  Period: {int(best['period'])}")
    print(f"  Poles:  {int(best['poles'])}")
    print(f"  Sigma:  {best['sigma']:.1f}")
    print(f"  Sharpe: {best['sharpe']:.4f}")
    print(f"  Return: {best['total_return']:.2%}")
    print(f"  Trades: {int(best['n_trades'])}")

    config_content = f"""# Gaussian Channel — Optimised Parameters
# Auto-generated by run_gaussian_optimisation.py

[gaussian_channel]
period = {int(best["period"])}
poles = {int(best["poles"])}
sigma = {best["sigma"]:.1f}

[gaussian_channel.results]
sharpe = {best["sharpe"]:.4f}
total_return = {best["total_return"]:.4f}
n_trades = {int(best["n_trades"])}
"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(config_content, encoding="utf-8")
    print(f"\nSaved config to {CONFIG_PATH}")

    return best.to_dict()


def generate_heatmap(results_df: pd.DataFrame) -> None:
    """Generate an interactive Plotly heatmap: Period vs Poles coloured by Sharpe."""
    try:
        import plotly.express as px
    except ImportError:
        print("Plotly not installed — skipping heatmap.")
        return

    # Aggregate over sigma (take max Sharpe for each period/poles pair)
    pivot = results_df.groupby(["period", "poles"])["sharpe"].max().reset_index()
    pivot_table = pivot.pivot(index="poles", columns="period", values="sharpe")

    fig = px.imshow(
        pivot_table,
        labels=dict(x="Period", y="Poles", color="Sharpe"),
        title="Gaussian Channel: Poles vs Period — Sharpe Ratio",
        color_continuous_scale="RdYlGn",
        aspect="auto",
    )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REPORT_DIR / "gaussian_channel_heatmap.html"
    fig.write_html(str(out_path))
    print(f"Heatmap saved to {out_path}")


def main() -> None:
    """Entry point."""
    print("=" * 60)
    print("Gaussian Channel Optimisation")
    print("=" * 60)

    df = load_data()
    results_df = run_optimisation(df)

    # Save full scoreboard
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    scoreboard_path = REPORT_DIR / "gaussian_channel_scoreboard.csv"
    results_df.to_csv(scoreboard_path, index=False)
    print(f"\nFull scoreboard saved to {scoreboard_path}")

    save_best_config(results_df)
    generate_heatmap(results_df)

    print("\nDone.")


if __name__ == "__main__":
    main()
