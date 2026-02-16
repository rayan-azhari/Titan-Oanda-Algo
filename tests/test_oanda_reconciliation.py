"""test_oanda_reconciliation.py — Tests for OANDA position reconciliation.

Validates that generate_position_status_reports correctly fetches and parses
open positions from the OANDA V20 API into Nautilus PositionStatusReport objects.
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add project root to path so we can import 'execution' package
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from nautilus_trader.common.providers import InstrumentProvider
from nautilus_trader.model.enums import AccountType, OmsType, PositionSide
from nautilus_trader.model.identifiers import ClientId, Venue
from nautilus_trader.model.objects import Currency
from nautilus_trader.test_kit.stubs.component import TestComponentStubs

from execution.nautilus_oanda.config import OandaExecutionClientConfig
from execution.nautilus_oanda.execution import OandaExecutionClient


def _make_client():
    """Create a test OandaExecutionClient with mocked OANDA API."""
    loop = asyncio.new_event_loop()

    config = OandaExecutionClientConfig(
        account_id="101-001-1234567-001",
        access_token="fake-token",
        environment="practice",
    )

    clock = TestComponentStubs.clock()
    msgbus = TestComponentStubs.msgbus()
    cache = TestComponentStubs.cache()

    client = OandaExecutionClient(
        loop=loop,
        client_id=ClientId("TEST_CLIENT"),
        venue=Venue("OANDA"),
        oms_type=OmsType.HEDGING,
        account_type=AccountType.MARGIN,
        base_currency=Currency.from_str("USD"),
        instrument_provider=MagicMock(spec=InstrumentProvider),
        config=config,
        msgbus=msgbus,
        cache=cache,
        clock=clock,
    )

    # Mock the internal OANDA API client so no real HTTP calls are made.
    # run_in_executor uses the real thread pool, but the lambda it executes
    # calls _api.request() which is now a MagicMock — so it just returns
    # the configured return_value instantly.
    client._api = MagicMock()

    return client, loop


def test_long_position():
    """Long position should produce a report with LONG side and correct qty."""
    client, loop = _make_client()
    client._api.request.return_value = {
        "positions": [
            {
                "instrument": "EUR_USD",
                "long": {"units": "1000", "averagePrice": "1.1050"},
                "short": {"units": "0", "averagePrice": "0.0000"},
            }
        ]
    }
    reports = loop.run_until_complete(
        client.generate_position_status_reports(command=None)
    )
    assert len(reports) == 1
    assert reports[0].instrument_id.symbol.value == "EUR/USD"
    assert reports[0].position_side == PositionSide.LONG
    assert reports[0].quantity.as_double() == 1000.0
    loop.close()


def test_short_position():
    """Short position (negative units in V20) should produce LONG=0, SHORT=-500 → net SHORT."""
    client, loop = _make_client()
    client._api.request.return_value = {
        "positions": [
            {
                "instrument": "GBP_USD",
                "long": {"units": "0", "averagePrice": "0.0000"},
                "short": {"units": "-500", "averagePrice": "1.2500"},
            }
        ]
    }
    reports = loop.run_until_complete(
        client.generate_position_status_reports(command=None)
    )
    assert len(reports) == 1
    assert reports[0].instrument_id.symbol.value == "GBP/USD"
    assert reports[0].position_side == PositionSide.SHORT
    assert reports[0].quantity.as_double() == 500.0
    loop.close()


def test_net_position():
    """When both long and short exist, report the net direction and qty."""
    client, loop = _make_client()
    client._api.request.return_value = {
        "positions": [
            {
                "instrument": "USD_JPY",
                "long": {"units": "1000", "averagePrice": "145.00"},
                "short": {"units": "-1500", "averagePrice": "146.00"},
            }
        ]
    }
    reports = loop.run_until_complete(
        client.generate_position_status_reports(command=None)
    )
    assert len(reports) == 1
    assert reports[0].instrument_id.symbol.value == "USD/JPY"
    assert reports[0].position_side == PositionSide.SHORT
    assert reports[0].quantity.as_double() == 500.0
    loop.close()


def test_empty_positions():
    """No open positions should return an empty list."""
    client, loop = _make_client()
    client._api.request.return_value = {"positions": []}
    reports = loop.run_until_complete(
        client.generate_position_status_reports(command=None)
    )
    assert len(reports) == 0
    loop.close()


def test_flat_position_skipped():
    """A position with net_units == 0 should be skipped."""
    client, loop = _make_client()
    client._api.request.return_value = {
        "positions": [
            {
                "instrument": "AUD_USD",
                "long": {"units": "500", "averagePrice": "0.6500"},
                "short": {"units": "-500", "averagePrice": "0.6510"},
            }
        ]
    }
    reports = loop.run_until_complete(
        client.generate_position_status_reports(command=None)
    )
    assert len(reports) == 0
    loop.close()


def test_api_error_returns_empty():
    """API errors should be caught gracefully, returning empty list."""
    client, loop = _make_client()
    client._api.request.side_effect = Exception("Connection failed")
    reports = loop.run_until_complete(
        client.generate_position_status_reports(command=None)
    )
    assert len(reports) == 0
    loop.close()
