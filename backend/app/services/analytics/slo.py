import uuid
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.analytics import DbSLOObjective

class SLOObjectiveTracker:
    async def evaluate_slo_compliance(self, slo_id: uuid.UUID, current_metrics: dict) -> Dict[str, Any]:
        """Check if metric updates violate active SLO thresholds, returning availability metrics."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(DbSLOObjective).where(DbSLOObjective.id == slo_id))
            slo = res.scalar_one_or_none()
            if not slo:
                return {"compliant": True, "error": "SLO not found"}
                
            metric_val = current_metrics.get(slo.metric_name, 0.0)
            is_compliant = True
            
            if slo.operator == "less_than":
                is_compliant = metric_val < slo.target_value
            elif slo.operator == "greater_than":
                is_compliant = metric_val > slo.target_value
                
            return {
                "slo_id": str(slo.id),
                "metric": slo.metric_name,
                "current_value": metric_val,
                "target_value": slo.target_value,
                "compliant": is_compliant
            }

# Global tracker instance
slo_tracker = SLOObjectiveTracker()
