import asyncio
import os
from typing import Dict, List
from fastapi import FastAPI, Response, status

app = FastAPI(
    title="CI Security & Load-Testing Quality Gate Demo API",
    description="Production-grade lightweight microservice designed for automated shift-left security and performance gates.",
    version="1.0.0",
)

# In-memory mock data
CATALOG_ITEMS = [
    {"id": 1, "name": "CloudWatch Logs Agent", "category": "Observability", "status": "active"},
    {"id": 2, "name": "ECR Image Scanner", "category": "Security", "status": "active"},
    {"id": 3, "name": "Autocannon Quality Gate", "category": "Performance", "status": "active"},
    {"id": 4, "name": "Fargate Task Controller", "category": "Compute", "status": "active"},
    {"id": 5, "name": "Trivy Vulnerability Filter", "category": "Security", "status": "active"},
    {"id": 6, "name": "Grafana Dashboard", "category": "Observability", "status": "active"},
]


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoring"])
async def health_check() -> Dict[str, str]:
    """
    Health check probe for ECS target groups, Kubernetes, and CI container readiness.
    Guaranteed zero-latency response for infrastructure health verifications.
    """
    return {"status": "ok"}


@app.get("/items", status_code=status.HTTP_200_OK, tags=["Catalog"])
async def get_items() -> List[Dict[str, str | int]]:
    """
    Retrieve service catalog items.
    Supports SIMULATE_DELAY_MS environment variable to intentionally inject
    artificial latency for testing CI/CD performance quality gates.
    """
    delay_ms_str = os.getenv("SIMULATE_DELAY_MS", "0")
    try:
        delay_ms = float(delay_ms_str)
    except ValueError:
        delay_ms = 0.0

    if delay_ms > 0:
        await asyncio.sleep(delay_ms / 1000.0)

    return CATALOG_ITEMS
