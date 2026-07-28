import uuid
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.remediation import RemediationPlan

class RemediationPlanner:
    def create_plan_steps(self, incident_title: str) -> List[Dict[str, Any]]:
        """Determine step sequences matching the target incident profile."""
        title_lower = incident_title.lower()
        
        if "cpu" in title_lower or "memory" in title_lower:
            return [
                {
                    "step": 1,
                    "action": "clear_temp_files",
                    "target": "/var/tmp",
                    "rollback_action": "noop"
                },
                {
                    "step": 2,
                    "action": "restart_service",
                    "target": "nginx",
                    "rollback_action": "noop"
                }
            ]
        elif "kubernetes" in title_lower or "pod" in title_lower:
            return [
                {
                    "step": 1,
                    "action": "restart_k8s_pod",
                    "target": "default/aegisops-api-pod-123",
                    "rollback_action": "noop"
                }
            ]
        else:
            return [
                {
                    "step": 1,
                    "action": "clear_temp_files",
                    "target": "/tmp",
                    "rollback_action": "noop"
                }
            ]

    async def generate_plan(self, incident_id: uuid.UUID, title: str) -> RemediationPlan:
        """Create and persist a structured multi-step recovery plan."""
        steps = self.create_plan_steps(title)
        
        async with TestingSessionLocal() as session:
            plan = RemediationPlan(
                incident_id=incident_id,
                risk_score=25.0,  # low default risk
                status="pending_approval",
                steps_data={"steps": steps}
            )
            session.add(plan)
            await session.commit()
            return plan

# Global planner instance
remediation_planner = RemediationPlanner()
