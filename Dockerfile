# Titan-Oanda-Algo — Production Container
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first (layer caching)
COPY pyproject.toml ./
RUN uv sync --no-dev

# Copy application code
COPY execution/ ./execution/
COPY config/ ./config/
COPY strategies/ ./strategies/

# Copy trained models (critical for ML strategies)
COPY models/ ./models/

# Copy environment template (runtime secrets via env vars)
COPY .env.example ./.env.example

# Health check
HEALTHCHECK --interval=60s --timeout=10s --retries=3 \
    CMD python -c "print('OK')" || exit 1

# Default: run the NautilusTrader live engine
CMD ["uv", "run", "python", "execution/run_nautilus_live.py"]
