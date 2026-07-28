import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.incident import Incident, IncidentEvent
from app.infrastructure.db.repositories.base import BaseRepository

class IncidentRepository(BaseRepository[Incident]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Incident, session)

    async def get_active_incidents(self) -> List[Incident]:
        result = await self.session.execute(
            select(self.model).where(self.model.status != "resolved", self.model.is_deleted == False)  # type: ignore
        )
        return list(result.scalars().all())

class IncidentEventRepository(BaseRepository[IncidentEvent]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(IncidentEvent, session)

    async def get_by_incident_id(self, incident_id: uuid.UUID) -> List[IncidentEvent]:
        result = await self.session.execute(
            select(self.model).where(self.model.incident_id == incident_id)
        )
        return list(result.scalars().all())
