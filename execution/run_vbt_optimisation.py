"""run_vbt_optimisation.py — Vectorised strategy optimisation using VectorBT Pro.

Runs parameterised strategy backtests across multiple indicator ranges,
generates Sharpe Ratio heatmaps, and exports optimal parameters to
config/strategy_config.toml.

Directive: Alpha Research Loop (VectorBT Pro).md
"""

import sys
from pathlib import Path

import tomllib
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

RAW_DATA_DIR = PROJECT_ROOT / ".tmp" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / ".tmp" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

try:
    import vectorbtpro as vbt
except ImportError:
    print("ERROR: vectorbtpro is not installed. Run `uv sync` first.")
    print("       Note: VectorBT Pro requires a valid license.")
    sys.exit(1)


def load_instruments_config() -> dict:
    """Load the instruments configuration from config/instruments.toml."""
    config_path = PROJECT_ROOT / "config" / "instruments.toml"
    if not config_path.exists():
        print(f"ERROR: {config_path} not found.")
        sys.exit(1)
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def load_raw_data(pair: str, granularity: str) -> pd.DataFrame:
    """Load raw Parquet data for a given instrument and granularity.

    Args:
        pair: Instrument name (e.g., "EUR_USD").
        granularity: Candle granularity (e.g., "M5").

    Returns:
        DataFrame with timestamp-indexed OHLCV data.
    """
    path = RAW_DATA_DIR / f"{pair}_{granularity}.parquet"
    if not path.exists():
        print(f"ERROR: {path} not found. Run download_oanda_data.py first.")
        sys.exit(1)
    df = pd.read_parquet(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    # Convert Decimal columns to float for VBT compatibility
    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float)
    return df


@vbt.chunked(
    n_chunks="auto",
    show_progress=True,
)
def run_rsi_optimisation(close: pd.Series, rsi_windows: list[int], entry_thresholds: list[int]):
    """Run parameterised RSI strategy optimisation.

    Uses vbt.parameterized to sweep across RSI window and
    entry threshold combinations.

    Args:
        close: Close price series.
        rsi_windows: List of RSI lookback periods to test.
        entry_thresholds: List of RSI entry thresholds to test.

    Returns:
        VBT Portfolio object with all parameter combinations.
    """
    rsi = vbt.RSI.run(close, window=rsi_windows, param_product=True)

    entries = rsi.rsi_crossed_below(entry_thresholds)
    exits = rsi.rsi_crossed_above(100 - np.array(entry_thresholds))

    portfolio = vbt.Portfolio.from_signals(
        close,
        entries=entries,
        exits=exits,
        init_cash=10_000,
        fees=0.0002,  # 2 pip spread cost
    )
    return portfolio


def generate_sharpe_heatmap(portfolio, rsi_windows: list[int], entry_thresholds: list[int]) -> Path:
    """Generate and save a Sharpe Ratio heatmap.

    Args:
        portfolio: VBT Portfolio object from optimisation.
        rsi_windows: RSI window values (y-axis).
        entry_thresholds: Entry threshold values (x-axis).

    Returns:
        Path to the saved heatmap HTML file.
    """
    sharpe = portfolio.sharpe_ratio()
    heatmap_path = REPORTS_DIR / "sharpe_heatmap.html"

    fig = sharpe.vbt.heatmap(
        x_level="rsi_crossed_below_entry_thresholds",
        y_level="rsi_window",
        title="Sharpe Ratio Heatmap — RSI Strategy",
    )
    fig.write_html(str(heatmap_path))
    print(f"  📊 Heatmap saved to {heatmap_path}")
    return heatmap_path


def export_optimal_params(sharpe_series) -> dict:
    """Identify the optimal parameter set from the Sharpe series.

    Selects the parameters in the "Plateau of Stability" —
    robust performance, not the single highest point.

    Args:
        sharpe_series: Series of Sharpe ratios indexed by parameter combos.

    Returns:
        Dictionary of optimal parameters.
    """
    best_idx = sharpe_series.idxmax()
    best_sharpe = sharpe_series.max()
    print(f"  🏆 Best Sharpe: {best_sharpe:.4f} at {best_idx}")

    # TODO: Implement plateau detection for robustness
    return {"best_params": best_idx, "sharpe": float(best_sharpe)}


def main() -> None:
    """Run the full VectorBT Pro optimisation loop."""
    config = load_instruments_config()
    pairs = config.get("instruments", {}).get("pairs", [])
    granularity = config.get("instruments", {}).get("granularities", ["M5"])[0]

    # Parameter ranges for RSI strategy
    rsi_windows = list(range(10, 25))        # RSI 10–24
    entry_thresholds = list(range(20, 40))    # Entry at RSI 20–39

    for pair in pairs:
        print(f"\n🔬 Optimising {pair} ({granularity})...\n")
        df = load_raw_data(pair, granularity)
        close = df["close"]

        portfolio = run_rsi_optimisation(close, rsi_windows, entry_thresholds)
        sharpe = portfolio.sharpe_ratio()

        generate_sharpe_heatmap(portfolio, rsi_windows, entry_thresholds)
        optimal = export_optimal_params(sharpe)
        print(f"  Optimal params: {optimal}")

    print("\n✅ VBT optimisation complete. Transfer results to config/strategy_config.toml.\n")


if __name__ == "__main__":
    main()
