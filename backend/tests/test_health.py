import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_liveness_endpoint(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

@pytest.mark.anyio
async def test_readiness_endpoint(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/readiness")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "components": {
            "database": "connected",
            "redis": "connected"
        }
    }
