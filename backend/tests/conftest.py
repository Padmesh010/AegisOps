import asyncio
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
# Define isolated SQLite memory engine for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Mock Redis Client
class MockRedis:
    def __init__(self) -> None:
        self.store = {}

    async def get(self, key: str) -> Optional[str]:
        return self.store.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        self.store[key] = str(value)
        return True

    async def ping(self) -> bool:
        return True

    async def close(self) -> None:
        pass

# Apply dynamic override immediately before loading other packages
import app.infrastructure.db.session as session_module
session_module.TestingSessionLocal = TestingSessionLocal

import app.infrastructure.redis as redis_module
redis_module.redis_manager = MockRedis()

from app.main import app
from app.core.config import get_settings
from app.infrastructure.db.models.base import BaseModel
from app.api.dependencies import get_db_session, get_redis_client

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    """Auto-initialize database tables in memory prior to running tests."""
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a transactional async DB session, rolling back after test execution."""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()



@pytest.fixture
def mock_redis() -> MockRedis:
    return MockRedis()

@pytest_asyncio.fixture(autouse=True)
async def override_dependencies(db_session: AsyncSession, mock_redis: MockRedis) -> None:
    """Apply FastAPI overrides injecting local DB/Redis fixtures."""
    import app.infrastructure.db.session as session_module
    session_module.TestingSessionLocal = TestingSessionLocal
    import app.infrastructure.redis as redis_module
    redis_module.redis_manager = mock_redis
    app.dependency_overrides[get_db_session] = lambda: db_session
    app.dependency_overrides[get_redis_client] = lambda: mock_redis
    yield
    app.dependency_overrides.clear()

import httpx

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Yield an HTTPX AsyncClient targeting the configured FastAPI application instance."""
    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac

from typing import Optional
