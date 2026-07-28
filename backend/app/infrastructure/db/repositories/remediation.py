import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.remediation import RemediationPolicy, RemediationPlan, RemediationStep, RemediationApproval
from app.infrastructure.db.repositories.base import BaseRepository

class RemediationPolicyRepository(BaseRepository[RemediationPolicy]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RemediationPolicy, session)

    async def get_by_metric(self, metric_name: str) -> List[RemediationPolicy]:
        result = await self.session.execute(
            select(self.model).where(self.model.target_metric == metric_name, self.model.is_active == True)
        )
        return list(result.scalars().all())

class RemediationPlanRepository(BaseRepository[RemediationPlan]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RemediationPlan, session)

    async def get_by_incident_id(self, incident_id: uuid.UUID) -> Optional[RemediationPlan]:
        result = await self.session.execute(
            select(self.model).where(self.model.incident_id == incident_id)
        )
        return result.scalar_one_or_none()

class RemediationApprovalRepository(BaseRepository[RemediationApproval]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RemediationApproval, session)

    async def get_by_plan_id(self, plan_id: uuid.UUID) -> List[RemediationApproval]:
        result = await self.session.execute(
            select(self.model).where(self.model.plan_id == plan_id)
        )
        return list(result.scalars().all())
