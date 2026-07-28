import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.notification import NotificationChannel, DbNotificationHistory, DbEscalationPolicy, DbWorkflowDefinition
from app.infrastructure.db.repositories.base import BaseRepository

class NotificationChannelRepository(BaseRepository[NotificationChannel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(NotificationChannel, session)

    async def get_by_name(self, name: str) -> Optional[NotificationChannel]:
        result = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalar_one_or_none()

class WorkflowDefinitionRepository(BaseRepository[DbWorkflowDefinition]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbWorkflowDefinition, session)

    async def get_active_workflows(self) -> List[DbWorkflowDefinition]:
        result = await self.session.execute(
            select(self.model).where(self.model.is_active == True)
        )
        return list(result.scalars().all())
