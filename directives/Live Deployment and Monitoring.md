# Directive: Live Deployment and Monitoring

## Goal

Containerise the Nautilus system and deploy it to a low-latency **Google Compute Engine (GCE)** instance.

## Pre-Flight Checklist

> [!CAUTION]
> **All items must pass before deployment.**

- [ ] `config/risk.toml` reviewed — max drawdown, position limits, daily loss cap
- [ ] `execution/kill_switch.py` tested on practice account
- [ ] OOS Sharpe ≥ 50% of IS Sharpe (from VBT optimisation)
- [ ] Model Sharpe ≥ 1.5 (from `train_ml_model.py`)
- [ ] `execution/validate_data.py` passed on latest data

## Execution Steps

### 1. Containerisation

- **DevOps Agent** runs `execution/build_docker_image.py`.
- Base: `python:3.11-slim` with `nautilus_trader` wheel.

> [!IMPORTANT]
> **Critical:** Copy the `models/` directory into the container if an ML strategy is active.

### 2. Infrastructure

- Deploy to `europe-west2` (London) for OANDA proximity.
- Use `e2-standard-2` instance type.

### 3. Headless Monitoring (The Guardian)

- Initialise "Guardian" agent in headless mode.
- **Task:** SSH log monitoring for `"ERROR"` strings.
- **Notification:** Trigger Slack alert on failure via `execution/send_notification.py`.

## Success Criteria

- System running in container on GCE.
- Guardian agent active and reporting heartbeat.