import uuid
from typing import Dict
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.incident import Incident

class KPICalculator:
    async def calculate_incident_mttr(self) -> float:
        """Calculate the Mean Time To Resolution (MTTR) in minutes for resolved incidents."""
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(
                select(Incident).where(
                    Incident.status == "resolved",
                    Incident.resolved_at != None
                )
            )
            incidents = res.scalars().all()
            
            if not incidents:
                return 0.0
                
            total_minutes = 0.0
            for inc in incidents:
                if inc.resolved_at and inc.created_at:
                    diff = inc.resolved_at - inc.created_at
                    total_minutes += diff.total_seconds() / 60.0
                    
            return float(total_minutes / len(incidents))

# Global calculator instance
kpi_calculator = KPICalculator()
