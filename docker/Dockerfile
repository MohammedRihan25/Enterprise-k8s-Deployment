# ==========================================
# Stage 1: Builder (Compile dependencies)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Install only production dependencies into portable wheel archives
COPY app/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels Flask==3.0.3 gunicorn==22.0.0

# ==========================================
# Stage 2: Production Runtime (Lean & Secure)
# ==========================================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Create a non-root group and user for security hardening
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# Copy pre-built wheels from Stage 1 and install them without internet or cache
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application code and set ownership to non-root user
COPY --chown=appuser:appgroup app/main.py .

# Switch from root to the restricted non-root user
USER appuser

EXPOSE 5000

# Built-in container health check hitting our /health endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
