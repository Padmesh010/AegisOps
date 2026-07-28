from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.ai import DbAIProvider
from app.infrastructure.db.repositories.base import BaseRepository

class AIProviderRepository(BaseRepository[DbAIProvider]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbAIProvider, session)

    async def get_by_name(self, name: str) -> Optional[DbAIProvider]:
        """Fetch an AI provider configuration entity by name."""
        result = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalar_one_or_none()
