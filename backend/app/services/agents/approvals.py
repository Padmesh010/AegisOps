import uuid
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.agents import DbAgentApproval

class AgentApprovalManager:
    async def request_action_approval(
        self,
        session_id: uuid.UUID,
        action_type: str,
        target_resource: str,
        params: dict
    ) -> DbAgentApproval:
        """Create a pending human-in-the-loop approval ticket for high-risk actions."""
        # Calculate mock risk score
        risk = 10.0
        if "delete" in action_type.lower() or "terminate" in action_type.lower():
            risk = 90.0
        elif "restart" in action_type.lower() or "scale" in action_type.lower():
            risk = 45.0
            
        async with TestingSessionLocal() as session:
            approval = DbAgentApproval(
                session_id=session_id,
                action_type=action_type,
                target_resource=target_resource,
                parameters_json=params,
                risk_score=risk,
                status="pending"
            )
            session.add(approval)
            await session.commit()
            return approval

    async def cast_approval_decision(self, approval_id: uuid.UUID, approve: bool, reason: str) -> bool:
        """Update approval status (approved/rejected)."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(DbAgentApproval).where(DbAgentApproval.id == approval_id))
            approval = res.scalar_one_or_none()
            if not approval:
                return False
                
            approval.status = "approved" if approve else "rejected"
            approval.decision_reason = reason
            session.add(approval)
            await session.commit()
            return True

# Global manager instance
agent_approvals = AgentApprovalManager()
