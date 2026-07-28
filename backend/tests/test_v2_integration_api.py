import pytest
import uuid
import httpx
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def authenticated_headers(client: httpx.AsyncClient, db_session: AsyncSession) -> dict:
    """Helper fixture to register a test user, log in, and return JWT authorization headers."""
    email = f"test_v2_{uuid.uuid4().hex}@aegisops.io"
    username = f"user_{uuid.uuid4().hex[:10]}"
    
    # 1. Register
    reg_res = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": "securepassword123"}
    )
    assert reg_res.status_code == 201

    # 2. Login
    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": "securepassword123"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.anyio
async def test_v2_api_endpoints_health_check(client: httpx.AsyncClient):
    """Verify liveness check behaves cleanly."""
    res = await client.get("/api/v1/health/liveness")
    assert res.status_code == 200
    assert res.json()["status"] == "alive"

@pytest.mark.anyio
async def test_aiops_routes(client: httpx.AsyncClient, authenticated_headers: dict):
    # 1. Anomaly detection
    res = await client.post(
        "/api/v1/aiops/anomaly/detect?metric_name=cpu&strategy=zscore",
        json=[10.0, 12.0, 11.0, 13.0, 95.0],
        headers=authenticated_headers
    )
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # 2. Health score
    res = await client.get(
        "/api/v1/aiops/health/scores?scope_type=cluster&scope_id=prod-1",
        headers=authenticated_headers
    )
    assert res.status_code == 200
    assert "health_score" in res.json()

@pytest.mark.anyio
async def test_rag_routes(client: httpx.AsyncClient, authenticated_headers: dict):
    # 1. Knowledge search
    res = await client.post(
        "/api/v1/rag/knowledge/search?query=cpu",
        headers=authenticated_headers
    )
    assert res.status_code == 200
    assert "context" in res.json()

@pytest.mark.anyio
async def test_finops_routes(client: httpx.AsyncClient, authenticated_headers: dict):
    # 1. Rightsizing recommendations
    res = await client.get(
        "/api/v1/finops/rightsizing/recommendations",
        headers=authenticated_headers
    )
    assert res.status_code == 200
    assert isinstance(res.json(), list)

@pytest.mark.anyio
async def test_governance_routes(client: httpx.AsyncClient, authenticated_headers: dict):
    # 1. Policy check evaluation
    res = await client.post(
        "/api/v1/governance/policies/evaluate?action_name=scale_down&resource_id=i-123",
        json={"tags": {"env": "prod"}},
        headers=authenticated_headers
    )
    assert res.status_code == 200
    assert "allowed_execution" in res.json()

@pytest.mark.anyio
async def test_mlops_routes(client: httpx.AsyncClient, authenticated_headers: dict):
    # 1. Prompt template format
    res = await client.post(
        "/api/v1/mlops/prompts/test-key/format",
        json={"service": "frontend", "count": 2},
        params={"template_str": "Scaling {{service}} replicas to {{count}}."},
        headers=authenticated_headers
    )
    assert res.status_code == 200
    assert "formatted_prompt" in res.json()
    assert "frontend" in res.json()["formatted_prompt"]

@pytest.mark.anyio
async def test_lts_routes(client: httpx.AsyncClient, authenticated_headers: dict):
    # 1. Diagnostics bundle zip file retrieval
    res = await client.get(
        "/api/v1/lts/diagnostics/bundle",
        headers=authenticated_headers
    )
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/zip"
