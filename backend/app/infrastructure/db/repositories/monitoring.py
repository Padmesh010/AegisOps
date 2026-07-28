import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.monitoring import Cluster, Node
from app.infrastructure.db.models.metric import DbMetricSnapshot, DbAlertThreshold
from app.infrastructure.db.repositories.base import BaseRepository

class ClusterRepository(BaseRepository[Cluster]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Cluster, session)

    async def get_by_name(self, name: str) -> Optional[Cluster]:
        result = await self.session.execute(
            select(self.model).where(self.model.name == name, self.model.is_deleted == False)  # type: ignore
        )
        return result.scalar_one_or_none()

class NodeRepository(BaseRepository[Node]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Node, session)

    async def get_by_cluster_id(self, cluster_id: uuid.UUID) -> List[Node]:
        result = await self.session.execute(
            select(self.model).where(self.model.cluster_id == cluster_id, self.model.is_deleted == False)  # type: ignore
        )
        return list(result.scalars().all())

class MetricSnapshotRepository(BaseRepository[DbMetricSnapshot]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbMetricSnapshot, session)

    async def get_latest_for_target(self, target_id: str, metric_id: uuid.UUID) -> Optional[DbMetricSnapshot]:
        result = await self.session.execute(
            select(self.model)
            .where(self.model.target_id == target_id, self.model.metric_id == metric_id)
            .order_by(self.model.timestamp.desc())  # type: ignore
            .limit(1)
        )
        return result.scalar_one_or_none()

class AlertThresholdRepository(BaseRepository[DbAlertThreshold]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DbAlertThreshold, session)

    async def get_by_metric_name(self, metric_name: str) -> Optional[DbAlertThreshold]:
        result = await self.session.execute(
            select(self.model).where(self.model.metric_name == metric_name)
        )
        return result.scalar_one_or_none()
