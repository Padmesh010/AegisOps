import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.integration import DbIntegrationAccount, DbCloudResource, DbKubernetesCluster
from app.infrastructure.db.repositories.base import BaseRepository

class IntegrationAccountRepository(BaseRepository[DbIntegrationAccount]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbIntegrationAccount, session)

    async def get_by_provider(self, provider_type: str) -> List[DbIntegrationAccount]:
        result = await self.session.execute(
            select(self.model).where(self.model.provider_type == provider_type)
        )
        return list(result.scalars().all())

class CloudResourceRepository(BaseRepository[DbCloudResource]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbCloudResource, session)

    async def get_by_account_id(self, account_id: uuid.UUID) -> List[DbCloudResource]:
        result = await self.session.execute(
            select(self.model).where(self.model.account_id == account_id)
        )
        return list(result.scalars().all())

class KubernetesClusterRepository(BaseRepository[DbKubernetesCluster]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbKubernetesCluster, session)

    async def get_by_name(self, name: str) -> Optional[DbKubernetesCluster]:
        result = await self.session.execute(
            select(self.model).where(self.model.cluster_name == name)
        )
        return result.scalar_one_or_none()
