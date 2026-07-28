import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.generation import DbArtifactTemplate, DbGeneratedArtifact, DbGenerationHistory
from app.infrastructure.db.repositories.base import BaseRepository

class ArtifactTemplateRepository(BaseRepository[DbArtifactTemplate]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbArtifactTemplate, session)

    async def get_by_name(self, name: str) -> Optional[DbArtifactTemplate]:
        result = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalar_one_or_none()

class GeneratedArtifactRepository(BaseRepository[DbGeneratedArtifact]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbGeneratedArtifact, session)

    async def get_by_user_id(self, user_id: uuid.UUID) -> List[DbGeneratedArtifact]:
        result = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return list(result.scalars().all())
