import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.user import Role, Permission
from app.core.security import get_password_hash

@pytest.mark.anyio
async def test_user_registration_and_login_flow(client: AsyncClient, db_session: AsyncSession) -> None:
    # 1. Register User
    reg_payload = {
        "email": "user_flow@aegisops.io",
        "username": "flowuser",
        "password": "verysecurepassword123"
    }
    reg_response = await client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_response.status_code == 201
    assert reg_response.json()["email"] == "user_flow@aegisops.io"
    
    # 2. Login User
    login_payload = {
        "username": "flowuser",
        "password": "verysecurepassword123"
    }
    login_response = await client.post(
        "/api/v1/auth/login",
        data=login_payload
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    
    # 3. Get Current User Details
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_response = await client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "flowuser"

@pytest.mark.anyio
async def test_permission_authorization_decorations(client: AsyncClient, db_session: AsyncSession) -> None:
    # 1. Create a dummy user
    hashed = get_password_hash("authpass123")
    from app.infrastructure.db.models.user import User
    test_user = User(
        email="scoped@aegisops.io",
        username="scopeduser",
        hashed_password=hashed
    )
    db_session.add(test_user)
    await db_session.flush()
    
    # 2. Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "scopeduser", "password": "authpass123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Attempt to query admin users list (Should raise 403 Forbidden since user has no roles/permissions)
    admin_response = await client.get("/api/v1/admin/users", headers=headers)
    assert admin_response.status_code == 403
    assert admin_response.json()["error"]["code"] == "PERMISSION_DENIED"
