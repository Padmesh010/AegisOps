import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.analysis import InvestigationHistory, Recommendation
from app.infrastructure.db.repositories.base import BaseRepository

class InvestigationRepository(BaseRepository[InvestigationHistory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(InvestigationHistory, session)

    async def get_by_incident_id(self, incident_id: uuid.UUID) -> List[InvestigationHistory]:
        result = await self.session.execute(
            select(self.model).where(self.model.incident_id == incident_id)
        )
        return list(result.scalars().all())

class RecommendationRepository(BaseRepository[Recommendation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Recommendation, session)

    async def get_by_investigation_id(self, investigation_id: uuid.UUID) -> List[Recommendation]:
        result = await self.session.execute(
            select(self.model).where(self.model.investigation_id == investigation_id)
        )
        return list(result.scalars().all())
