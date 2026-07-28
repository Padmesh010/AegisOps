from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.infrastructure.db.session import get_db_session
from app.infrastructure.redis import redis_manager
from app.core.exceptions import DatabaseConnectionError, RedisConnectionError

router = APIRouter()

@router.get("/liveness")
async def liveness() -> dict:
    """Basic endpoint to verify the service is running."""
    return {"status": "alive"}

@router.get("/readiness")
async def readiness(
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """Verify backend has active connections to its database and cache."""
    # 1. DB Ping
    try:
        await db.execute(text("SELECT 1"))
    except Exception as err:
        raise DatabaseConnectionError(f"Database readiness check failed: {str(err)}")

    # 2. Redis Ping
    is_redis_healthy = await redis_manager.ping()
    if not is_redis_healthy:
        raise RedisConnectionError("Redis readiness check failed")

    return {
        "status": "ready",
        "components": {
            "database": "connected",
            "redis": "connected"
        }
    }
