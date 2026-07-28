import logging
from typing import Optional
import redis.asyncio as aioredis
from app.core.config import get_settings

logger = logging.getLogger("app.redis")
settings = get_settings()

class RedisManager:
    def __init__(self) -> None:
        self.client: Optional[aioredis.Redis] = None

    def connect(self) -> None:
        """Initialize Redis connection client."""
        if not self.client:
            logger.info("Initializing Redis connection pool...")
            self.client = aioredis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_timeout=5.0,
                socket_connect_timeout=5.0
            )

    async def disconnect(self) -> None:
        """Close Redis connection pool."""
        if self.client:
            logger.info("Closing Redis connection pool...")
            await self.client.close()
            self.client = None

    async def ping(self) -> bool:
        """Check if Redis connection is active."""
        if not self.client:
            return False
        try:
            return await self.client.ping()
        except Exception as err:
            logger.error(f"Redis ping failure: {str(err)}")
            return False

# Global Singleton Manager
redis_manager = RedisManager()

async def get_redis_client() -> aioredis.Redis:
    """Dependency provider yielding active Redis connection."""
    if not redis_manager.client:
        redis_manager.connect()
    return redis_manager.client
