# Directive: Nautilus-Oanda Adapter Construction

## Goal

Build a high-performance, deterministic `nautilus_oanda` adapter package using a **hybrid wrapper approach**.

## Inputs

- OANDA v20 API Specification
- `oandapyV20` library documentation
- NautilusTrader `adapter_guide.md`

## Execution Steps

### Phase 1 — Instrumentation

- Call `execution/parse_oanda_instruments.py` to generate `oanda_instrument_provider.py`.
- **Validation:** Run `tests/test_instrument_parsing.py` to assert `tick_size` accuracy.

### Phase 2 — Streaming Data

- Implement `OandaDataClient` by wrapping the official `oandapyV20` streaming endpoints.

> [!IMPORTANT]
> **Constraint:** Do not implement raw `aiohttp` requests. Use the official library for connection handling, but map the output to Nautilus `QuoteTick`.

- Ensure exponential backoff logic is preserved for network resilience.

### Phase 3 — Execution Logic

- Implement `OandaExecutionClient`.
- Map `order.client_order_id` → OANDA's `clientExtensions.id`.

## Success Criteria

- Successful connection to OANDA streaming API via the `oandapyV20` wrapper.
- 100% pass rate on unit tests for instrument parsing and order mapping.