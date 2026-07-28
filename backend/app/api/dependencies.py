import logging
from typing import AsyncGenerator, Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings, Settings
from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.core.security import decode_token
from app.infrastructure.db.session import get_db_session
from app.infrastructure.redis import get_redis_client
from app.infrastructure.db.models.user import User
from app.infrastructure.db.repositories.user import UserRepository

logger = logging.getLogger("app.api.dependencies")
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)

async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    token: Optional[str] = Depends(oauth2_scheme),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
) -> User:
    """Authenticate requests using either OAuth2 JWT bearer tokens or API key headers."""
    # 1. API Key Authentication (Service accounts / CLI)
    if x_api_key:
        import hashlib
        from app.infrastructure.db.repositories.user import APIKeyRepository
        
        # Parse key_prefix and actual key value
        if ":" not in x_api_key:
            raise AuthenticationError("Malformed API Key format (prefix:key expected)")
        prefix, key_val = x_api_key.split(":", 1)
        hashed_val = hashlib.sha256(x_api_key.encode()).hexdigest()
        
        key_repo = APIKeyRepository(db)
        key_record = await key_repo.get_by_hashed_key(hashed_val)
        if not key_record or key_record.is_revoked:
            raise AuthenticationError("API Key has been revoked or is invalid")
        
        if key_record.expires_at and key_record.expires_at < datetime.now(timezone.utc):
            raise AuthenticationError("API Key has expired")
            
        return key_record.user

    # 2. JWT Bearer Token Authentication (Browser clients)
    if not token:
        raise AuthenticationError("Authorization header is missing")
        
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Malformed authentication token signature")
            
        user_repo = UserRepository(db)
        user = await user_repo.get(user_id)
        if not user or user.is_deleted:
            raise AuthenticationError("Authenticated user does not exist")
            
        return user
    except Exception as err:
        if isinstance(err, AuthenticationError):
            raise err
        raise AuthenticationError("Invalid authorization token")

class RequirePermission:
    """Authorization decorator checking if the user owns roles possessing target permission."""
    def __init__(self, required_permission: str) -> None:
        self.required_permission = required_permission

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_permissions = []
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.append(perm.name)
                
        # Admins bypass specific permission scopes checks
        if "admin" in user_permissions or self.required_permission in user_permissions:
            return current_user
            
        raise PermissionDeniedError(f"Operation requires permission scope: {self.required_permission}")
