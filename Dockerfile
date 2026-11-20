FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered standard I/O for CloudWatch/stdout logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install dependencies in a single layer with no cache
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && groupadd -r appgroup --gid 10001 \
    && useradd -r -g appgroup --uid 10001 --no-create-home appuser

# Copy application source code
COPY app /app/app

# Ensure proper permissions for unprivileged user
RUN chown -R appuser:appgroup /app

# Switch to non-root user (Security Best Practice for CIS/Trivy benchmarks)
USER appuser

EXPOSE 8000

# Built-in lightweight health check using Python standard library (no curl package needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Launch production ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
