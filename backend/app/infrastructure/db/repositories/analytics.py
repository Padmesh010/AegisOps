import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.analytics import DbSLADefinition, DbSLOObjective, DbKPIValue
from app.infrastructure.db.repositories.base import BaseRepository

class SLADefinitionRepository(BaseRepository[DbSLADefinition]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbSLADefinition, session)

    async def get_by_service_name(self, service_name: str) -> Optional[DbSLADefinition]:
        result = await self.session.execute(
            select(self.model).where(self.model.service_name == service_name)
        )
        return result.scalar_one_or_none()

class KPIRepository(BaseRepository[DbKPIValue]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbKPIValue, session)

    async def get_by_kpi_name(self, kpi_name: str) -> List[DbKPIValue]:
        result = await self.session.execute(
            select(self.model).where(self.model.kpi_name == kpi_name).order_by(self.model.timestamp.desc())  # type: ignore
        )
        return list(result.scalars().all())
