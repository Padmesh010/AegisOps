# backend/Dockerfile
# Multi-stage production-ready Dockerfile for AegisOps FastAPI Backend

# --- Stage 1: Build & Dependencies Export ---
FROM python:3.13-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy package config files
COPY pyproject.toml README.md ./

# Export requirements to requirements.txt (including standard dependencies)
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

# --- Stage 2: Final Runtime ---
FROM python:3.13-slim AS runner

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from builder stage
COPY --from=builder /build/requirements.txt .

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Expose backend service port
EXPOSE 8000

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STAGE=production

# Run database migrations and boot FastAPI service
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
