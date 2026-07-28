from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.user import User, APIKey
from app.infrastructure.db.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a single user record by their unique email address."""
        result = await self.session.execute(
            select(self.model).where(self.model.email == email, self.model.is_deleted == False)  # type: ignore
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Fetch a single user record by their unique username string."""
        result = await self.session.execute(
            select(self.model).where(self.model.username == username, self.model.is_deleted == False)  # type: ignore
        )
        return result.scalar_one_or_none()

class APIKeyRepository(BaseRepository[APIKey]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(APIKey, session)

    async def get_by_hashed_key(self, hashed_key: str) -> Optional[APIKey]:
        """Fetch an active API key record matching the hashed key signature."""
        result = await self.session.execute(
            select(self.model).where(
                self.model.hashed_key == hashed_key,
                self.model.is_revoked == False
            )
        )
        return result.scalar_one_or_none()
