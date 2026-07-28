import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.dashboard import DbDashboard, DbWidget, DbUserPreference
from app.infrastructure.db.repositories.base import BaseRepository

class DashboardRepository(BaseRepository[DbDashboard]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbDashboard, session)

    async def get_by_owner_id(self, owner_id: uuid.UUID) -> List[DbDashboard]:
        result = await self.session.execute(
            select(self.model).where(self.model.owner_id == owner_id, self.model.is_deleted == False)  # type: ignore
        )
        return list(result.scalars().all())

class UserPreferenceRepository(BaseRepository[DbUserPreference]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbUserPreference, session)

    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[DbUserPreference]:
        result = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return result.scalar_one_or_none()
