# tests/api/test_main.py
import os
import pytest
from httpx import AsyncClient
from fastapi import status
from src.api.main import app

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    """
    Configura variables de entorno para tests (evitar conflictos con prod).
    """
    monkeypatch.setenv("SECRET_KEY", "testsecret")
    monkeypatch.setenv("OAUTH_CLIENT_ID", "fake-id")
    monkeypatch.setenv("OAUTH_CLIENT_SECRET", "fake-secret")
    # Usar SQLite en memoria para tests de DB (si tu app lee DATABASE_URL)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["msg"].startswith("Hola FastAPI")

@pytest.mark.asyncio
async def test_healthz():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_metrics_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/metrics")
    assert res.status_code == 200
    # Debe contener texto conforme Prometheus (counter, help, etc.)
    assert b"app_requests_total" in res.content

@pytest.mark.asyncio
async def test_dashboard_requires_auth():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/dashboard")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
