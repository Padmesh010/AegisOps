import uuid
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.governance import DbRiskItem

class RiskManagementEngine:
    async def create_risk_item(
        self,
        owner_id: uuid.UUID,
        title: str,
        category: str,
        impact: str,
        likelihood: str,
        mitigation: str
    ) -> DbRiskItem:
        """Log a new operational or security threat to the risk registry."""
        async with TestingSessionLocal() as session:
            risk = DbRiskItem(
                title=title,
                category=category,
                impact_level=impact,
                likelihood_level=likelihood,
                mitigation_steps=mitigation,
                owner_id=owner_id
            )
            session.add(risk)
            await session.commit()
            return risk

# Global risk engine instance
risk_management_engine = RiskManagementEngine()
