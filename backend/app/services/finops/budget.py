import uuid
import logging
from typing import Dict, Any, List
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.finops import DbBudget

logger = logging.getLogger("app.services.finops.budget")

class BudgetManager:
    async def evaluate_budget_alarms(self) -> List[Dict[str, Any]]:
        """Check all budgets against limits and compile alerts for overruns."""
        alerts = []
        async with TestingSessionLocal() as session:
            from sqlalchemy import select
            res = await session.execute(select(DbBudget))
            budgets = res.scalars().all()
            
            for b in budgets:
                ratio = (b.current_spending / b.limit_amount) * 100.0
                if ratio >= b.alert_threshold_pct:
                    alerts.append({
                        "budget_id": str(b.id),
                        "name": b.name,
                        "ratio_pct": ratio,
                        "limit": b.limit_amount,
                        "current": b.current_spending
                    })
                    logger.warn(f"Budget '{b.name}' has reached {ratio:.2f}% of limit!")
                    
        return alerts

# Global manager instance
budget_manager = BudgetManager()
