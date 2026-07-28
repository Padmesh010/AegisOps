import uuid
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.incident import Incident
from app.infrastructure.db.models.agents import DbAgentApproval

class OfflineDeltaSyncService:
    async def get_offline_sync_delta(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """Aggregate active incident alerts and pending approvals into delta update objects for PWAs."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            # Get incidents
            res_inc = await session.execute(
                select(Incident).where(Incident.status != "resolved").limit(10)
            )
            incidents = res_inc.scalars().all()
            
            # Get approvals
            res_app = await session.execute(
                select(DbAgentApproval).where(DbAgentApproval.status == "pending").limit(5)
            )
            approvals = res_app.scalars().all()
            
            return {
                "user_id": str(user_id),
                "incidents": [
                    {"id": str(i.id), "title": i.title, "status": i.status, "severity": i.severity}
                    for i in incidents
                ],
                "pending_approvals": [
                    {"id": str(a.id), "action_type": a.action_type, "resource": a.target_resource}
                    for a in approvals
                ]
            }

# Global sync service instance
offline_sync_service = OfflineDeltaSyncService()
