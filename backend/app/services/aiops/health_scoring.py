import logging
from typing import Dict, Any
from app.infrastructure.db.session import TestingSessionLocal
from app.infrastructure.db.models.aiops import DbOperationalHealthScore

logger = logging.getLogger("app.services.aiops.health_scoring")

class HealthScoringEngine:
    async def calculate_scope_health(
        self,
        scope_type: str,
        scope_id: str,
        factors: Dict[str, float]  # e.g., {"cpu_spikes": 2, "slo_violations": 1, "vulnerabilities": 5}
    ) -> DbOperationalHealthScore:
        """Aggregate warning factors, calculate 0-100 score, and save results."""
        # Baseline score is 100
        score = 100.0
        
        # Deduct based on factors weights
        deductions = {
            "cpu_spikes": 5.0,
            "slo_violations": 20.0,
            "vulnerabilities": 10.0,
            "errors_ratio_pct": 1.5
        }
        
        for factor, count in factors.items():
            weight = deductions.get(factor, 2.0)
            score -= (count * weight)
            
        score = max(0.0, min(100.0, score))
        
        async with TestingSessionLocal() as session:
            health = DbOperationalHealthScore(
                scope_type=scope_type,
                scope_id=scope_id,
                health_score=score,
                breakdown_json=factors
            )
            session.add(health)
            await session.commit()
            return health

# Global health engine instance
health_scoring_engine = HealthScoringEngine()
