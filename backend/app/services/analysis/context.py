import uuid
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.incident import Incident
from app.infrastructure.db.models.metric import DbMetricSnapshot

class ContextBuilder:
    async def build_investigation_context(self, incident_id: uuid.UUID) -> Dict[str, Any]:
        """Aggregate incident parameters, system metrics trends and timeline events for prompt mapping."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            # 1. Pull Incident
            res = await session.execute(select(Incident).where(Incident.id == incident_id))
            incident = res.scalar_one_or_none()
            if not incident:
                return {}

            # 2. Pull Metric Snapshots (historical trends)
            metric_res = await session.execute(
                select(DbMetricSnapshot)
                .order_by(DbMetricSnapshot.timestamp.desc())  # type: ignore
                .limit(20)
            )
            snapshots = metric_res.scalars().all()
            
            # 3. Pull Timeline events logs
            events_data = [{"type": e.event_type, "msg": e.message} for e in incident.events]

            return {
                "incident": {
                    "id": str(incident.id),
                    "title": incident.title,
                    "severity": incident.severity,
                    "description": incident.description,
                    "created_at": incident.created_at.isoformat() if incident.created_at else None
                },
                "telemetry": [
                    {
                        "metric_id": str(s.metric_id),
                        "target": s.target_id,
                        "value": s.value,
                        "time": s.timestamp.isoformat()
                    } for s in snapshots
                ],
                "timeline": events_data,
                "environment": "production",
                "cluster_details": "EKS Cluster: aegisops-prod-us-east-1"
            }

# Global builder instance
context_builder = ContextBuilder()
