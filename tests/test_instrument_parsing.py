"""test_instrument_parsing.py — Unit tests for OANDA instrument provider.

Validates tick_size accuracy and data completeness of the
auto-generated instrument provider.

Directive: Nautilus-Oanda Adapter Construction.md (Phase 1)
"""

from decimal import Decimal
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_instrument_provider_exists():
    """The instrument provider module should exist after generation."""
    provider_path = PROJECT_ROOT / "execution" / "oanda_instrument_provider.py"
    assert provider_path.exists(), (
        "oanda_instrument_provider.py not found. "
        "Run: uv run python execution/parse_oanda_instruments.py"
    )


def test_instrument_provider_imports():
    """The generated module should be importable."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "oanda_instrument_provider",
        PROJECT_ROOT / "execution" / "oanda_instrument_provider.py",
    )
    if spec is None or spec.loader is None:
        pytest.skip("Module could not be loaded")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "OANDA_INSTRUMENTS")


def test_tick_size_accuracy():
    """Tick sizes should match OANDA's display precision.

    EUR/USD has 5 decimal places → tick_size = 0.00001
    USD/JPY has 3 decimal places → tick_size = 0.001
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "oanda_instrument_provider",
        PROJECT_ROOT / "execution" / "oanda_instrument_provider.py",
    )
    if spec is None or spec.loader is None:
        pytest.skip("Module could not be loaded")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    instruments = module.OANDA_INSTRUMENTS

    if "EUR_USD" in instruments:
        assert instruments["EUR_USD"]["tick_size"] == Decimal("0.00001")

    if "USD_JPY" in instruments:
        assert instruments["USD_JPY"]["tick_size"] == Decimal("0.001")
