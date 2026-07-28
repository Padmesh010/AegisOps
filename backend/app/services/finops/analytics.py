import logging
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.finops import DbCostRecord

logger = logging.getLogger("app.services.finops.analytics")

class CostAnalyticsEngine:
    async def aggregate_costs_by_service(self) -> Dict[str, float]:
        """Aggregate all billing records grouped by service_type string keys."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(DbCostRecord))
            records = res.scalars().all()
            
            aggregates: Dict[str, float] = {}
            for r in records:
                t = r.service_type
                aggregates[t] = aggregates.get(t, 0.0) + r.cost_amount
                
            return aggregates

# Global analytics instance
cost_analytics = CostAnalyticsEngine()
