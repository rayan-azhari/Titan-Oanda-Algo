# Titan-Oanda-Algo Project Audit Report

**Date:** 2026-02-16
**Auditor:** Antigravity

## 1. Executive Summary

The **Titan-Oanda-Algo** project is a well-structured algorithmic trading system leveraging modern Python tooling (`uv`, `ruff`, `pandas`, `vectorbt`, `nautilus_trader`). The architecture clearly separates research/strategy (`strategies/`), data (`data/`), and execution (`execution/`).

**Overall Health:** 🟢 **Good**
The codebase is clean, documented, and follows modern practices. However, there are **critical architecture gaps** in the live execution adapter regarding state persistence (reconciliation) and a lack of integration testing for the core strategy logic.

---

## 2. Critical Risks & Gaps

### ✅ 1. ~~Incomplete NautilusTrader Adapter~~ — **RESOLVED** (2026-02-16)

> **Status:** `generate_position_status_reports` has been implemented. On startup, the engine now
> fetches open positions from OANDA's `OpenPositions` endpoint, computes net direction (`PositionSide.LONG`/`SHORT`),
> and generates `PositionStatusReport` objects for the reconciliation engine.
>
> **Remaining stub:** `generate_fill_reports` still returns empty. This is lower risk as position-level
> reconciliation (now implemented) handles the primary desync scenario.
>
> **Tests:** 6 unit tests in `tests/test_oanda_reconciliation.py` — all passing.

### ✅ 1b. ~~Data Client Streaming Broken~~ — **RESOLVED** (2026-02-16)

> **Status:** The `OandaDataClient` had 4 bugs preventing live data from flowing:
> 1. Subscribe methods were `async def` but Nautilus calls them synchronously → coroutines never awaited.
> 2. Used `self._connected` instead of `self.is_connected` (base class property).
> 3. `Price(precision=None)` — Nautilus requires an integer → derived from OANDA price string.
> 4. `self._msgbus.publish_data()` doesn't exist → replaced with `self._handle_data_py()`.
>
> All subscribe methods now use correct `(self, command)` signatures matching the Nautilus base class API.

### ⚠️ 2. Lack of Integration Tests
While there are unit tests for parsing and mock tests for the ML strategy class, there are **no signals or integration tests** for the core logic in `execution/mtf_confluence.py` or the full end-to-end pipeline.
**Impact:** Logic errors in the "best performing strategy" (MTF Confluence) may go undetected until live trading.

---

## 3. Architecture & Code Quality

### 🟢 Strengths
-   **Dependency Management:** Excellent usage of `uv` and `pyproject.toml`.
-   **Linting:** `ruff` configuration is solid. Code is generally PEP8 compliant.
-   **Documentation:** `README.md` and `USER_GUIDE.md` are exemplary—clear, comprehensive, and beginner-friendly.
-   **Type Hinting:** Widespread use of type hints improves readability and safety.

### 🟠 Areas for Improvement
-   **Script-Heavy Structure:** The `execution/` directory is cluttered with 13+ `run_*.py` scripts.
    -   *Recommendation:* Move entry-point scripts to a `scripts/` directory and keep `execution/` as a proper Python package (e.g., `src/titan/execution`).
-   **Runtime Path Manipulation:**
    -   Files like `mtf_confluence.py` and tests use `sys.path.insert(0, str(PROJECT_ROOT))`.
    -   *Recommendation:* Install the project in editable mode (`uv pip install -e .`) and use absolute imports (e.g., `from titan.execution import ...`) instead of hacking `sys.path`.
-   **Hardcoded Paths:**
    -   `PROJECT_ROOT = Path(__file__).resolve().parent.parent` assumes a rigid directory structure.

---

## 4. Security Audit

-   **Secrets:** No hardcoded passwords or tokens were found in the codebase.
-   **Env Handling:** Correctly using `.env` and `python-dotenv`.
-   **Gitignore:** Properly identifying sensitive files (`.env`, `data/`, `models/`, `logs/`).
-   **Verification File:** `verify_conn.txt` was checked and found to contain error logs, not leaked secrets.

---

## 5. Next Steps Plan

ID | Priority | Task | Description
---|---|---|---
1 | ~~**High**~~ ✅ | ~~**Fix Adapter Reconciliation**~~ | ✅ Implemented `generate_position_status_reports` — positions synced on startup (2026-02-16).
2 | **Medium** | **Add Strategy Tests** | Create tests for `mtf_confluence.py` using fixed data inputs (CSV/Parquet) to verify signal logic without mocks.
3 | **Low** | **Refactor Directory** | Move `run_*.py` scripts to `scripts/` and formalize the package structure.
4 | **Low** | **CI/CD Expansion** | Add a simple end-to-end "dry run" test in CI to ensure key scripts don't crash on start.

