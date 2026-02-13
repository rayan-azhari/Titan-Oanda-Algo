"""
run_live.py — Live / Paper trading engine.

Connects to OANDA, loads the trained model, generates signals in real-time,
and executes trades with risk management.

Directive: Live Deployment and Monitoring.md
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import tomllib
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

load_dotenv(PROJECT_ROOT / ".env")

import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.pricing as pricing

from rate_limiter import rate_limited_call, order_limiter, api_limiter

MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / ".tmp" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("OANDA_ACCESS_TOKEN")


def load_risk_config() -> dict:
    config_path = PROJECT_ROOT / "config" / "risk.toml"
    if not config_path.exists():
        print(f"ERROR: {config_path} not found. See directives/07_live_deployment.md")
        sys.exit(1)
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def find_latest_model() -> Path:
    models = sorted(MODELS_DIR.glob("*.joblib"))
    if not models:
        print("ERROR: No trained models found. Run train_model.py first.")
        sys.exit(1)
    return models[-1]


def setup_logging(mode: str) -> logging.Logger:
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    log_file = LOGS_DIR / f"live_{mode}_{date_str}.log"
    logger = logging.getLogger("titan")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    logger.addHandler(console)
    return logger


def main() -> None:
    parser = argparse.ArgumentParser(description="Live trading engine")
    parser.add_argument("--mode", choices=["practice", "live"], default="practice")
    args = parser.parse_args()

    logger = setup_logging(args.mode)
    risk_cfg = load_risk_config().get("risk", {})
    model_path = find_latest_model()
    model = joblib.load(model_path)

    environment = "practice" if args.mode == "practice" else "live"
    client = oandapyV20.API(access_token=ACCESS_TOKEN, environment=environment)

    logger.info("=" * 50)
    logger.info(f"  TITAN TRADING ENGINE — {args.mode.upper()}")
    logger.info(f"  Model: {model_path.name}")
    logger.info(f"  Max position: {risk_cfg.get('max_position_size_units', 'N/A')} units")
    logger.info(f"  Max daily loss: {risk_cfg.get('max_daily_loss_pct', 'N/A')}%")
    logger.info("=" * 50)

    # -----------------------------------------------------------------------
    # Main trading loop (placeholder — extend with real signal generation)
    # -----------------------------------------------------------------------
    logger.info("Entering main loop. Press Ctrl+C to stop.")
    logger.info(f"Rate limiter active: API={api_limiter.capacity}/s, "
                f"Orders={order_limiter.capacity}/s")
    try:
        while True:
            # TODO: Implement real-time signal generation
            # 1. Fetch latest candle(s) — use rate_limited_call(client.request, req)
            # 2. Build features
            # 3. model.predict(features) → signal
            # 4. Check risk limits
            # 5. Execute order — use rate_limited_call(
            #        client.request, order_req, limiter=order_limiter
            #    )
            logger.info("Heartbeat — engine running. (Signal generation not yet implemented)")
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Engine stopped by user.")

    logger.info("✅ Engine shut down cleanly.")


if __name__ == "__main__":
    main()
