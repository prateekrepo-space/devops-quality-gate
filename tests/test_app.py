import os
import pytest
from fastapi.testclient import TestClient
from app.main import app, CATALOG_ITEMS

client = TestClient(app)


def test_health_check_returns_200():
    """Verify health probe responds with HTTP 200 and status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_items_default_latency():
    """Verify /items responds with HTTP 200 and valid catalog payload."""
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(CATALOG_ITEMS)
    assert data[0]["name"] == "CloudWatch Logs Agent"


def test_get_items_with_simulated_delay(monkeypatch):
    """Verify /items respects SIMULATE_DELAY_MS environment override."""
    monkeypatch.setenv("SIMULATE_DELAY_MS", "50")
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == len(CATALOG_ITEMS)


def test_get_items_with_invalid_delay_env(monkeypatch):
    """Verify /items falls back gracefully to 0ms if SIMULATE_DELAY_MS is non-numeric."""
    monkeypatch.setenv("SIMULATE_DELAY_MS", "invalid_value")
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == len(CATALOG_ITEMS)
